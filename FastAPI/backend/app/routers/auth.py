"""
认证路由模块

该模块处理所有与用户认证相关的 API 端点，包括：
- 用户登录 (token)
- 用户注册
- 获取当前用户信息

使用 JWT (JSON Web Token) 进行身份验证。
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.models.user import User

# 创建 APIRouter 实例
# prefix 已在 routers/__init__.py 中设置为 /api/auth
router = APIRouter()

# ==================== 密码加密相关 ====================

# CryptContext 用于密码 hashing
# schemes=["bcrypt"]: 使用 bcrypt 算法进行密码加密（推荐）
# deprecated="auto": 允许密码算法升级
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer 用于从请求头中提取 token
# tokenUrl 指定了登录接口的 URL（相对路径）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# ==================== 数据模型 ====================

class Token(BaseModel):
    """
    JWT 令牌响应模型

    Attributes:
        access_token: 访问令牌
        token_type: 令牌类型（通常为 "bearer"）
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    JWT 令牌载荷数据模型

    用于解析 JWT 中的用户信息

    Attributes:
        username: 用户名（JWT 的 subject）
    """
    username: Optional[str] = None


# ==================== 密码处理函数 ====================

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

    # 使用 JWT 编码
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# ==================== 依赖注入函数 ====================

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

        # 创建 TokenData 对象
        token_data = TokenData(username=username)

    except JWTError:
        # JWT 解析失败，抛出认证异常
        raise credentials_exception

    # 从数据库中查找用户
    user = session.exec(select(User).where(User.username == token_data.username)).first()

    # 如果用户不存在，抛出认证异常
    if user is None:
        raise credentials_exception

    return user


# ==================== 路由端点 ====================

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    用户登录

    验证用户名和密码，返回 JWT 访问令牌。
    使用 OAuth2PasswordRequestForm 格式（form-data），自动处理表单数据。

    Args:
        form_data: 用户提交的用户名和密码（FastAPI 自动从表单数据解析）
        session: 数据库会话

    Returns:
        Token: 包含 access_token 和 token_type 的响应

    Raises:
        HTTPException 401: 用户名或密码错误

    Note:
        - 请求需要使用 Content-Type: application/x-www-form-urlencoded
        - 需要传递 username 和 password 两个字段
    """
    print("login form_data:", form_data)

    # 根据用户名查找用户
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    # 验证用户是否存在且密码正确
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  # sub = subject，通常放用户名
        expires_delta=access_token_expires
    )

    # 返回令牌
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(
    username: str,
    email: str,
    password: str,
    session: Session = Depends(get_session)
):
    """
    用户注册

    创建新用户账号。

    Args:
        username: 用户名（必填）
        email: 邮箱地址（必填）
        password: 密码（必填）
        session: 数据库会话

    Returns:
        dict: 包含成功消息和用户 ID

    Raises:
        HTTPException 400: 用户名或邮箱已存在
    """
    # 检查用户名或邮箱是否已存在
    existing_user = session.exec(
        select(User).where((User.username == username) | (User.email == email))
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # 加密密码
    hashed_password = get_password_hash(password)

    # 创建新用户
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_active=True  # 新用户默认激活
    )

    # 保存到数据库
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息

    需要先登录获取 token，然后在请求头中携带 token 才能访问。

    Args:
        current_user: 当前登录用户（由 Depends(get_current_user) 自动注入）

    Returns:
        dict: 当前用户的基本信息
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active
    }
