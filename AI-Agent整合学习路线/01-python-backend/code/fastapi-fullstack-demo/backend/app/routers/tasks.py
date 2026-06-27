"""
后台任务路由模块

演示 FastAPI BackgroundTasks 的使用：
- 注册后发送欢迎通知
- 创建文章后记录审计日志
"""

import asyncio
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks

from app.core.response import success_response

router = APIRouter(prefix="/tasks", tags=["tasks"])


def write_audit_log(action: str, detail: str):
    """模拟写审计日志（后台任务）"""
    # 实际项目中这里写文件或数据库
    timestamp = datetime.now().isoformat()
    print(f"[AUDIT {timestamp}] {action}: {detail}")


def send_welcome_notification(username: str, email: str):
    """模拟发送欢迎通知（后台任务）"""
    # 实际项目中这里调用邮件/消息服务
    print(f"[NOTIFICATION] 发送欢迎通知给 {username} ({email})")
    # 模拟耗时操作
    import time
    time.sleep(2)
    print(f"[NOTIFICATION] 欢迎通知已发送给 {username}")


@router.post("/send-notification")
async def send_notification(background_tasks: BackgroundTasks):
    """
    演示 BackgroundTasks 的使用

    请求立即返回响应，后台任务异步执行。
    适合场景：发邮件、写审计日志、异步通知等不需要用户等待的操作。
    """
    background_tasks.add_task(write_audit_log, "NOTIFICATION", "用户请求发送通知")
    background_tasks.add_task(
        send_welcome_notification,
        username="demo_user",
        email="demo@example.com"
    )
    return success_response(message="通知已在后台处理")


@router.post("/audit")
async def create_audit_record(background_tasks: BackgroundTasks):
    """
    演示后台写审计日志

    模拟一个需要写审计日志的操作。
    """
    background_tasks.add_task(write_audit_log, "API_CALL", "审计记录接口被调用")
    return success_response(message="操作成功，审计日志将异步写入")
