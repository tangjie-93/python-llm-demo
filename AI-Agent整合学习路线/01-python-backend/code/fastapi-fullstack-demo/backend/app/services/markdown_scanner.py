from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlmodel import Session, select

from app.models.intelligence import ContentStatus, LocalNote, PublishStatus
from app.services.intelligence_classifier import classify_text


def scan_markdown_root(session: Session, root: Path) -> int:
    scanned = 0
    for path in sorted(root.rglob("*.md")):
        if path.is_file():
            _upsert_note(session, path)
            scanned += 1
    session.commit()
    return scanned


def _upsert_note(session: Session, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(text)
    title = _extract_title(body, path)
    classification = classify_text(title, body)
    publish_status = PublishStatus.PUBLIC if frontmatter.get("publish") is True else PublishStatus.PRIVATE
    existing = session.exec(select(LocalNote).where(LocalNote.file_path == str(path))).first()

    payload = {
        "title": title,
        "updated_at": datetime.fromtimestamp(path.stat().st_mtime),
        "frontmatter": frontmatter,
        "summary": classification.summary,
        "category": classification.category,
        "tags": classification.tags,
        "publish_status": publish_status,
        "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "index_status": ContentStatus.PROCESSED,
    }

    if existing:
        for key, value in payload.items():
            setattr(existing, key, value)
        session.add(existing)
    else:
        session.add(LocalNote(file_path=str(path), **payload))


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    frontmatter: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        cleaned = value.strip()
        if cleaned.lower() in {"true", "false"}:
            frontmatter[key.strip()] = cleaned.lower() == "true"
        else:
            frontmatter[key.strip()] = cleaned
    return frontmatter, body


def _extract_title(body: str, path: Path) -> str:
    match = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else path.stem
