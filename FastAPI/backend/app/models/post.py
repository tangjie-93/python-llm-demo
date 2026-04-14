"""
博客文章模型模块

该模块定义了博客系统相关的所有数据模型：
- Post: 文章数据库表模型
- Tag: 标签数据库表模型
- PostTagLink: 文章和标签的多对多关联表
- PostCreate/PostUpdate/PostResponse: Pydantic 请求/响应模型
- TagCreate/TagUpdate/TagResponse: 标签的请求/响应模型

关系说明：
- User (1) ----< Post (N): 一个用户可以有多篇文章
- Post (N) >----< Tag (N): 一篇文章可以有多个标签，一个标签可以属于多篇文章
"""

from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


# ==================== 关联表（多对多关系）====================

class PostTagLink(SQLModel, table=True):
    """
    文章和标签的关联表

    实现 Post 和 Tag 的多对多关系。

    Attributes:
        post_id: 文章 ID，外键关联到 post 表
        tag_id: 标签 ID，外键关联到 tag 表
    """
    __tablename__ = "post_tag_links"

    post_id: Optional[int] = Field(
        default=None,
        foreign_key="posts.id",
        primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None,
        foreign_key="tags.id",
        primary_key=True
    )


# ==================== 数据库表模型 ====================

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
        link_model=PostTagLink
    )


class Post(SQLModel, table=True):
    """
    文章数据库表模型

    对应数据库中的 posts 表。

    字段说明：
    - id: 主键，自增
    - title: 文章标题
    - content: 文章内容
    - summary: 文章摘要（可选）
    - author_id: 作者 ID，外键关联到 users 表
    - is_published: 是否发布（默认 False）
    - view_count: 浏览次数（默认 0）
    - created_at: 创建时间
    - updated_at: 更新时间

    关系：
    - author: 多对一关系，关联到 User 模型
    - tags: 多对多关系，关联到 Tag 模型

    Attributes:
        id: 文章 ID
        title: 文章标题
        content: 文章内容
        summary: 文章摘要
        author_id: 作者 ID
        is_published: 是否发布
        view_count: 浏览次数
        created_at: 创建时间
        updated_at: 更新时间
        author: 作者对象
        tags: 标签列表
    """
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    content: str
    summary: Optional[str] = Field(default=None, max_length=500)
    author_id: int = Field(foreign_key="users.id")
    is_published: bool = Field(default=False)
    view_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # 多对一关系：一篇文章属于一个作者
    author: Optional["User"] = Relationship(back_populates="posts")

    # 多对多关系：一篇文章可以有多个标签
    tags: List["Tag"] = Relationship(
        back_populates="posts",
        link_model=PostTagLink
    )


# ==================== Pydantic 请求/响应模型 ====================

# ----- 标签相关模型 -----

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


# ----- 文章相关模型 -----

class PostCreate(SQLModel):
    """
    文章创建请求模型

    Attributes:
        title: 文章标题（必填）
        content: 文章内容（必填）
        summary: 文章摘要（可选）
        is_published: 是否发布（可选，默认 False）
        tag_ids: 标签 ID 列表（可选）
    """
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    summary: Optional[str] = Field(default=None, max_length=500)
    is_published: bool = Field(default=False)
    tag_ids: List[int] = Field(default=[])


class PostUpdate(SQLModel):
    """
    文章更新请求模型

    所有字段都是可选的，只有提供的字段才会被更新。

    Attributes:
        title: 文章标题（可选）
        content: 文章内容（可选）
        summary: 文章摘要（可选）
        is_published: 是否发布（可选）
        tag_ids: 标签 ID 列表（可选，会替换原有标签）
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, min_length=1)
    summary: Optional[str] = Field(default=None, max_length=500)
    is_published: Optional[bool] = None
    tag_ids: Optional[List[int]] = None


class PostSimpleResponse(SQLModel):
    """
    文章简化响应模型

    用于在列表中显示文章基本信息，不包含完整内容。

    Attributes:
        id: 文章 ID
        title: 文章标题
        summary: 文章摘要
        author_id: 作者 ID
        is_published: 是否发布
        view_count: 浏览次数
        created_at: 创建时间
        updated_at: 更新时间
    """
    id: int
    title: str
    summary: Optional[str] = None
    author_id: int
    is_published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostResponse(PostSimpleResponse):
    """
    文章完整响应模型

    包含文章的完整信息和关联数据。

    Attributes:
        content: 文章内容
        author: 作者信息（简化）
        tags: 标签列表
    """
    content: str
    author: "UserSimpleResponse"
    tags: List[TagResponse] = []


# ----- 作者简化信息模型 -----

class UserSimpleResponse(SQLModel):
    """
    用户简化响应模型

    用于在文章响应中显示作者基本信息，不包含敏感信息。

    Attributes:
        id: 用户 ID
        username: 用户名
        full_name: 真实姓名
    """
    id: int
    username: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True


# 更新前向引用
TagWithPosts.model_rebuild()
PostResponse.model_rebuild()
