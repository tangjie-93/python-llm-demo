"""
认证路由模块

该模块处理所有与用户认证相关的 API 端点，包括：
- 用户登录 (token)
- 用户注册
- 获取当前用户信息

使用 JWT (JSON Web Token) 进行身份验证。
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import secrets
import re
from collections import defaultdict
import threading

from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.core.response import success_response, error_response
from app.models.user import User
from app.models.response import ApiResponse

# 创建 APIRouter 实例
# prefix 已在 routers/__init__.py 中设置为 /api/auth
router = APIRouter()

# ==================== 登录失败限制 ====================

class LoginAttemptTracker:
    """
    登录失败追踪器
    
    用于记录每个用户的登录失败次数，防止暴力破解。
    使用内存存储，生产环境建议使用 Redis。
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.failed_attempts: Dict[str, list] = defaultdict(list)
        self.max_attempts = 5  # 最大失败次数
        self.lockout_duration = timedelta(hours=1)  # 锁定时长
    
    def record_failed_attempt(self, username: str) -> None:
        """记录一次失败尝试"""
        with self._lock:
            now = datetime.now(timezone.utc)
            self.failed_attempts[username].append(now)
            # 清理 1 小时前的记录
            cutoff = now - timedelta(hours=1)
            self.failed_attempts[username] = [
                t for t in self.failed_attempts[username] if t > cutoff
            ]
    
    def get_failed_count(self, username: str) -> int:
        """获取当前失败次数"""
        with self._lock:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
            recent_attempts = [
                t for t in self.failed_attempts[username] if t > cutoff
            ]
            return len(recent_attempts)
    
    def is_locked_out(self, username: str) -> tuple[bool, Optional[int]]:
        """
        检查是否被锁定
        
        Returns:
            tuple[bool, Optional[int]]: (是否锁定，剩余锁定时间（分钟）)
        """
        with self._lock:
            failed_count = self.get_failed_count(username)
            
            if failed_count >= self.max_attempts:
                # 计算最早失败时间
                if self.failed_attempts[username]:
                    earliest = min(self.failed_attempts[username])
                    now = datetime.now(timezone.utc)
                    remaining = self.lockout_duration - (now - earliest)
                    
                    if remaining.total_seconds() > 0:
                        return True, int(remaining.total_seconds() / 60)
                
                # 锁定时间已过，重置计数
                self.failed_attempts[username] = []
            
            return False, None
    
    def reset_failed_attempts(self, username: str) -> None:
        """重置失败计数（登录成功后调用）"""
        with self._lock:
            self.failed_attempts[username] = []


# 全局登录失败追踪器
login_tracker = LoginAttemptTracker()

# ==================== 密码加密相关 ====================

# CryptContext 用于密码 hashing
# schemes=["pbkdf2_sha256"]: 使用 pbkdf2_sha256 算法进行密码加密
# deprecated="auto": 允许密码算法升级
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

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


# ==================== 密码处理函数 ====================

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    验证密码强度

    密码必须满足：
    - 至少 8 位
    - 包含大小写字母
    - 包含数字

    Args:
        password: 待验证的密码

    Returns:
        tuple[bool, str]: (是否通过，错误消息)
    """
    if len(password) < 8:
        return False, "密码长度至少为 8 位"
    
    if not re.search(r'[a-z]', password):
        return False, "密码必须包含小写字母"
    
    if not re.search(r'[A-Z]', password):
        return False, "密码必须包含大写字母"
    
    if not re.search(r'\d', password):
        return False, "密码必须包含数字"
    
    return True, ""


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


def verify_refresh_token(user: User, refresh_token: str) -> bool:
    """
    验证刷新令牌

    验证提供的 refresh token 是否与用户存储的匹配且未过期。

    Args:
        user: 用户对象
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

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    用户登录

    验证用户名和密码，返回 JWT 访问令牌和刷新令牌。
    使用 OAuth2PasswordRequestForm 格式（form-data），自动处理表单数据。

    Args:
        form_data: 用户提交的用户名和密码（FastAPI 自动从表单数据解析）
        session: 数据库会话

    Returns:
        ApiResponse[Token]: 包含 access_token、refresh_token 和 token_type 的统一响应

    Raises:
        HTTPException 401: 用户名或密码错误
        HTTPException 429: 登录尝试次数过多

    Note:
        - 请求需要使用 Content-Type: application/x-www-form-urlencoded
        - 需要传递 username 和 password 两个字段
        - access_token 有效期 15 分钟
        - refresh_token 有效期 7 天，存储在 HttpOnly Cookie 中
        - 5 次失败后锁定账户 1 小时
    """
    print("login form_data:", form_data)

    # 验证用户名格式
    if not re.match(r'^[a-zA-Z0-9_]{4,32}$', form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名格式错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查是否被锁定
    is_locked, remaining_minutes = login_tracker.is_locked_out(form_data.username)
    if is_locked:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"登录尝试次数过多，账户已锁定。请 {remaining_minutes} 分钟后再试",
            headers={"Retry-After": str(remaining_minutes * 60)},
        )

    # 根据用户名查找用户
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    # 验证用户是否存在
    if not user:
        # 记录失败尝试
        login_tracker.record_failed_attempt(form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在，请先注册",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证密码是否正确
    if not verify_password(form_data.password, user.hashed_password):
        # 记录失败尝试
        login_tracker.record_failed_attempt(form_data.username)
        failed_count = login_tracker.get_failed_count(form_data.username)
        remaining_attempts = login_tracker.max_attempts - failed_count
        
        if remaining_attempts <= 0:
            detail = "登录尝试次数过多，账户已锁定。请 60 分钟后再试"
        else:
            detail = f"密码错误，还剩 {remaining_attempts} 次尝试机会"
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 登录成功，重置失败计数
    login_tracker.reset_failed_attempts(form_data.username)

    # 创建访问令牌（15 分钟）
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    # 创建刷新令牌（7 天）
    refresh_token = create_refresh_token()
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(days=7)
    
    # 保存 refresh token 到数据库
    user.refresh_token = refresh_token
    user.token_expires_at = refresh_token_expires.isoformat()
    session.commit()

    # 创建响应
    response = Response(
        content=success_response(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": int(access_token_expires.total_seconds())
            },
            message="登录成功"
        )["detail"]
    )
    
    # 设置 HttpOnly Cookie 存储 refresh token
    # httponly=True: JavaScript 无法访问，防止 XSS 攻击
    # samesite="lax": 防止 CSRF 攻击
    # secure=False: 开发环境允许 HTTP，生产环境应设为 True（HTTPS）
    # max_age: Cookie 有效期（秒）
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,  # 生产环境改为 True
        max_age=int(refresh_token_expires.timestamp() - datetime.now(timezone.utc).timestamp()),
        path="/api/auth/refresh"  # 只在 refresh 接口发送此 Cookie
    )
    
    return response


@router.post("/register", response_model=ApiResponse)
async def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    用户注册

    创建新用户账号。

    Args:
        user_data: 用户注册数据
        session: 数据库会话

    Returns:
        ApiResponse: 包含成功消息和用户 ID 的统一响应

    Raises:
        HTTPException 400: 用户名或邮箱已存在、用户名格式错误、密码强度不足
    """
    # 验证用户名格式 (4-32 位字母数字下划线)
    if not re.match(r'^[a-zA-Z0-9_]{4,32}$', user_data.username):
        return error_response(message="用户名格式错误，应为 4-32 位字母、数字或下划线")
    
    # 验证密码强度
    is_valid, message = validate_password_strength(user_data.password)
    if not is_valid:
        return error_response(message=message)
    
    # 验证邮箱格式
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, user_data.email):
        return error_response(message="邮箱格式不正确")
    
    # 检查用户名或邮箱是否已存在
    existing_user = session.exec(
        select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    ).first()

    if existing_user:
        return error_response(message="用户名或邮箱已存在", error="Conflict")

    # 加密密码
    hashed_password = get_password_hash(user_data.password)

    # 创建新用户
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True  # 新用户默认激活
    )

    # 保存到数据库
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return success_response(data={"user_id": new_user.id}, message="用户注册成功")


@router.get("/me", response_model=ApiResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息

    需要先登录获取 token，然后在请求头中携带 token 才能访问。

    Args:
        current_user: 当前登录用户（由 Depends(get_current_user) 自动注入）

    Returns:
        ApiResponse: 包含当前用户基本信息的统一响应
    """
    user_info = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active
    }
    return success_response(data=user_info, message="获取用户信息成功")


@router.post("/refresh", response_model=ApiResponse)
async def refresh_access_token(
    request: Request,
    session: Session = Depends(get_session)
):
    """
    刷新访问令牌

    从 HttpOnly Cookie 中读取 refresh token 并刷新 access token。

    Args:
        request: HTTP 请求对象（用于读取 Cookie）
        session: 数据库会话

    Returns:
        ApiResponse[Token]: 包含新的 access_token 的统一响应

    Raises:
        HTTPException 401: refresh_token 无效或已过期
    """
    # 从 Cookie 中读取 refresh token
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未找到刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 查找拥有该 refresh token 的用户
    user = session.exec(select(User).where(User.refresh_token == refresh_token)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证 refresh token
    if not verify_refresh_token(user, refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌已过期或无效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建新的 access token（15 分钟）
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    # 创建新的 refresh token（7 天）
    new_refresh_token = create_refresh_token()
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(days=7)
    
    # 更新数据库中的 refresh token
    user.refresh_token = new_refresh_token
    user.token_expires_at = refresh_token_expires.isoformat()
    session.commit()
    
    # 创建响应
    response = Response(
        content=success_response(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": int(access_token_expires.total_seconds())
            },
            message="Token 刷新成功"
        )["detail"]
    )
    
    # 更新 HttpOnly Cookie 中的 refresh token
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,  # 生产环境改为 True
        max_age=int(refresh_token_expires.timestamp() - datetime.now(timezone.utc).timestamp()),
        path="/api/auth/refresh"
    )
    
    return response


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    用户登出

    清除用户的 refresh token 和 Cookie。

    Args:
        current_user: 当前登录用户
        session: 数据库会话

    Returns:
        Response: 成功消息，并清除 refresh_token Cookie
    """
    # 清除数据库中的 refresh token
    current_user.refresh_token = None
    current_user.token_expires_at = None
    session.commit()
    
    # 创建响应并清除 Cookie
    response = Response(
        content=success_response(message="登出成功")["detail"]
    )
    
    # 删除 refresh_token Cookie
    response.delete_cookie(
        key="refresh_token",
        path="/api/auth/refresh"
    )
    
    return response
