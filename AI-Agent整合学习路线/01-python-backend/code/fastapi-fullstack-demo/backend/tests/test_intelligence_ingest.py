from datetime import date

from sqlmodel import Session, SQLModel, create_engine, select

from app.core import database as _database  # noqa: F401
from app.models.intelligence import ContentItem, DailyBrief, IntelligenceCategory
from app.services.daily_brief import generate_daily_brief
from app.services.intelligence_ingest import RawContentItem, ingest_content_items


def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_ingest_content_items_deduplicates_by_url():
    session = make_session()
    raw_items = [
        RawContentItem(
            title="LangGraph tool calling update",
            url="https://example.com/langgraph-tools",
            source_name="Example AI",
            raw_excerpt="Agent workflows and tool calling are improved.",
        ),
        RawContentItem(
            title="LangGraph tool calling update copy",
            url="https://example.com/langgraph-tools",
            source_name="Example AI",
            raw_excerpt="Duplicate item.",
        ),
    ]

    created = ingest_content_items(session, raw_items)
    items = session.exec(select(ContentItem)).all()

    assert created == 1
    assert len(items) == 1
    assert items[0].category == IntelligenceCategory.AGENT


def test_generate_daily_brief_groups_items_by_category():
    session = make_session()
    ingest_content_items(
        session,
        [
            RawContentItem(
                title="Hybrid RAG guide",
                url="https://example.com/hybrid-rag",
                source_name="Example AI",
                raw_excerpt="RAG retrieval, pgvector, embeddings, and reranking.",
            ),
            RawContentItem(
                title="Agent workflow release",
                url="https://example.com/agent-workflow",
                source_name="Example AI",
                raw_excerpt="Agent workflow release with tool calling.",
            ),
        ],
    )

    brief = generate_daily_brief(session, brief_date=date(2026, 6, 27))
    saved = session.exec(select(DailyBrief)).one()

    assert brief.id == saved.id
    assert "2026-06-27" in brief.title
    assert len(brief.sections) >= 2
