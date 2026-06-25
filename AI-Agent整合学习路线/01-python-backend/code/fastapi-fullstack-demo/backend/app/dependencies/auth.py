"""
认证依赖注入模块

提供 FastAPI 依赖注入函数，用于路由认证
"""

from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.models.user import User
from app.utils.auth import oauth2_scheme


# 创建 OAuth2 认证方案实例
# 这里延迟导入以避免循环依赖
if oauth2_scheme is None:
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """
    获取当前登录用户

    这是一个依赖注入函数，用于需要认证的路由。
    从请求头的 Authorization 字段中提取 JWT token，
    解析并验证 token，然后从数据库中获取用户信息。

    Args:
        token: JWT token（由 Depends 自动从请求头提取）
        session: 数据库会话（由 Depends 自动注入）

    Returns:
        User: 当前登录的用户对象

    Raises:
        HTTPException 401: token 无效或用户不存在
    """
    # 定义认证失败时返回的错误
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 解码 JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # 从载荷中获取用户名（subject）
        username: str = payload.get("sub")

        # 如果没有用户名，抛出认证异常
        if username is None:
            raise credentials_exception

    except JWTError:
        # JWT 解析失败，抛出认证异常
        raise credentials_exception

    # 从数据库中查找用户
    user = session.exec(select(User).where(User.username == username)).first()

    # 如果用户不存在，抛出认证异常
    if user is None:
        raise credentials_exception

    return user
