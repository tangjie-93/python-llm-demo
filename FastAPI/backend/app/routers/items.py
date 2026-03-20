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

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from app.core.database import get_session
from app.models.item import Item, ItemCreate, ItemUpdate, ItemResponse

# 创建 APIRouter 实例
router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
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
        List[ItemResponse]: 物品列表
    """
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, session: Session = Depends(get_session)):
    """
    获取指定物品

    根据物品 ID 获取单个物品的详细信息。

    Args:
        item_id: 物品 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        ItemResponse: 物品信息

    Raises:
        HTTPException 404: 物品不存在
    """
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    """
    创建新物品

    创建一个新的物品记录。

    Args:
        item: 物品创建数据（请求体）
        session: 数据库会话

    Returns:
        ItemResponse: 创建成功后的物品信息
    """
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=ItemResponse)
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
        ItemResponse: 更新后的物品信息

    Raises:
        HTTPException 404: 物品不存在
    """
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # 将请求中的非空字段更新到数据库对象
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """
    删除物品

    删除指定的物品记录。

    Args:
        item_id: 物品 ID（URL 路径参数）
        session: 数据库会话

    Returns:
        HTTP 204 No Content

    Raises:
        HTTPException 404: 物品不存在
    """
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(item)
    session.commit()
    return None
