"""
认证路由模块

该模块处理所有与用户认证相关的 API 端点，包括：
- 用户登录 (token)
- 用户注册
- 获取当前用户信息
- Token 刷新
- 用户登出

使用 JWT (JSON Web Token) 进行身份验证。
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.response import success_response, error_response
from app.models.user import User
from app.models.response import ApiResponse
from app.schemas.auth import UserCreate
from app.services.auth_service import (
    login_tracker,
    validate_password_strength,
    validate_username,
    validate_email,
)
from app.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from app.dependencies.auth import get_current_user


# 创建 APIRouter 实例
# prefix 已在 routers/__init__.py 中设置为 /api/auth
router = APIRouter()


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
    # 验证用户名格式
    print(f"validating username: {form_data.username}")
    if not validate_username(form_data.username):
        print("username validation failed")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名格式错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查是否被锁定
    print("checking lock status")
    is_locked, remaining_minutes = login_tracker.is_locked_out(form_data.username)
    if is_locked:
        print(f"account locked, remaining: {remaining_minutes} minutes")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"登录尝试次数过多，账户已锁定。请 {remaining_minutes} 分钟后再试",
            headers={"Retry-After": str(remaining_minutes * 60)},
        )

    # 根据用户名查找用户
    print(f"querying user: {form_data.username}")
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
    response_data = success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": int(access_token_expires.total_seconds())
        },
        message="登录成功"
    )
    
    response = Response(
        content=response_data.model_dump_json(),
        media_type="application/json"
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
    if not validate_username(user_data.username):
        return error_response(message="用户名格式错误，应为 4-32 位字母、数字或下划线")
    
    # 验证密码强度
    is_valid, message = validate_password_strength(user_data.password)
    if not is_valid:
        return error_response(message=message)
    
    # 验证邮箱格式
    if not validate_email(user_data.email):
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
