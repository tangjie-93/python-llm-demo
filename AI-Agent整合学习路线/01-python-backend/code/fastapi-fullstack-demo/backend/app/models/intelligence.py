from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class IntelligenceCategory(str, Enum):
    AGENT = "Agent"
    RAG = "RAG"
    LLM_API = "LLM API"
    MCP_TOOLS = "MCP / Tools"
    OPEN_SOURCE = "Open Source"
    PAPERS = "Papers"
    PRODUCTS = "Products"
    TUTORIALS = "Tutorials"
    DEPLOYMENT_EVAL_SECURITY = "Deployment / Eval / Security"
    UNCATEGORIZED = "Uncategorized"


class PublishStatus(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    DRAFT = "draft"


class ContentStatus(str, Enum):
    RAW = "raw"
    PROCESSED = "processed"
    FAILED = "failed"


class ContentItem(SQLModel, table=True):
    __tablename__ = "intelligence_content_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=300)
    url: str = Field(unique=True, index=True, min_length=1, max_length=1000)
    source_name: str = Field(index=True, min_length=1, max_length=120)
    source_type: str = Field(default="rss", max_length=40)
    published_at: Optional[datetime] = Field(default=None, index=True)
    fetched_at: datetime = Field(default_factory=datetime.now, index=True)
    raw_excerpt: str = Field(default="")
    summary: str = Field(default="")
    key_points: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    category: IntelligenceCategory = Field(default=IntelligenceCategory.UNCATEGORIZED, index=True)
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    importance: int = Field(default=3, ge=1, le=5, index=True)
    reason: str = Field(default="")
    content_hash: str = Field(index=True, max_length=64)
    status: ContentStatus = Field(default=ContentStatus.RAW, index=True)


class LocalNote(SQLModel, table=True):
    __tablename__ = "intelligence_local_notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=300)
    file_path: str = Field(unique=True, index=True, min_length=1, max_length=1000)
    updated_at: datetime = Field(index=True)
    frontmatter: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    summary: str = Field(default="")
    category: IntelligenceCategory = Field(default=IntelligenceCategory.UNCATEGORIZED, index=True)
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    publish_status: PublishStatus = Field(default=PublishStatus.PRIVATE, index=True)
    content_hash: str = Field(index=True, max_length=64)
    index_status: ContentStatus = Field(default=ContentStatus.RAW, index=True)


class DailyBrief(SQLModel, table=True):
    __tablename__ = "intelligence_daily_briefs"

    id: Optional[int] = Field(default=None, primary_key=True)
    brief_date: date = Field(unique=True, index=True)
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(default="")
    sections: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    generated_at: datetime = Field(default_factory=datetime.now, index=True)
    status: ContentStatus = Field(default=ContentStatus.PROCESSED, index=True)


class IntelligenceChunk(SQLModel, table=True):
    __tablename__ = "intelligence_chunks"

    id: Optional[int] = Field(default=None, primary_key=True)
    object_type: str = Field(index=True, max_length=40)
    object_id: int = Field(index=True)
    chunk_text: str
    chunk_metadata: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.now, index=True)


class ClassifiedContent(SQLModel):
    summary: str
    key_points: list[str]
    category: IntelligenceCategory
    tags: list[str]
    audience: str = "developer"
    importance: int = Field(ge=1, le=5)
    reason: str


class ContentItemRead(SQLModel):
    id: int
    title: str
    url: str
    source_name: str
    published_at: Optional[datetime]
    summary: str
    key_points: list[str]
    category: IntelligenceCategory
    tags: list[str]
    importance: int
    reason: str


class LocalNoteRead(SQLModel):
    id: int
    title: str
    file_path: str
    updated_at: datetime
    summary: str
    category: IntelligenceCategory
    tags: list[str]
    publish_status: PublishStatus


class DailyBriefRead(SQLModel):
    id: int
    brief_date: date
    title: str
    summary: str
    sections: list[dict[str, Any]]
    generated_at: datetime


class SearchResult(SQLModel):
    result_type: str
    id: int
    title: str
    summary: str
    category: IntelligenceCategory
    tags: list[str]
    source: str


class Citation(SQLModel):
    source_type: str
    id: int
    title: str
    excerpt: str


class AskResponse(SQLModel):
    answer: str
    citations: list[Citation]
    refused: bool = False
