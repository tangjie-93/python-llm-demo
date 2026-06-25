"""
认证相关的 Pydantic 模型

该模块定义了所有与认证相关的数据传输对象（DTO）
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    JWT 令牌响应模型

    Attributes:
        access_token: 访问令牌
        token_type: 令牌类型（通常为 "bearer"）
        refresh_token: 刷新令牌
        expires_in: access_token 过期时间（秒）
    """
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int


class TokenData(BaseModel):
    """
    JWT 令牌载荷数据模型

    用于解析 JWT 中的用户信息

    Attributes:
        username: 用户名（JWT 的 subject）
    """
    username: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """
    刷新令牌请求模型

    Attributes:
        refresh_token: 刷新令牌
    """
    refresh_token: str


class UserCreate(BaseModel):
    """
    用户创建请求模型

    用于接收用户注册时的请求数据

    Attributes:
        username: 用户名 (4-32 位字母数字下划线)
        email: 邮箱地址
        password: 密码 (至少 8 位，包含大小写字母和数字)
    """
    username: str
    email: str
    password: str
