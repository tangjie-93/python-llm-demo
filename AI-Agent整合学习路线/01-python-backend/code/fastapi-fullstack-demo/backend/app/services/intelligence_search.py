from __future__ import annotations

from sqlmodel import Session, select

from app.models.intelligence import AskResponse, Citation, ContentItem, LocalNote, PublishStatus, SearchResult


def search_public_knowledge(session: Session, query: str, limit: int = 10) -> list[SearchResult]:
    needle = query.lower().strip()
    if not needle:
        return []

    results: list[SearchResult] = []
    for item in session.exec(select(ContentItem).order_by(ContentItem.fetched_at.desc())).all():
        haystack = f"{item.title} {item.summary} {' '.join(item.tags)}".lower()
        if needle in haystack:
            results.append(
                SearchResult(
                    result_type="content",
                    id=item.id or 0,
                    title=item.title,
                    summary=item.summary,
                    category=item.category,
                    tags=item.tags,
                    source=item.url,
                )
            )

    for note in session.exec(select(LocalNote).where(LocalNote.publish_status == PublishStatus.PUBLIC)).all():
        haystack = f"{note.title} {note.summary} {' '.join(note.tags)}".lower()
        if needle in haystack:
            results.append(
                SearchResult(
                    result_type="note",
                    id=note.id or 0,
                    title=note.title,
                    summary=note.summary,
                    category=note.category,
                    tags=note.tags,
                    source=note.file_path,
                )
            )

    return results[:limit]


def answer_with_citations(session: Session, question: str) -> AskResponse:
    results = search_public_knowledge(session, question, limit=3)
    if not results:
        return AskResponse(answer="当前公开资料中没有找到足够依据回答这个问题。", citations=[], refused=True)

    citations = [
        Citation(source_type=result.result_type, id=result.id, title=result.title, excerpt=result.summary[:220])
        for result in results
    ]
    answer = "根据站内公开资料，" + "；".join(result.summary for result in results[:2])
    return AskResponse(answer=answer, citations=citations, refused=False)
