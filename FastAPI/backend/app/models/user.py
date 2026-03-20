"""
用户模型模块

该模块定义了用户相关的所有数据模型：
- User: 数据库表模型（SQLModel）
- UserCreate: 用户创建请求模型
- UserUpdate: 用户更新请求模型
- UserResponse: 用户响应模型

使用 SQLModel 结合了 Pydantic 和 SQLAlchemy 的功能。
"""

from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    用户数据库表模型

    对应数据库中的 users 表。

    字段说明：
    - id: 主键，自增
    - username: 用户名，唯一索引
    - email: 邮箱，唯一索引
    - hashed_password: 加密后的密码（切勿存储明文密码）
    - full_name: 真实姓名（可选）
    - is_active: 账户是否激活（默认 True）
    - is_superuser: 是否超级管理员（默认 False）

    Attributes:
        id: 用户 ID
        username: 用户名
        email: 邮箱地址
        hashed_password: 哈希密码
        full_name: 真实姓名
        is_active: 是否激活
        is_superuser: 是否超级管理员

    Note:
        - table=True 表示这是一个数据库表模型
        - __tablename__ 指定表名（默认类名小写）
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class UserCreate(SQLModel):
    """
    用户创建请求模型

    用于 POST /api/users 或 POST /api/auth/register 接口的请求体验证。

    Attributes:
        username: 用户名（必填）
        email: 邮箱地址（必填）
        password: 密码（必填）
        full_name: 真实姓名（可选）
    """
    username: str
    email: str
    password: str
    full_name: Optional[str] = None


class UserUpdate(SQLModel):
    """
    用户更新请求模型

    用于 PUT /api/users/{id} 接口的请求体验证。

    所有字段都是可选的，只有提供的字段才会被更新。

    Attributes:
        username: 用户名（可选）
        email: 邮箱地址（可选）
        password: 密码（可选）
        full_name: 真实姓名（可选）
        is_active: 是否激活（可选）
    """
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(SQLModel):
    """
    用户响应模型

    用于 API 响应的数据模型，不包含敏感信息（如密码）。

    Attributes:
        id: 用户 ID
        username: 用户名
        email: 邮箱地址
        full_name: 真实姓名
        is_active: 是否激活

    Note:
        - 不包含 password、hashed_password、is_superuser 等敏感字段
    """
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        """
        Pydantic 模型配置

        from_attributes = True:
            允许从 ORM 对象（如 SQLModel 实例）创建模型实例。
            这样可以直接从数据库对象序列化到响应模型。
        """
        from_attributes = True
