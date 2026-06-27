from fastapi import BackgroundTasks


def test_background_task_example(client, auth_headers):
    """验证后台任务机制：请求返回后仍可执行任务"""
    response = client.post("/api/tasks/send-notification", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "已在后台处理" in data["message"]
