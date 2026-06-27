def test_list_items(client, auth_headers):
    response = client.get("/api/items/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_create_item(client, auth_headers):
    """创建物品 — owner_id 从 JWT 当前用户自动获取"""
    response = client.post("/api/items/", json={
        "title": "Test Item",
        "description": "Test Description",
        "price": 9.99,
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Test Item"
    assert data["data"]["owner_id"] == 1  # testuser 的 id


def test_get_item(client, auth_headers):
    create_resp = client.post("/api/items/", json={
        "title": "Get Item",
        "description": "Test",
        "price": 5.0,
    }, headers=auth_headers)
    item_id = create_resp.json()["data"]["id"]

    response = client.get(f"/api/items/{item_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Get Item"


def test_get_nonexistent_item(client, auth_headers):
    response = client.get("/api/items/99999", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False


def test_update_item(client, auth_headers):
    create_resp = client.post("/api/items/", json={
        "title": "Update Item",
        "description": "Test",
        "price": 5.0,
    }, headers=auth_headers)
    item_id = create_resp.json()["data"]["id"]

    response = client.put(f"/api/items/{item_id}", json={
        "title": "Updated Item"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Updated Item"


def test_update_item_forbidden(client, auth_headers, admin_headers):
    """更新非本人物品应返回 403"""
    # admin 创建物品
    create_resp = client.post("/api/items/", json={
        "title": "Admin Item",
        "description": "Admin's",
        "price": 10.0,
    }, headers=admin_headers)
    item_id = create_resp.json()["data"]["id"]

    # testuser 尝试更新
    response = client.put(f"/api/items/{item_id}", json={
        "title": "Hacked Item"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False


def test_delete_item(client, auth_headers):
    create_resp = client.post("/api/items/", json={
        "title": "Delete Item",
        "description": "Test",
        "price": 5.0,
    }, headers=auth_headers)
    item_id = create_resp.json()["data"]["id"]

    response = client.delete(f"/api/items/{item_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_delete_item_forbidden(client, auth_headers, admin_headers):
    """删除非本人物品应返回 403"""
    # admin 创建物品
    create_resp = client.post("/api/items/", json={
        "title": "Admin Item 2",
        "description": "Admin's",
        "price": 10.0,
    }, headers=admin_headers)
    item_id = create_resp.json()["data"]["id"]

    # testuser 尝试删除
    response = client.delete(f"/api/items/{item_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False
