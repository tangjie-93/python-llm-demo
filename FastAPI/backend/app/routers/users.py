"""
用户管理路由模块

该模块处理用户相关的 CRUD 操作：
- 获取用户列表
- 获取单个用户
- 创建用户
- 更新用户
- 删除用户

注意：这些是基础的用户管理接口，实际项目中可能需要：
- 权限控制（只有管理员可以操作）
- 密码加密存储
- 分页支持
"""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.core.response import success_response, error_response
from app.models.user import User, UserCreate, UserUpdate, UserResponse
from app.models.response import ApiResponse
from app.routers.auth import get_password_hash

# 创建 APIRouter 实例
router = APIRouter()


@router.get("/", response_model=ApiResponse[List[UserResponse]])
def get_users(session: Session = Depends(get_session)):
    """
    获取所有用户

    返回数据库中所有用户的列表。

    Args:
        session: 数据库会话（由 Depends 自动注入）

    Returns:
        ApiResponse[List[UserResponse]]: 包含用户列表的统一响应
    """
    users = session.exec(select(User)).all()
    return success_response(data=users, message="获取用户列表成功")


@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
def get_user(user_id: int, session: Session = Depends(get_session)):
    """
    获取指定用户

    根据用户 ID 获取单个用户的详细信息。

    Args:
        user_id: 用户 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        ApiResponse[UserResponse]: 包含用户信息的统一响应

    Raises:
        HTTPException 404: 用户不存在
    """
    user = session.get(User, user_id)
    if not user:
        return error_response(message="用户不存在", error="NotFound")
    return success_response(data=user, msg="获取用户信息成功")


@router.post("/", response_model=ApiResponse[UserResponse])
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    创建新用户

    创建一个新的用户记录。

    Args:
        user: 用户创建数据（请求体）
        session: 数据库会话

    Returns:
        ApiResponse[UserResponse]: 包含创建成功后的用户信息的统一响应

    Raises:
        HTTPException 400: 用户名或邮箱已存在
    """
    # 检查用户名是否已存在
    existing_user = session.exec(
        select(User).where((User.username == user.username) | (User.email == user.email))
    ).first()

    if existing_user:
        if existing_user.username == user.username:
            return error_response(message="用户名已存在", error="Conflict")
        else:
            return error_response(message="邮箱已存在", error="Conflict")

    # Hash the password before creating the user
    hashed_password = get_password_hash(user.password)
    # Create user with hashed password
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return success_response(data=db_user, message="用户创建成功")


@router.put("/{user_id}", response_model=ApiResponse[UserResponse])
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    """
    更新用户

    更新指定用户的信息。
    使用 Pydantic 的 exclude_unset=True，只更新提供的字段。

    Args:
        user_id: 用户 ID（URL 路径参数）
        user: 用户更新数据（请求体）
        session: 数据库会话

    Returns:
        ApiResponse[UserResponse]: 包含更新后的用户信息的统一响应

    Raises:
        HTTPException 404: 用户不存在
    """
    db_user = session.get(User, user_id)
    if not db_user:
        return error_response(message="用户不存在", error="NotFound")

    # 将请求中的非空字段更新到数据库对象
    user_data = user.model_dump(exclude_unset=True)
    
    # Handle password hashing if password is being updated
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return success_response(data=db_user, message="用户更新成功")


@router.delete("/{user_id}", response_model=ApiResponse)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    删除用户

    删除指定的用户记录。

    Args:
        user_id: 用户 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        ApiResponse: 包含删除成功信息的统一响应

    Raises:
        HTTPException 404: 用户不存在
    """
    user = session.get(User, user_id)
    if not user:
        return error_response(message="用户不存在", error="NotFound")

    session.delete(user)
    session.commit()
    return success_response(message="用户删除成功")
