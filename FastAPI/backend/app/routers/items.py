"""
物品管理路由模块

该模块处理物品相关的 CRUD 操作：
- 获取物品列表（支持分页）
- 获取单个物品
- 创建物品
- 更新物品
- 删除物品

注意：这些是基础的物品管理接口，实际项目中可能需要：
- 权限控制（只有物品所有者可以操作）
- 更多的查询参数（搜索、排序等）
"""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List, Optional

from app.core.database import get_session
from app.core.response import success_response, error_response
from app.models.item import Item, ItemCreate, ItemUpdate, ItemResponse
from app.models.response import ApiResponse

# 创建 APIRouter 实例
router = APIRouter()


@router.get("/", response_model=ApiResponse[List[ItemResponse]])
def get_items(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """
    获取物品列表

    返回数据库中物品的列表，支持分页。

    Query 参数:
        skip: 跳过的记录数（用于分页，默认 0）
        limit: 返回的记录数（用于分页，默认 100）

    Args:
        skip: 跳过的记录数
        limit: 返回的记录数限制
        session: 数据库会话

    Returns:
        ApiResponse[List[ItemResponse]]: 包含物品列表的统一响应
    """
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return success_response(data=items, message="获取物品列表成功")


@router.get("/{item_id}", response_model=ApiResponse[ItemResponse])
def get_item(item_id: int, session: Session = Depends(get_session)):
    """
    获取指定物品

    根据物品 ID 获取单个物品的详细信息。

    Args:
        item_id: 物品 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        ApiResponse[ItemResponse]: 包含物品信息的统一响应

    Raises:
        HTTPException 404: 物品不存在
    """
    item = session.get(Item, item_id)
    if not item:
        return error_response(message="物品不存在", error="NotFound")
    return success_response(data=item, message="获取物品信息成功")


@router.post("/", response_model=ApiResponse[ItemResponse])
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    """
    创建新物品

    创建一个新的物品记录。

    Args:
        item: 物品创建数据（请求体）
        session: 数据库会话

    Returns:
        ApiResponse[ItemResponse]: 包含创建成功后的物品信息的统一响应
    """
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return success_response(data=db_item, message="物品创建成功")


@router.put("/{item_id}", response_model=ApiResponse[ItemResponse])
def update_item(item_id: int, item: ItemUpdate, session: Session = Depends(get_session)):
    """
    更新物品

    更新指定物品的信息。
    使用 Pydantic 的 exclude_unset=True，只更新提供的字段。

    Args:
        item_id: 物品 ID（URL 路径参数）
        item: 物品更新数据（请求体）
        session: 数据库会话

    Returns:
        ApiResponse[ItemResponse]: 包含更新后的物品信息的统一响应

    Raises:
        HTTPException 404: 物品不存在
    """
    db_item = session.get(Item, item_id)
    if not db_item:
        return error_response(message="物品不存在", error="NotFound")

    # 将请求中的非空字段更新到数据库对象
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return success_response(data=db_item, message="物品更新成功")


@router.delete("/{item_id}", response_model=ApiResponse)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """
    删除物品

    删除指定的物品记录。

    Args:
        item_id: 物品 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        ApiResponse: 包含删除成功信息的统一响应

    Raises:
        HTTPException 404: 物品不存在
    """
    item = session.get(Item, item_id)
    if not item:
        return error_response(message="物品不存在", error="NotFound")

    session.delete(item)
    session.commit()
    return success_response(message="物品删除成功")
