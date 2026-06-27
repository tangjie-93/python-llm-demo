from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime

from sqlmodel import Session, select

from app.models.intelligence import ContentItem, ContentStatus
from app.services.intelligence_classifier import classify_text


@dataclass(frozen=True)
class RawContentItem:
    title: str
    url: str
    source_name: str
    raw_excerpt: str
    source_type: str = "seed"
    published_at: datetime | None = None


def ingest_content_items(session: Session, raw_items: list[RawContentItem]) -> int:
    created = 0
    seen_urls: set[str] = set()
    for raw in raw_items:
        if raw.url in seen_urls:
            continue
        seen_urls.add(raw.url)

        existing = session.exec(select(ContentItem).where(ContentItem.url == raw.url)).first()
        if existing:
            continue

        classification = classify_text(raw.title, raw.raw_excerpt)
        item = ContentItem(
            title=raw.title,
            url=raw.url,
            source_name=raw.source_name,
            source_type=raw.source_type,
            published_at=raw.published_at,
            raw_excerpt=raw.raw_excerpt,
            summary=classification.summary,
            key_points=classification.key_points,
            category=classification.category,
            tags=classification.tags,
            importance=classification.importance,
            reason=classification.reason,
            content_hash=_content_hash(raw.title, raw.raw_excerpt),
            status=ContentStatus.PROCESSED,
        )
        session.add(item)
        created += 1

    session.commit()
    return created


def _content_hash(title: str, text: str) -> str:
    return hashlib.sha256(f"{title}\n{text}".encode("utf-8")).hexdigest()
