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

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.user import User, UserCreate, UserUpdate, UserResponse

# 创建 APIRouter 实例
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(session: Session = Depends(get_session)):
    """
    获取所有用户

    返回数据库中所有用户的列表。

    Args:
        session: 数据库会话（由 Depends 自动注入）

    Returns:
        List[UserResponse]: 用户列表
    """
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """
    获取指定用户

    根据用户 ID 获取单个用户的详细信息。

    Args:
        user_id: 用户 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        UserResponse: 用户信息

    Raises:
        HTTPException 404: 用户不存在
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    创建新用户

    创建一个新的用户记录。

    Args:
        user: 用户创建数据（请求体）
        session: 数据库会话

    Returns:
        UserResponse: 创建成功后的用户信息
    """
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
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
        UserResponse: 更新后的用户信息

    Raises:
        HTTPException 404: 用户不存在
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 将请求中的非空字段更新到数据库对象
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    删除用户

    删除指定的用户记录。

    Args:
        user_id: 用户 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        HTTP 204 No Content

    Raises:
        HTTPException 404: 用户不存在
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return None
