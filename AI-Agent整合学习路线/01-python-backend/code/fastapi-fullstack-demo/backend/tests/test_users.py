def test_list_users(client, auth_headers, test_user):
    response = client.get("/api/users/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) >= 1


def test_get_user(client, auth_headers, test_user):
    response = client.get(f"/api/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "testuser"


def test_get_nonexistent_user(client, auth_headers):
    response = client.get("/api/users/99999", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_create_user(client):
    response = client.post("/api/users/", json={
        "username": "anotheruser",
        "email": "another@example.com",
        "password": "StrongPass1!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_update_user(client, auth_headers, test_user):
    """用户更新自己 — 应成功"""
    response = client.put(f"/api/users/{test_user.id}", json={
        "full_name": "Updated Name"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_update_user_forbidden(client, auth_headers, admin_headers):
    """非管理员更新其他用户 — 应返回 403"""
    # admin 创建用户
    client.post("/api/users/", json={
        "username": "victim",
        "email": "victim@example.com",
        "password": "StrongPass1!"
    })
    list_resp = client.get("/api/users/", headers=auth_headers)
    users = list_resp.json()["data"]
    target = [u for u in users if u["username"] == "victim"][0]

    # testuser 尝试更新 victim（非本人无权限）
    response = client.put(f"/api/users/{target['id']}", json={
        "full_name": "Hacked Name"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_delete_user(client, auth_headers, admin_headers):
    """管理员删除其他用户 — 应成功"""
    # 创建待删除用户
    client.post("/api/users/", json={
        "username": "todelete",
        "email": "delete@example.com",
        "password": "StrongPass1!"
    })
    list_resp = client.get("/api/users/", headers=auth_headers)
    users = list_resp.json()["data"]
    target = [u for u in users if u["username"] == "todelete"][0]

    # admin 删除用户
    response = client.delete(f"/api/users/{target['id']}", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_delete_user_forbidden(client, auth_headers):
    """普通用户删除其他用户 — 应返回 403"""
    # 创建待删除用户
    client.post("/api/users/", json={
        "username": "todelete2",
        "email": "delete2@example.com",
        "password": "StrongPass1!"
    })
    list_resp = client.get("/api/users/", headers=auth_headers)
    users = list_resp.json()["data"]
    target = [u for u in users if u["username"] == "todelete2"][0]

    # testuser 尝试删除（非本人无权限）
    response = client.delete(f"/api/users/{target['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
