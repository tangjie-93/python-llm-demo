# AI Agent 情报站实施计划

> **面向 agentic 工作程序：** 必须使用子技能：推荐使用 superpowers:subagent-driven-development 或 superpowers:executing-plans 按任务逐项实施本计划。步骤使用复选框（`- [ ]`）语法进行跟踪。

**目标：** 在现有 FastAPI + Vue 演示项目中构建一个面向 AI Agent 开发者/学习者的公共情报站的首个可运行版本。

**架构：** 在现有后端中添加一个专注的 `intelligence` 领域，包含 SQLModel 表、确定性内容分类、RSS/静态内容采集、本地 Markdown 扫描、公开读取 API、搜索以及带来源引用的问答。添加公开 Vue 路由，显示首页、分类页、内容详情页、每日简报和搜索/问答视图，无需登录。

**技术栈：** FastAPI、SQLModel、SQLite（本地 MVP 阶段）、pytest、Vue 3、Vue Router、Axios、Element Plus、TypeScript。

---

## 文件结构

后端文件：

- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/models/intelligence.py`
  - 内容条目、本地笔记、每日简报、嵌入占位块和来源引用的 SQLModel 表及响应模式。
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_classifier.py`
  - 供测试和本地开发使用的确定性分类器。它镜像 LLM 输出契约，无需网络调用。
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_ingest.py`
  - 采集静态种子条目，按 URL/内容哈希去重，分类并持久化记录。
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/markdown_scanner.py`
  - 扫描配置的 Markdown 根目录，遵循 `publish: true` 标记，提取元数据，分类并持久化本地笔记。
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/daily_brief.py`
  - 按分类分组重要内容，每天生成一份每日简报。
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_search.py`
  - 对公开内容和公开本地笔记进行关键词搜索及简单带引用的问答。
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/routers/intelligence.py`
  - `/api/intelligence` 下的公开 API 路由。
- 修改：`01-python-backend/code/fastapi-fullstack-demo/backend/app/core/database.py`
  - 导入 intelligence 模型，使 `create_db_and_tables()` 创建其表。
- 修改：`01-python-backend/code/fastapi-fullstack-demo/backend/app/routers/__init__.py`
  - 注册 intelligence 路由。
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_classifier.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_ingest.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_markdown_scanner.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_api.py`

前端文件：

- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/types/intelligence.ts`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/api/intelligence.ts`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/PublicLayout.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/HomePage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/CategoryPage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/ContentDetailPage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/BriefsPage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/SearchPage.vue`
- 修改：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/router/index.ts`
  - 在认证布局之前添加公开路由。

文档：

- 修改：`01-python-backend/code/fastapi-fullstack-demo/README.md`
  - 添加情报站的本地运行说明。

## 任务 1：后端领域模型

**涉及文件：**
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/models/intelligence.py`
- 修改：`01-python-backend/code/fastapi-fullstack-demo/backend/app/core/database.py`
- 测试：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_classifier.py`

- [ ] **步骤 1：添加领域模型文件**

创建 `backend/app/models/intelligence.py`，包含以下模型：

```python
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
    metadata: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
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
```

- [ ] **步骤 2：将模型注册到 SQLModel 元数据**

修改 `backend/app/core/database.py`，在现有模型导入附近添加以下导入：

```python
from app.models.intelligence import ContentItem, DailyBrief, IntelligenceChunk, LocalNote
```

- [ ] **步骤 3：添加带导入检查的分类器测试文件**

创建 `backend/tests/test_intelligence_classifier.py`：

```python
from app.models.intelligence import IntelligenceCategory


def test_intelligence_categories_are_fixed_navigation_labels():
    labels = [category.value for category in IntelligenceCategory]

    assert "Agent" in labels
    assert "RAG" in labels
    assert "LLM API" in labels
    assert "Deployment / Eval / Security" in labels
```

- [ ] **步骤 4：运行模型导入测试**

在 `01-python-backend/code/fastapi-fullstack-demo/backend` 下执行：

```bash
pytest tests/test_intelligence_classifier.py -v
```

预期：模型文件存在后测试通过。如果缺少 `pytest`，请在继续之前安装项目测试依赖：

```bash
python -m pip install pytest
```

- [ ] **步骤 5：提交**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/backend/app/models/intelligence.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/app/core/database.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_classifier.py
git commit -m "feat: add intelligence domain models"
```

## 任务 2：确定性分类服务

**涉及文件：**
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_classifier.py`
- 修改：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_classifier.py`

- [ ] **步骤 1：扩展分类器测试**

追加到 `backend/tests/test_intelligence_classifier.py`：

```python
from app.services.intelligence_classifier import classify_text


def test_classify_agent_content():
    result = classify_text(
        title="LangGraph adds better tool calling for agents",
        text="The release improves agent workflows, tool calls, and multi-step execution.",
    )

    assert result.category == IntelligenceCategory.AGENT
    assert "LangGraph" in result.tags
    assert result.importance >= 4


def test_classify_rag_content():
    result = classify_text(
        title="Hybrid RAG with pgvector and BM25",
        text="This tutorial explains retrieval, embeddings, reranking, and citations.",
    )

    assert result.category == IntelligenceCategory.RAG
    assert "pgvector" in result.tags
    assert "retrieval" in [tag.lower() for tag in result.tags]


def test_classify_unknown_content_is_uncategorized():
    result = classify_text(title="Weekly notes", text="A short update without AI technical detail.")

    assert result.category == IntelligenceCategory.UNCATEGORIZED
    assert result.importance == 2
```

- [ ] **步骤 2：运行测试并验证失败**

执行：

```bash
pytest tests/test_intelligence_classifier.py -v
```

预期：失败，报 `ModuleNotFoundError: No module named 'app.services.intelligence_classifier'`。

- [ ] **步骤 3：创建分类器服务**

创建 `backend/app/services/intelligence_classifier.py`：

```python
from __future__ import annotations

import re

from app.models.intelligence import ClassifiedContent, IntelligenceCategory


CATEGORY_KEYWORDS: list[tuple[IntelligenceCategory, list[str]]] = [
    (IntelligenceCategory.AGENT, ["agent", "agents", "langgraph", "tool calling", "workflow", "multi-agent"]),
    (IntelligenceCategory.RAG, ["rag", "retrieval", "embedding", "embeddings", "vector", "rerank", "citation", "pgvector", "qdrant"]),
    (IntelligenceCategory.LLM_API, ["openai api", "responses api", "structured output", "function calling", "llm api"]),
    (IntelligenceCategory.MCP_TOOLS, ["mcp", "model context protocol", "tool server", "tools"]),
    (IntelligenceCategory.OPEN_SOURCE, ["github", "open source", "repo", "library", "framework"]),
    (IntelligenceCategory.PAPERS, ["paper", "arxiv", "research", "benchmark"]),
    (IntelligenceCategory.PRODUCTS, ["launch", "product", "release", "pricing", "preview"]),
    (IntelligenceCategory.TUTORIALS, ["tutorial", "guide", "course", "learn", "how to"]),
    (IntelligenceCategory.DEPLOYMENT_EVAL_SECURITY, ["eval", "evaluation", "deploy", "security", "prompt injection", "observability", "tracing"]),
]

TAG_KEYWORDS: dict[str, list[str]] = {
    "LangGraph": ["langgraph"],
    "LlamaIndex": ["llamaindex", "llama index"],
    "OpenAI API": ["openai", "responses api"],
    "MCP": ["mcp", "model context protocol"],
    "Qdrant": ["qdrant"],
    "pgvector": ["pgvector"],
    "Prompt Injection": ["prompt injection"],
    "Evals": ["eval", "evaluation", "benchmark"],
    "retrieval": ["retrieval", "rag"],
    "Tool Calling": ["tool calling", "function calling", "tools"],
}


def classify_text(title: str, text: str) -> ClassifiedContent:
    combined = f"{title}\n{text}".lower()
    category = _pick_category(combined)
    tags = _pick_tags(combined)
    importance = _score_importance(category, combined)
    summary = _summarize(title, text)
    key_points = _key_points(text)

    return ClassifiedContent(
        summary=summary,
        key_points=key_points,
        category=category,
        tags=tags,
        audience="developer",
        importance=importance,
        reason=_reason(category, tags, importance),
    )


def _pick_category(text: str) -> IntelligenceCategory:
    best_category = IntelligenceCategory.UNCATEGORIZED
    best_score = 0
    for category, keywords in CATEGORY_KEYWORDS:
        score = sum(1 for keyword in keywords if keyword in text)
        if score > best_score:
            best_category = category
            best_score = score
    return best_category


def _pick_tags(text: str) -> list[str]:
    tags = [tag for tag, keywords in TAG_KEYWORDS.items() if any(keyword in text for keyword in keywords)]
    return tags[:6]


def _score_importance(category: IntelligenceCategory, text: str) -> int:
    if category == IntelligenceCategory.UNCATEGORIZED:
        return 2
    score = 3
    if any(word in text for word in ["release", "launch", "benchmark", "security", "open source"]):
        score += 1
    if any(word in text for word in ["agent", "rag", "mcp", "eval"]):
        score += 1
    return min(score, 5)


def _summarize(title: str, text: str) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if clean:
        return f"{title}：{clean[:180]}"
    return title


def _key_points(text: str) -> list[str]:
    sentences = [part.strip() for part in re.split(r"[。.!?]\s*", text) if part.strip()]
    return sentences[:3] if sentences else ["需要进一步阅读原文确认细节"]


def _reason(category: IntelligenceCategory, tags: list[str], importance: int) -> str:
    if category == IntelligenceCategory.UNCATEGORIZED:
        return "内容与当前 AI Agent 学习主题关联较弱。"
    tag_text = "、".join(tags) if tags else category.value
    return f"与 {tag_text} 相关，适合 AI Agent 开发者跟进，重要性 {importance}/5。"
```

- [ ] **步骤 4：运行分类器测试**

执行：

```bash
pytest tests/test_intelligence_classifier.py -v
```

预期：全部通过。

- [ ] **步骤 5：提交**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_classifier.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_classifier.py
git commit -m "feat: add intelligence classifier"
```

## 任务 3：内容采集与每日简报生成

**涉及文件：**
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_ingest.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/daily_brief.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_ingest.py`

- [ ] **步骤 1：添加采集测试**

创建 `backend/tests/test_intelligence_ingest.py`：

```python
from datetime import date

from sqlmodel import Session, SQLModel, create_engine, select

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
```

- [ ] **步骤 2：运行测试并验证失败**

执行：

```bash
pytest tests/test_intelligence_ingest.py -v
```

预期：失败，因为采集和每日简报服务尚不存在。

- [ ] **步骤 3：添加采集服务**

创建 `backend/app/services/intelligence_ingest.py`：

```python
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
    for raw in raw_items:
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
```

- [ ] **步骤 4：添加每日简报服务**

创建 `backend/app/services/daily_brief.py`：

```python
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
```

- [ ] **步骤 5：运行采集测试**

执行：

```bash
pytest tests/test_intelligence_ingest.py -v
```

预期：全部通过。

- [ ] **步骤 6：提交**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_ingest.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/app/services/daily_brief.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_ingest.py
git commit -m "feat: ingest intelligence content and briefs"
```

## 任务 4：Markdown 扫描器

**涉及文件：**
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/markdown_scanner.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_markdown_scanner.py`

- [ ] **步骤 1：添加扫描器测试**

创建 `backend/tests/test_markdown_scanner.py`：

```python
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

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
```

- [ ] **步骤 2：运行扫描器测试并验证失败**

执行：

```bash
pytest tests/test_markdown_scanner.py -v
```

预期：失败，因为 `app.services.markdown_scanner` 不存在。

- [ ] **步骤 3：创建扫描器服务**

创建 `backend/app/services/markdown_scanner.py`：

```python
from __future__ import annotations

import hashlib
import re
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
        "updated_at": _mtime(path),
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
        frontmatter[key.strip()] = cleaned.lower() == "true" if cleaned.lower() in {"true", "false"} else cleaned
    return frontmatter, body


def _extract_title(body: str, path: Path) -> str:
    match = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else path.stem


def _mtime(path: Path):
    from datetime import datetime

    return datetime.fromtimestamp(path.stat().st_mtime)
```

- [ ] **步骤 4：运行扫描器测试**

执行：

```bash
pytest tests/test_markdown_scanner.py -v
```

预期：全部通过。

- [ ] **步骤 5：提交**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/backend/app/services/markdown_scanner.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_markdown_scanner.py
git commit -m "feat: scan markdown notes for intelligence site"
```

## 任务 5：公开情报 API

**涉及文件：**
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_search.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/app/routers/intelligence.py`
- 修改：`01-python-backend/code/fastapi-fullstack-demo/backend/app/routers/__init__.py`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_api.py`

- [ ] **步骤 1：添加 API 测试**

创建 `backend/tests/test_intelligence_api.py`：

```python
from fastapi.testclient import TestClient

from app.main import app


def test_public_home_endpoint_returns_seeded_shape():
    client = TestClient(app)

    response = client.get("/api/intelligence/home")

    assert response.status_code == 200
    payload = response.json()["data"]
    assert "latest_items" in payload
    assert "categories" in payload
    assert "brief" in payload


def test_public_categories_endpoint_lists_navigation_labels():
    client = TestClient(app)

    response = client.get("/api/intelligence/categories")

    assert response.status_code == 200
    labels = response.json()["data"]
    assert "Agent" in labels
    assert "RAG" in labels
```

- [ ] **步骤 2：运行 API 测试并验证失败**

执行：

```bash
pytest tests/test_intelligence_api.py -v
```

预期：失败，`/api/intelligence/home` 返回 404。

- [ ] **步骤 3：添加搜索服务**

创建 `backend/app/services/intelligence_search.py`：

```python
from __future__ import annotations

from sqlmodel import Session, select

from app.models.intelligence import AskResponse, Citation, ContentItem, LocalNote, PublishStatus, SearchResult


def search_public_knowledge(session: Session, query: str, limit: int = 10) -> list[SearchResult]:
    needle = query.lower().strip()
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
```

- [ ] **步骤 4：添加路由**

创建 `backend/app/routers/intelligence.py`：

```python
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
```

- [ ] **步骤 5：注册路由**

修改 `backend/app/routers/__init__.py`，导入并包含该路由。保持现有路由不变。最终设置应包含：

```python
from fastapi import FastAPI

from app.routers import auth, intelligence, items, posts, users


def setup_routers(app: FastAPI):
    app.include_router(auth.router, prefix="/api")
    app.include_router(users.router, prefix="/api")
    app.include_router(items.router, prefix="/api")
    app.include_router(posts.router, prefix="/api")
    app.include_router(intelligence.router, prefix="/api")
```

- [ ] **步骤 6：运行 API 测试**

执行：

```bash
pytest tests/test_intelligence_api.py -v
```

预期：全部通过。

- [ ] **步骤 7：提交**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/backend/app/services/intelligence_search.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/app/routers/intelligence.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/app/routers/__init__.py \
  01-python-backend/code/fastapi-fullstack-demo/backend/tests/test_intelligence_api.py
git commit -m "feat: expose public intelligence api"
```

## 任务 6：公开前端路由与 API 客户端

**涉及文件：**
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/types/intelligence.ts`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/api/intelligence.ts`
- 修改：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/router/index.ts`

- [ ] **步骤 1：添加前端类型**

创建 `frontend/src/types/intelligence.ts`：

```ts
export interface ContentItem {
  id: number;
  title: string;
  url: string;
  source_name: string;
  published_at: string | null;
  summary: string;
  key_points: string[];
  category: string;
  tags: string[];
  importance: number;
  reason: string;
}

export interface DailyBrief {
  id: number;
  brief_date: string;
  title: string;
  summary: string;
  sections: Array<{
    category: string;
    items: Array<{
      id: number;
      title: string;
      summary: string;
      url: string;
      tags: string[];
      importance: number;
      reason: string;
    }>;
  }>;
  generated_at: string;
}

export interface HomeData {
  latest_items: ContentItem[];
  brief: DailyBrief | null;
  categories: string[];
}

export interface SearchResult {
  result_type: string;
  id: number;
  title: string;
  summary: string;
  category: string;
  tags: string[];
  source: string;
}

export interface AskResponse {
  answer: string;
  refused: boolean;
  citations: Array<{
    source_type: string;
    id: number;
    title: string;
    excerpt: string;
  }>;
}
```

- [ ] **步骤 2：添加 API 客户端**

创建 `frontend/src/api/intelligence.ts`：

```ts
import api from '@/utils/api';
import type { AskResponse, ContentItem, DailyBrief, HomeData, SearchResult } from '@/types/intelligence';

export function fetchIntelligenceHome() {
  return api.get<HomeData>('/intelligence/home');
}

export function fetchCategories() {
  return api.get<string[]>('/intelligence/categories');
}

export function fetchContents(category?: string) {
  return api.get<ContentItem[]>('/intelligence/contents', {
    params: category ? { category } : {}
  });
}

export function fetchContentDetail(id: string | number) {
  return api.get<ContentItem | null>(`/intelligence/contents/${id}`);
}

export function fetchBriefs() {
  return api.get<DailyBrief[]>('/intelligence/briefs');
}

export function searchIntelligence(q: string) {
  return api.get<SearchResult[]>('/intelligence/search', { params: { q } });
}

export function askIntelligence(q: string) {
  return api.get<AskResponse>('/intelligence/ask', { params: { q } });
}
```

- [ ] **步骤 3：添加公开路由**

修改 `frontend/src/router/index.ts`，在认证布局路由之前添加以下路由：

```ts
  {
    path: '/',
    component: () => import('@/views/intelligence/PublicLayout.vue'),
    children: [
      {
        path: '',
        name: 'IntelligenceHome',
        component: () => import('@/views/intelligence/HomePage.vue')
      },
      {
        path: 'categories/:category',
        name: 'IntelligenceCategory',
        component: () => import('@/views/intelligence/CategoryPage.vue')
      },
      {
        path: 'contents/:id',
        name: 'IntelligenceContentDetail',
        component: () => import('@/views/intelligence/ContentDetailPage.vue')
      },
      {
        path: 'briefs',
        name: 'IntelligenceBriefs',
        component: () => import('@/views/intelligence/BriefsPage.vue')
      },
      {
        path: 'search',
        name: 'IntelligenceSearch',
        component: () => import('@/views/intelligence/SearchPage.vue')
      }
    ]
  },
```

将旧的根路径重定向从 `redirect: '/login'` 改为专用管理路径：

```ts
{
  path: '/admin',
  redirect: '/login'
},
```

- [ ] **步骤 4：运行前端类型检查**

在 `01-python-backend/code/fastapi-fullstack-demo/frontend` 下执行：

```bash
npm run build
```

预期：失败，因为引用的 Vue 页面尚不存在。这在任务 7 之前是预期的。

- [ ] **步骤 5：提交**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/frontend/src/types/intelligence.ts \
  01-python-backend/code/fastapi-fullstack-demo/frontend/src/api/intelligence.ts \
  01-python-backend/code/fastapi-fullstack-demo/frontend/src/router/index.ts
git commit -m "feat: add intelligence frontend routes"
```

## 任务 7：公开 Vue 页面

**涉及文件：**
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/PublicLayout.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/HomePage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/CategoryPage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/ContentDetailPage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/BriefsPage.vue`
- 创建：`01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence/SearchPage.vue`

- [ ] **步骤 1：创建公开布局**

创建 `frontend/src/views/intelligence/PublicLayout.vue`：

```vue
<template>
  <div class="public-shell">
    <header class="site-header">
      <RouterLink class="brand" to="/">AI Agent Intelligence</RouterLink>
      <nav class="nav">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/briefs">每日简报</RouterLink>
        <RouterLink to="/search">搜索问答</RouterLink>
        <RouterLink to="/login">管理入口</RouterLink>
      </nav>
    </header>
    <main class="site-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.public-shell {
  min-height: 100vh;
  background: #f6f8fb;
  color: #1f2937;
}

.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 18px 32px;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
}

.brand {
  color: #111827;
  font-size: 20px;
  font-weight: 700;
  text-decoration: none;
}

.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.nav a {
  color: #4b5563;
  text-decoration: none;
}

.nav a.router-link-active {
  color: #2563eb;
}

.site-main {
  max-width: 1120px;
  margin: 0 auto;
  padding: 28px 20px 48px;
}
</style>
```

- [ ] **步骤 2：创建首页**

创建 `frontend/src/views/intelligence/HomePage.vue`：

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { fetchIntelligenceHome } from '@/api/intelligence';
import type { HomeData } from '@/types/intelligence';

const data = ref<HomeData | null>(null);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  try {
    data.value = await fetchIntelligenceHome();
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="hero">
    <div>
      <p class="eyebrow">每日更新</p>
      <h1>AI Agent 开发者情报站</h1>
      <p class="subtitle">聚合 Agent、RAG、LLM API、MCP、开源项目和工程实践内容。</p>
    </div>
  </section>

  <el-skeleton v-if="loading" :rows="8" animated />

  <template v-else-if="data">
    <section v-if="data.brief" class="section">
      <h2>{{ data.brief.title }}</h2>
      <p>{{ data.brief.summary }}</p>
    </section>

    <section class="section">
      <h2>主题分类</h2>
      <div class="category-grid">
        <RouterLink v-for="category in data.categories" :key="category" :to="`/categories/${encodeURIComponent(category)}`">
          {{ category }}
        </RouterLink>
      </div>
    </section>

    <section class="section">
      <h2>最新内容</h2>
      <div class="item-list">
        <RouterLink v-for="item in data.latest_items" :key="item.id" class="item" :to="`/contents/${item.id}`">
          <span class="item-category">{{ item.category }}</span>
          <strong>{{ item.title }}</strong>
          <p>{{ item.summary }}</p>
        </RouterLink>
      </div>
    </section>
  </template>
</template>

<style scoped>
.hero {
  padding: 40px 0 28px;
}

.eyebrow {
  color: #2563eb;
  font-weight: 700;
}

h1 {
  margin: 0;
  font-size: 42px;
  line-height: 1.1;
}

.subtitle {
  max-width: 720px;
  color: #4b5563;
  font-size: 18px;
}

.section {
  margin-top: 28px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.category-grid a,
.item {
  display: block;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  color: #111827;
  text-decoration: none;
}

.item-list {
  display: grid;
  gap: 12px;
}

.item-category {
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
}

.item p {
  color: #4b5563;
}
</style>
```

- [ ] **步骤 3：创建分类页**

创建 `frontend/src/views/intelligence/CategoryPage.vue`：

```vue
<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { fetchContents } from '@/api/intelligence';
import type { ContentItem } from '@/types/intelligence';

const route = useRoute();
const items = ref<ContentItem[]>([]);

async function load() {
  items.value = await fetchContents(String(route.params.category));
}

onMounted(load);
watch(() => route.params.category, load);
</script>

<template>
  <section>
    <h1>{{ route.params.category }}</h1>
    <div class="item-list">
      <RouterLink v-for="item in items" :key="item.id" class="item" :to="`/contents/${item.id}`">
        <strong>{{ item.title }}</strong>
        <p>{{ item.summary }}</p>
        <span>{{ item.source_name }}</span>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.item-list {
  display: grid;
  gap: 12px;
}

.item {
  display: block;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  color: #111827;
  text-decoration: none;
}

.item p,
.item span {
  color: #4b5563;
}
</style>
```

- [ ] **步骤 4：创建内容详情页**

创建 `frontend/src/views/intelligence/ContentDetailPage.vue`：

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { fetchContentDetail } from '@/api/intelligence';
import type { ContentItem } from '@/types/intelligence';

const route = useRoute();
const item = ref<ContentItem | null>(null);

onMounted(async () => {
  item.value = await fetchContentDetail(String(route.params.id));
});
</script>

<template>
  <article v-if="item" class="detail">
    <p class="category">{{ item.category }}</p>
    <h1>{{ item.title }}</h1>
    <p class="summary">{{ item.summary }}</p>
    <div class="tags">
      <el-tag v-for="tag in item.tags" :key="tag">{{ tag }}</el-tag>
    </div>
    <h2>关键要点</h2>
    <ul>
      <li v-for="point in item.key_points" :key="point">{{ point }}</li>
    </ul>
    <p>{{ item.reason }}</p>
    <a :href="item.url" target="_blank" rel="noreferrer">打开原文</a>
  </article>
</template>

<style scoped>
.detail {
  max-width: 800px;
}

.category {
  color: #2563eb;
  font-weight: 700;
}

.summary {
  color: #374151;
  font-size: 18px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}
</style>
```

- [ ] **步骤 5：创建简报页**

创建 `frontend/src/views/intelligence/BriefsPage.vue`：

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { fetchBriefs } from '@/api/intelligence';
import type { DailyBrief } from '@/types/intelligence';

const briefs = ref<DailyBrief[]>([]);

onMounted(async () => {
  briefs.value = await fetchBriefs();
});
</script>

<template>
  <section>
    <h1>每日简报</h1>
    <article v-for="brief in briefs" :key="brief.id" class="brief">
      <h2>{{ brief.title }}</h2>
      <p>{{ brief.summary }}</p>
      <section v-for="section in brief.sections" :key="section.category">
        <h3>{{ section.category }}</h3>
        <ul>
          <li v-for="item in section.items" :key="item.id">{{ item.title }}</li>
        </ul>
      </section>
    </article>
  </section>
</template>

<style scoped>
.brief {
  margin-bottom: 20px;
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
}
</style>
```

- [ ] **步骤 6：创建搜索页**

创建 `frontend/src/views/intelligence/SearchPage.vue`：

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { askIntelligence, searchIntelligence } from '@/api/intelligence';
import type { AskResponse, SearchResult } from '@/types/intelligence';

const query = ref('');
const results = ref<SearchResult[]>([]);
const answer = ref<AskResponse | null>(null);

async function runSearch() {
  if (!query.value.trim()) return;
  results.value = await searchIntelligence(query.value);
  answer.value = await askIntelligence(query.value);
}
</script>

<template>
  <section>
    <h1>搜索与问答</h1>
    <div class="search-row">
      <el-input v-model="query" placeholder="搜索 Agent、RAG、MCP 等主题" @keyup.enter="runSearch" />
      <el-button type="primary" @click="runSearch">搜索</el-button>
    </div>

    <section v-if="answer" class="answer">
      <h2>回答</h2>
      <p>{{ answer.answer }}</p>
      <ul>
        <li v-for="citation in answer.citations" :key="`${citation.source_type}-${citation.id}`">
          {{ citation.title }}：{{ citation.excerpt }}
        </li>
      </ul>
    </section>

    <section class="results">
      <h2>搜索结果</h2>
      <div v-for="result in results" :key="`${result.result_type}-${result.id}`" class="result">
        <strong>{{ result.title }}</strong>
        <p>{{ result.summary }}</p>
      </div>
    </section>
  </section>
</template>

<style scoped>
.search-row {
  display: flex;
  gap: 12px;
}

.answer,
.result {
  margin-top: 18px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
}
</style>
```

- [ ] **步骤 7：运行前端构建**

执行：

```bash
npm run build
```

预期：构建通过。

- [ ] **步骤 8：提交**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/frontend/src/views/intelligence
git commit -m "feat: add public intelligence pages"
```

## 任务 8：文档与端到端验证

**涉及文件：**
- 修改：`01-python-backend/code/fastapi-fullstack-demo/README.md`

- [ ] **步骤 1：添加 README 说明**

追加到 `01-python-backend/code/fastapi-fullstack-demo/README.md`：

```markdown
## AI Agent 情报站

本演示项目包含一个公开的 AI Agent 情报站。

后端启动：

```bash
cd backend
python -m uvicorn app.main:app --reload
```

生成演示内容：

```bash
curl -X POST http://127.0.0.1:8000/api/intelligence/seed
curl http://127.0.0.1:8000/api/intelligence/home
```

前端启动：

```bash
cd frontend
npm install
npm run dev
```

打开 `http://127.0.0.1:5173/` 查看公开站点。

首个 MVP 版本默认将本地笔记设为私有，除非 Markdown 文件包含：

```yaml
---
publish: true
---
```
```

- [ ] **步骤 2：运行后端测试**

在 `backend` 下执行：

```bash
pytest tests/test_intelligence_classifier.py tests/test_intelligence_ingest.py tests/test_markdown_scanner.py tests/test_intelligence_api.py -v
```

预期：全部通过。

- [ ] **步骤 3：运行前端构建**

在 `frontend` 下执行：

```bash
npm run build
```

预期：构建通过。

- [ ] **步骤 4：手动验证 API seed 流程**

在 `backend` 下执行：

```bash
python -m uvicorn app.main:app --reload
```

在另一个终端中：

```bash
curl -X POST http://127.0.0.1:8000/api/intelligence/seed
curl http://127.0.0.1:8000/api/intelligence/home
curl "http://127.0.0.1:8000/api/intelligence/search?q=RAG"
curl "http://127.0.0.1:8000/api/intelligence/ask?q=RAG"
```

预期：

- Seed 响应中包含 `"created"`。
- Home 响应中包含 `"latest_items"`、`"categories"` 和 `"brief"`。
- 生成种子数据后，搜索响应至少包含一条 RAG 结果。
- Ask 响应中包含 `"citations"`。

- [ ] **步骤 5：提交文档**

```bash
git add 01-python-backend/code/fastapi-fullstack-demo/README.md
git commit -m "docs: document intelligence site workflow"
```

## 自查清单

Spec 覆盖情况：

- 公开首页：任务 5 API 和任务 7 首页。
- 分类导航：任务 1 枚举、任务 5 分类 API、任务 7 分类页。
- 内容详情：任务 1 Schema、任务 5 详情 API、任务 7 详情页。
- 每日简报：任务 3 服务、任务 5 简报 API、任务 7 简报页。
- 本地 Markdown 管理：任务 4 扫描器。
- 搜索与带引用 RAG：任务 5 搜索服务/API 和任务 7 搜索页。
- 公开/私有边界：任务 4 的 `publish: true` 处理和任务 5 的公开笔记过滤。
- 验证：任务 8 后端测试、前端构建和 API 冒烟检查。

实施决策：

- 首个公开站点使用 Vite，因为仓库中已包含 Vite Vue 应用。如果 SEO 成为优先级，Nuxt 可作为后续迁移方向。
- SQLite 兼容的 JSON 字段使 MVP 保持在本地友好的状态。PostgreSQL 和 pgvector 可以在核心流程跑通后引入。
- 首个分类器采用确定性实现，确保测试稳定且无需网络密钥。真正的 LLM 分类器可以在相同的 `ClassifiedContent` 契约背后替换服务实现。
