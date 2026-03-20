"""
物品模型模块

该模块定义了物品相关的所有数据模型：
- Item: 数据库表模型（SQLModel）
- ItemCreate: 物品创建请求模型
- ItemUpdate: 物品更新请求模型
- ItemResponse: 物品响应模型

使用 SQLModel 结合了 Pydantic 和 SQLAlchemy 的功能。
"""

from typing import Optional
from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    """
    物品数据库表模型

    对应数据库中的 items 表。

    字段说明：
    - id: 主键，自增
    - title: 物品标题，普通索引
    - description: 物品描述（可选）
    - price: 价格，必须大于 0
    - tax: 税费（可选，必须大于等于 0）
    - owner_id: 所有者 ID，外键关联 users 表

    Attributes:
        id: 物品 ID
        title: 物品标题
        description: 物品描述
        price: 价格
        tax: 税费
        owner_id: 所有者用户 ID

    Note:
        - table=True 表示这是一个数据库表模型
        - __tablename__ 指定表名（默认类名小写）
        - 使用 Field 的 gt、ge 参数进行数值校验
    """
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    price: float = Field(gt=0)  # gt=0 表示必须大于 0
    tax: Optional[float] = Field(default=None, ge=0)  # ge=0 表示必须大于等于 0
    owner_id: int = Field(foreign_key="users.id")  # 外键关联 users 表


class ItemCreate(SQLModel):
    """
    物品创建请求模型

    用于 POST /api/items 接口的请求体验证。

    Attributes:
        title: 物品标题（必填）
        description: 物品描述（可选）
        price: 价格（必填，必须大于 0）
        tax: 税费（可选，必须大于等于 0）
        owner_id: 所有者 ID（必填）
    """
    title: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    owner_id: int


class ItemUpdate(SQLModel):
    """
    物品更新请求模型

    用于 PUT /api/items/{id} 接口的请求体验证。

    所有字段都是可选的，只有提供的字段才会被更新。

    Attributes:
        title: 物品标题（可选）
        description: 物品描述（可选）
        price: 价格（可选，必须大于 0）
        tax: 税费（可选，必须大于等于 0）
    """
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None


class ItemResponse(SQLModel):
    """
    物品响应模型

    用于 API 响应的数据模型。

    Attributes:
        id: 物品 ID
        title: 物品标题
        description: 物品描述
        price: 价格
        tax: 税费
        owner_id: 所有者用户 ID
    """
    id: int
    title: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    owner_id: int

    class Config:
        """
        Pydantic 模型配置

        from_attributes = True:
            允许从 ORM 对象（如 SQLModel 实例）创建模型实例。
            这样可以直接从数据库对象序列化到响应模型。
        """
        from_attributes = True
