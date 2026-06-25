"""
中间件模块

该模块负责配置 FastAPI 应用的中间件。
使用 setup_ 函数模式，将中间件配置集中管理。

中间件 (Middleware) 是在请求到达路由之前或响应返回之前执行的代码。
它可以用于：
- 日志记录
- CORS 跨域处理
- 请求/响应拦截
- 性能监控
- 安全头部设置
- 等等
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from app.core.config import settings


def setup_middleware(app: FastAPI):
    """
    配置应用中间件

    当前配置了 CORS 中间件和安全头部中间件。

    CORS (Cross-Origin Resource Sharing) 跨域资源共享：
        - 由于浏览器的同源策略，前端应用（域名 A）无法直接请求后端 API（域名 B）
        - CORS 中间件通过在响应头中添加允许跨域的信息来解决这个问题

    Args:
        app: FastAPI 应用实例

    配置说明：
        - allow_origins: 允许访问的来源域名列表
        - allow_credentials: 允许携带凭证（cookie、Authorization header 等）
        - allow_methods: 允许的 HTTP 方法
        - allow_headers: 允许的 HTTP 请求头
    """
    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # 允许的来源域名
        allow_credentials=True,               # 允许携带凭证
        allow_methods=["*"],                  # 允许所有 HTTP 方法
        allow_headers=["*"],                  # 允许所有请求头
    )

    # 添加安全头部中间件
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        """
        添加安全相关的 HTTP 响应头

        包括：
        - X-Frame-Options: 防止点击劫持攻击
        - X-Content-Type-Options: 防止 MIME 类型嗅探
        - X-XSS-Protection: XSS 防护
        - Strict-Transport-Security: 强制使用 HTTPS
        - Content-Security-Policy: 内容安全策略
        - Referrer-Policy: 控制 referrer 信息
        """
        response = await call_next(request)
        
        # 防止点击劫持
        response.headers["X-Frame-Options"] = "DENY"
        
        # 防止 MIME 类型嗅探
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # XSS 防护
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # 强制使用 HTTPS (max-age=31536000 表示 1 年)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # 内容安全策略
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;"
        
        # 控制 referrer 信息
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response
