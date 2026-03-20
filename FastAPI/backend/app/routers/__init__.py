"""
路由模块初始化文件

该模块负责集中注册所有路由。
使用 setup_ 函数模式，将路由配置集中管理，保持 main.py 的简洁。
"""

from fastapi import FastAPI
from app.routers import users, items, auth


def setup_routers(app: FastAPI):
    """
    注册所有路由

    将各个模块的路由注册到 FastAPI 应用中。
    每个路由都可以指定：
    - prefix: URL 前缀
    - tags: API 文档中的分组标签

    Args:
        app: FastAPI 应用实例

    Example:
        # 注册后，可用的 API 路径：
        # - GET    /api/users/       获取用户列表
        # - POST   /api/users/       创建用户
        # - GET    /api/users/{id}  获取指定用户
        # - PUT    /api/users/{id}  更新用户
        # - DELETE /api/users/{id}  删除用户
        #
        # - GET    /api/items/       获取物品列表
        # - POST   /api/items/       创建物品
        # - GET    /api/items/{id}  获取指定物品
        # - PUT    /api/items/{id}  更新物品
        # - DELETE /api/items/{id}  删除物品
        #
        # - POST   /api/auth/token   用户登录
        # - POST   /api/auth/register 用户注册
        # - GET    /api/auth/me      获取当前用户信息
    """
    # 用户管理路由
    # /api/users
    app.include_router(users.router, prefix="/api/users", tags=["users"])

    # 物品管理路由
    # /api/items
    app.include_router(items.router, prefix="/api/items", tags=["items"])

    # 认证路由
    # /api/auth
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
