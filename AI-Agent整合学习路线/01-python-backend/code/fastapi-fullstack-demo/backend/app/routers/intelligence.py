from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.response import success_response
from app.models.intelligence import (
    AskResponse,
    ContentItem,
    ContentItemRead,
    DailyBrief,
    DailyBriefRead,
    IntelligenceCategory,
    LocalNote,
    PublishStatus,
    SearchResult,
)
from app.services.daily_brief import generate_daily_brief
from app.services.intelligence_ingest import RawContentItem, ingest_content_items
from app.services.intelligence_search import answer_with_citations, search_public_knowledge

router = APIRouter(prefix="/intelligence", tags=["intelligence"])


@router.get("/categories")
def list_categories():
    labels = [category.value for category in IntelligenceCategory if category != IntelligenceCategory.UNCATEGORIZED]
    return success_response(data=labels, message="获取分类成功")


@router.post("/seed")
def seed_demo_content(session: Session = Depends(get_session)):
    created = ingest_content_items(
        session,
        [
            RawContentItem(
                title="LangGraph tool calling update",
                url="https://example.com/langgraph-tools",
                source_name="Example AI",
                raw_excerpt="Agent workflows and tool calling are improved for multi-step AI applications.",
            ),
            RawContentItem(
                title="Hybrid RAG with pgvector",
                url="https://example.com/hybrid-rag",
                source_name="Example AI",
                raw_excerpt="A practical guide to RAG retrieval, embeddings, reranking, and citations.",
            ),
        ],
    )
    brief = generate_daily_brief(session, date.today())
    return success_response(data={"created": created, "brief_id": brief.id}, message="演示内容已生成")


@router.get("/home")
def get_home(session: Session = Depends(get_session)):
    latest_items = session.exec(select(ContentItem).order_by(ContentItem.fetched_at.desc()).limit(12)).all()
    brief = session.exec(select(DailyBrief).order_by(DailyBrief.brief_date.desc()).limit(1)).first()
    categories = [category.value for category in IntelligenceCategory if category != IntelligenceCategory.UNCATEGORIZED]
    return success_response(
        data={
            "latest_items": [ContentItemRead.model_validate(item) for item in latest_items],
            "brief": DailyBriefRead.model_validate(brief) if brief else None,
            "categories": categories,
        },
        message="获取首页数据成功",
    )


@router.get("/contents")
def list_contents(
    category: Optional[IntelligenceCategory] = Query(default=None),
    session: Session = Depends(get_session),
):
    query = select(ContentItem).order_by(ContentItem.fetched_at.desc())
    if category:
        query = query.where(ContentItem.category == category)
    items = session.exec(query.limit(50)).all()
    return success_response(data=[ContentItemRead.model_validate(item) for item in items], message="获取内容列表成功")


@router.get("/contents/{content_id}")
def get_content(content_id: int, session: Session = Depends(get_session)):
    item = session.get(ContentItem, content_id)
    return success_response(data=ContentItemRead.model_validate(item) if item else None, message="获取内容详情成功")


@router.get("/briefs")
def list_briefs(session: Session = Depends(get_session)):
    briefs = session.exec(select(DailyBrief).order_by(DailyBrief.brief_date.desc()).limit(30)).all()
    return success_response(data=[DailyBriefRead.model_validate(brief) for brief in briefs], message="获取简报列表成功")


@router.get("/notes")
def list_public_notes(session: Session = Depends(get_session)):
    notes = session.exec(select(LocalNote).where(LocalNote.publish_status == PublishStatus.PUBLIC)).all()
    return success_response(data=notes, message="获取公开笔记成功")


@router.get("/search", response_model=None)
def search(q: str = Query(min_length=1), session: Session = Depends(get_session)):
    results: list[SearchResult] = search_public_knowledge(session, q)
    return success_response(data=results, message="搜索成功")


@router.get("/ask", response_model=None)
def ask(q: str = Query(min_length=1), session: Session = Depends(get_session)):
    answer: AskResponse = answer_with_citations(session, q)
    return success_response(data=answer, message="问答完成")
