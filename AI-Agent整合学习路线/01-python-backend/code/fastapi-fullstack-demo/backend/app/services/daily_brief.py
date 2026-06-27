from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, time
from typing import Any

from sqlmodel import Session, select

from app.models.intelligence import ContentItem, ContentStatus, DailyBrief


def generate_daily_brief(session: Session, brief_date: date) -> DailyBrief:
    existing = session.exec(select(DailyBrief).where(DailyBrief.brief_date == brief_date)).first()
    if existing:
        return existing

    start = datetime.combine(brief_date, time.min)
    end = datetime.combine(brief_date, time.max)
    items = session.exec(
        select(ContentItem)
        .where(ContentItem.fetched_at >= start)
        .where(ContentItem.fetched_at <= end)
        .order_by(ContentItem.importance.desc(), ContentItem.fetched_at.desc())
    ).all()

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item.category.value].append(
            {
                "id": item.id,
                "title": item.title,
                "summary": item.summary,
                "url": item.url,
                "tags": item.tags,
                "importance": item.importance,
                "reason": item.reason,
            }
        )

    sections = [{"category": category, "items": values[:5]} for category, values in grouped.items()]
    summary = f"今日共收录 {len(items)} 条 AI Agent 开发与学习相关内容。"
    brief = DailyBrief(
        brief_date=brief_date,
        title=f"{brief_date.isoformat()} AI Agent 每日简报",
        summary=summary,
        sections=sections,
        status=ContentStatus.PROCESSED,
    )
    session.add(brief)
    session.commit()
    session.refresh(brief)
    return brief
