"""
认证工具模块

提供 JWT 令牌生成、密码加密等底层认证工具函数
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


# 密码加密上下文
# schemes=["pbkdf2_sha256"]: 使用 pbkdf2_sha256 算法进行密码加密
# deprecated="auto": 允许密码算法升级
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# OAuth2 认证方案
# tokenUrl 指定了登录接口的 URL（用于 Swagger UI 的认证按钮）
oauth2_scheme = None  # 在 dependencies 模块中创建，避免循环依赖


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确

    将明文密码与数据库中的哈希密码进行比对。

    Args:
        plain_password: 用户输入的明文密码
        hashed_password: 数据库中存储的哈希密码

    Returns:
        bool: 密码正确返回 True，否则返回 False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    生成密码哈希

    将明文密码转换为哈希值，用于存储到数据库中。

    Args:
        password: 明文密码

    Returns:
        str: 加密后的哈希密码
    """
    # Truncate password to 72 bytes to avoid bcrypt limit
    password = password[:72]
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT 访问令牌

    生成一个带有过期时间的 JWT token。

    Args:
        data: 要编码到 token 中的数据（通常是 {"sub": username}）
        expires_delta: 令牌过期时间增量

    Returns:
        str: 编码后的 JWT token 字符串
    """
    # 复制数据字典，避免修改原数据
    to_encode = data.copy()

    # 设置过期时间
    if expires_delta:
        # 如果指定了过期时间增量
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 默认 15 分钟
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # 将过期时间添加到 token 载荷中
    to_encode.update({"exp": expire})
    to_encode.update({"type": "access"})

    # 使用 JWT 编码
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token() -> str:
    """
    创建刷新令牌

    生成一个随机的 refresh token，用于刷新 access token。

    Returns:
        str: 随机生成的 refresh token
    """
    return secrets.token_urlsafe(32)


def verify_refresh_token(user, refresh_token: str) -> bool:
    """
    验证刷新令牌

    验证提供的 refresh token 是否与用户存储的匹配且未过期。

    Args:
        user: 用户对象（需要有 refresh_token 和 token_expires_at 属性）
        refresh_token: 刷新令牌

    Returns:
        bool: 验证成功返回 True，否则返回 False
    """
    if not user.refresh_token or not user.token_expires_at:
        return False
    
    # 检查 token 是否匹配
    if user.refresh_token != refresh_token:
        return False
    
    # 检查是否过期
    expires_at = datetime.fromisoformat(user.token_expires_at)
    if datetime.now(timezone.utc) > expires_at:
        return False
    
    return True
