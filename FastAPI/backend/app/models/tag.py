"""
标签模型模块

该模块定义了博客系统中标签相关的所有数据模型：
- Tag: 标签数据库表模型
- TagCreate: 标签创建请求模型
- TagUpdate: 标签更新请求模型
- TagResponse: 标签响应模型
- TagWithPosts: 包含文章列表的标签响应模型

关系：
- Post (N) >----< Tag (N): 一篇文章可以有多个标签，一个标签可以属于多篇文章
"""

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.post import Post


class Tag(SQLModel, table=True):
    """
    标签数据库表模型

    对应数据库中的 tags 表。

    字段说明：
    - id: 主键，自增
    - name: 标签名称，唯一
    - description: 标签描述（可选）
    - created_at: 创建时间

    关系：
    - posts: 多对多关系，关联到 Post 模型

    Attributes:
        id: 标签 ID
        name: 标签名称
        description: 标签描述
        created_at: 创建时间
        posts: 关联的文章列表
    """
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.now)

    # 多对多关系：一个标签可以属于多篇文章
    posts: List["Post"] = Relationship(
        back_populates="tags",
        link_model="PostTagLink"
    )


class TagCreate(SQLModel):
    """
    标签创建请求模型

    Attributes:
        name: 标签名称（必填）
        description: 标签描述（可选）
    """
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)


class TagUpdate(SQLModel):
    """
    标签更新请求模型

    所有字段都是可选的，只有提供的字段才会被更新。

    Attributes:
        name: 标签名称（可选）
        description: 标签描述（可选）
    """
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)


class TagResponse(SQLModel):
    """
    标签响应模型

    Attributes:
        id: 标签 ID
        name: 标签名称
        description: 标签描述
        created_at: 创建时间
    """
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TagWithPosts(TagResponse):
    """
    包含文章列表的标签响应模型

    用于获取标签详情时，同时返回该标签下的所有文章。

    Attributes:
        posts: 该标签下的文章列表（简化信息）
    """
    posts: List["PostSimpleResponse"] = []


# 前向引用会在 post.py 中统一处理
