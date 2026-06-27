from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

from app.core import database as _database  # noqa: F401
from app.models.intelligence import IntelligenceCategory, LocalNote, PublishStatus
from app.services.markdown_scanner import scan_markdown_root


def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_scan_markdown_root_only_publishes_marked_notes(tmp_path: Path):
    public_note = tmp_path / "rag-note.md"
    public_note.write_text(
        "---\npublish: true\n---\n# RAG Note\n\nHybrid RAG uses retrieval and pgvector.",
        encoding="utf-8",
    )
    private_note = tmp_path / "private.md"
    private_note.write_text("# Private\n\nThis should stay private.", encoding="utf-8")

    session = make_session()
    scanned = scan_markdown_root(session, tmp_path)
    notes = session.exec(select(LocalNote)).all()

    assert scanned == 2
    assert len(notes) == 2
    public = next(note for note in notes if note.title == "RAG Note")
    private = next(note for note in notes if note.title == "Private")
    assert public.publish_status == PublishStatus.PUBLIC
    assert public.category == IntelligenceCategory.RAG
    assert private.publish_status == PublishStatus.PRIVATE
