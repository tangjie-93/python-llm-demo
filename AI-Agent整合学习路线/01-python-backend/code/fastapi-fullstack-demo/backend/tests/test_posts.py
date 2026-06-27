def test_list_posts(client, auth_headers):
    response = client.get("/api/posts/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_create_post(client, auth_headers):
    response = client.post("/api/posts/", json={
        "title": "Test Post",
        "content": "Test Content Body",
        "summary": "A test summary",
        "is_published": True
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Test Post"


def test_get_post(client, auth_headers):
    create_resp = client.post("/api/posts/", json={
        "title": "Get Post",
        "content": "Content",
        "summary": "Summary",
        "is_published": True
    }, headers=auth_headers)
    post_id = create_resp.json()["data"]["id"]

    response = client.get(f"/api/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Get Post"


def test_get_nonexistent_post(client, auth_headers):
    response = client.get("/api/posts/99999", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False


def test_update_post(client, auth_headers):
    create_resp = client.post("/api/posts/", json={
        "title": "Update Post",
        "content": "Content",
        "summary": "Summary",
        "is_published": False
    }, headers=auth_headers)
    post_id = create_resp.json()["data"]["id"]

    response = client.patch(f"/api/posts/{post_id}", json={
        "title": "Updated Post"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Updated Post"


def test_update_post_forbidden(client, auth_headers, admin_headers):
    """非作者更新文章 — 应返回 403"""
    # admin 创建文章
    create_resp = client.post("/api/posts/", json={
        "title": "Admin Post",
        "content": "Content",
        "summary": "Summary",
        "is_published": True
    }, headers=admin_headers)
    post_id = create_resp.json()["data"]["id"]

    # testuser 尝试更新
    response = client.patch(f"/api/posts/{post_id}", json={
        "title": "Hacked Post"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False


def test_publish_post(client, auth_headers):
    create_resp = client.post("/api/posts/", json={
        "title": "Publish Post",
        "content": "Content",
        "summary": "Summary",
        "is_published": False
    }, headers=auth_headers)
    post_id = create_resp.json()["data"]["id"]

    response = client.post(f"/api/posts/{post_id}/publish", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["is_published"] is True


def test_unpublish_post(client, auth_headers):
    create_resp = client.post("/api/posts/", json={
        "title": "Unpublish Post",
        "content": "Content",
        "summary": "Summary",
        "is_published": True
    }, headers=auth_headers)
    post_id = create_resp.json()["data"]["id"]

    response = client.post(f"/api/posts/{post_id}/unpublish", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["data"]["is_published"] is False


def test_delete_post(client, auth_headers):
    create_resp = client.post("/api/posts/", json={
        "title": "Delete Post",
        "content": "Content",
        "summary": "Summary",
        "is_published": True
    }, headers=auth_headers)
    post_id = create_resp.json()["data"]["id"]

    response = client.delete(f"/api/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_delete_post_forbidden(client, auth_headers, admin_headers):
    """非作者删除文章 — 应返回 403"""
    # admin 创建文章
    create_resp = client.post("/api/posts/", json={
        "title": "Admin Post 2",
        "content": "Content",
        "summary": "Summary",
        "is_published": True
    }, headers=admin_headers)
    post_id = create_resp.json()["data"]["id"]

    # testuser 尝试删除
    response = client.delete(f"/api/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False


def test_create_post_tag(client, auth_headers):
    tag_resp = client.post("/api/posts/tags/", json={
        "name": "test-tag"
    }, headers=auth_headers)
    tag_id = tag_resp.json()["data"]["id"]

    response = client.post("/api/posts/", json={
        "title": "Tagged Post",
        "content": "Content",
        "summary": "Summary",
        "is_published": True,
        "tag_ids": [tag_id]
    }, headers=auth_headers)
    assert response.status_code == 201
    assert len(response.json()["data"]["tags"]) == 1


def test_list_tags(client, auth_headers):
    response = client.get("/api/posts/tags/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is True
