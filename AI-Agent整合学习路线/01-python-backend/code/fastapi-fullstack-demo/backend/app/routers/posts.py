"""
博客文章路由模块

该模块实现了博客系统的文章相关 API：
- 文章的 CRUD 操作
- 文章标签管理
- 文章发布/取消发布
- 浏览量统计

路由前缀: /api/posts
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.response import success_response, error_response
from app.models.post import (
    Post, PostCreate, PostUpdate, PostResponse, PostSimpleResponse,
    UserSimpleResponse
)
from app.models.tag import (
    Tag, TagCreate, TagUpdate, TagResponse, TagWithPosts, PostTagLink
)
from app.models.user import User
from app.models.response import ApiResponse

router = APIRouter(prefix="/posts", tags=["posts"])


# ==================== 文章相关 API ====================

@router.get("/", response_model=ApiResponse[List[PostSimpleResponse]])
def list_posts(
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=10, ge=1, le=100, description="返回的记录数"),
    is_published: Optional[bool] = Query(default=None, description="筛选发布状态"),
    author_id: Optional[int] = Query(default=None, description="筛选作者"),
    tag_id: Optional[int] = Query(default=None, description="筛选标签"),
    session: Session = Depends(get_session)
):
    """
    获取文章列表

    支持分页和多种筛选条件：
    - is_published: 筛选已发布/未发布文章
    - author_id: 筛选特定作者的文章
    - tag_id: 筛选包含特定标签的文章
    """
    query = select(Post)

    # 应用筛选条件
    if is_published is not None:
        query = query.where(Post.is_published == is_published)
    if author_id is not None:
        query = query.where(Post.author_id == author_id)
    if tag_id is not None:
        # 通过关联表筛选包含特定标签的文章
        from app.models.post import PostTagLink
        query = query.join(PostTagLink).where(PostTagLink.tag_id == tag_id)

    # 按创建时间倒序排列
    query = query.order_by(Post.created_at.desc())
    query = query.offset(skip).limit(limit)

    posts = session.exec(query).all()
    return success_response(data=posts, message="获取文章列表成功")


@router.get("/{post_id}", response_model=ApiResponse[PostResponse])
def get_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    """
    获取文章详情

    返回文章的完整信息，包括作者和标签。
    同时会增加文章的浏览次数。
    """
    post = session.get(Post, post_id)
    if not post:
        return error_response(message="文章不存在", error="NotFound")

    # 增加浏览次数
    post.view_count += 1
    session.add(post)
    session.commit()

    return success_response(data=post, message="获取文章详情成功")


@router.post("/", response_model=ApiResponse[PostResponse], status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    author_id: int,  # 实际项目中应该从 JWT Token 中获取
    session: Session = Depends(get_session)
):
    """
    创建新文章

    创建文章并关联标签（如果提供了 tag_ids）。
    """
    # 验证作者是否存在
    author = session.get(User, author_id)
    if not author:
        return error_response(message="作者不存在", error="NotFound")

    # 创建文章
    post = Post(
        title=post_data.title,
        content=post_data.content,
        summary=post_data.summary,
        author_id=author_id,
        is_published=post_data.is_published
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    # 关联标签
    if post_data.tag_ids:
        tags = session.exec(select(Tag).where(Tag.id.in_(post_data.tag_ids))).all()
        post.tags = tags
        session.add(post)
        session.commit()
        session.refresh(post)

    return success_response(data=post, message="文章创建成功")


@router.patch("/{post_id}", response_model=ApiResponse[PostResponse])
def update_post(
    post_id: int,
    post_data: PostUpdate,
    session: Session = Depends(get_session)
):
    """
    更新文章

    支持部分更新，只有提供的字段才会被更新。
    如果提供了 tag_ids，会替换原有的标签。
    """
    post = session.get(Post, post_id)
    if not post:
        return error_response(message="文章不存在", error="NotFound")

    # 更新基本字段
    update_data = post_data.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for key, value in update_data.items():
        setattr(post, key, value)

    # 更新时间
    post.updated_at = datetime.now()

    # 更新标签（如果提供了 tag_ids）
    if post_data.tag_ids is not None:
        if post_data.tag_ids:
            tags = session.exec(select(Tag).where(Tag.id.in_(post_data.tag_ids))).all()
            post.tags = tags
        else:
            post.tags = []

    session.add(post)
    session.commit()
    session.refresh(post)

    return success_response(data=post, message="文章更新成功")


@router.delete("/{post_id}", response_model=ApiResponse)
def delete_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    """
    删除文章

    删除文章及其标签关联（关联表记录会自动删除）。
    """
    post = session.get(Post, post_id)
    if not post:
        return error_response(message="文章不存在", error="NotFound")

    session.delete(post)
    session.commit()

    return success_response(message="文章删除成功")


@router.post("/{post_id}/publish", response_model=ApiResponse[PostResponse])
def publish_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    """
    发布文章

    将文章状态设置为已发布。
    """
    post = session.get(Post, post_id)
    if not post:
        return error_response(message="文章不存在", error="NotFound")

    post.is_published = True
    post.updated_at = datetime.now()
    session.add(post)
    session.commit()
    session.refresh(post)

    return success_response(data=post, message="文章发布成功")


@router.post("/{post_id}/unpublish", response_model=ApiResponse[PostResponse])
def unpublish_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    """
    取消发布文章

    将文章状态设置为未发布。
    """
    post = session.get(Post, post_id)
    if not post:
        return error_response(message="文章不存在", error="NotFound")

    post.is_published = False
    post.updated_at = datetime.now()
    session.add(post)
    session.commit()
    session.refresh(post)

    return success_response(data=post, message="文章已取消发布")


# ==================== 标签相关 API ====================

@router.get("/tags/", response_model=ApiResponse[List[TagResponse]])
def list_tags(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """
    获取标签列表
    """
    tags = session.exec(select(Tag).offset(skip).limit(limit)).all()
    return success_response(data=tags, message="获取标签列表成功")


@router.get("/tags/{tag_id}", response_model=ApiResponse[TagWithPosts])
def get_tag(
    tag_id: int,
    session: Session = Depends(get_session)
):
    """
    获取标签详情

    返回标签信息及其关联的所有文章。
    """
    tag = session.get(Tag, tag_id)
    if not tag:
        return error_response(message="标签不存在", error="NotFound")

    return success_response(data=tag, message="获取标签详情成功")


@router.post("/tags/", response_model=ApiResponse[TagResponse], status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_data: TagCreate,
    session: Session = Depends(get_session)
):
    """
    创建新标签

    标签名称必须唯一。
    """
    # 检查标签名是否已存在
    existing_tag = session.exec(select(Tag).where(Tag.name == tag_data.name)).first()
    if existing_tag:
        return error_response(message=f"标签 '{tag_data.name}' 已存在", error="Conflict")

    tag = Tag(**tag_data.model_dump())
    session.add(tag)
    session.commit()
    session.refresh(tag)

    return success_response(data=tag, message="标签创建成功")


@router.patch("/tags/{tag_id}", response_model=ApiResponse[TagResponse])
def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    session: Session = Depends(get_session)
):
    """
    更新标签
    """
    tag = session.get(Tag, tag_id)
    if not tag:
        return error_response(message="标签不存在", error="NotFound")

    # 如果更新名称，检查是否与其他标签冲突
    if tag_data.name and tag_data.name != tag.name:
        existing_tag = session.exec(select(Tag).where(Tag.name == tag_data.name)).first()
        if existing_tag:
            return error_response(message=f"标签 '{tag_data.name}' 已存在", error="Conflict")

    update_data = tag_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)

    session.add(tag)
    session.commit()
    session.refresh(tag)

    return success_response(data=tag, message="标签更新成功")


@router.delete("/tags/{tag_id}", response_model=ApiResponse)
def delete_tag(
    tag_id: int,
    session: Session = Depends(get_session)
):
    """
    删除标签

    删除标签会自动解除与文章的关联（关联表记录会自动删除）。
    """
    tag = session.get(Tag, tag_id)
    if not tag:
        return error_response(message="标签不存在", error="NotFound")

    session.delete(tag)
    session.commit()

    return success_response(message="标签删除成功")


# ==================== 文章标签管理 API ====================

@router.post("/{post_id}/tags/{tag_id}", response_model=ApiResponse[PostResponse])
def add_tag_to_post(
    post_id: int,
    tag_id: int,
    session: Session = Depends(get_session)
):
    """
    为文章添加标签
    """
    post = session.get(Post, post_id)
    if not post:
        return error_response(message="文章不存在", error="NotFound")

    tag = session.get(Tag, tag_id)
    if not tag:
        return error_response(message="标签不存在", error="NotFound")

    # 检查标签是否已关联
    if tag in post.tags:
        return error_response(message=f"文章已包含标签 '{tag.name}'", error="Conflict")

    post.tags.append(tag)
    post.updated_at = datetime.now()
    session.add(post)
    session.commit()
    session.refresh(post)

    return success_response(data=post, message="标签添加成功")


@router.delete("/{post_id}/tags/{tag_id}", response_model=ApiResponse[PostResponse])
def remove_tag_from_post(
    post_id: int,
    tag_id: int,
    session: Session = Depends(get_session)
):
    """
    从文章移除标签
    """
    post = session.get(Post, post_id)
    if not post:
        return error_response(message="文章不存在", error="NotFound")

    tag = session.get(Tag, tag_id)
    if not tag:
        return error_response(message="标签不存在", error="NotFound")

    # 检查标签是否已关联
    if tag not in post.tags:
        return error_response(message=f"文章不包含标签 '{tag.name}'", error="Conflict")

    post.tags.remove(tag)
    post.updated_at = datetime.now()
    session.add(post)
    session.commit()
    session.refresh(post)

    return success_response(data=post, message="标签移除成功")
