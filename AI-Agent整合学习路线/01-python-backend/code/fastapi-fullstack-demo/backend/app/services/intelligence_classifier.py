from __future__ import annotations

import re

from app.models.intelligence import ClassifiedContent, IntelligenceCategory


CATEGORY_KEYWORDS: list[tuple[IntelligenceCategory, list[str]]] = [
    (IntelligenceCategory.AGENT, ["agent", "agents", "langgraph", "tool calling", "tool calls", "workflow", "multi-agent"]),
    (IntelligenceCategory.RAG, ["rag", "retrieval", "embedding", "embeddings", "vector", "rerank", "reranking", "citation", "citations", "pgvector", "qdrant"]),
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
    "Tool Calling": ["tool calling", "tool calls", "function calling", "tools"],
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
        return f"{title}: {clean[:180]}"
    return title


def _key_points(text: str) -> list[str]:
    sentences = [part.strip() for part in re.split(r"[。.!?]\s*", text) if part.strip()]
    return sentences[:3] if sentences else ["需要进一步阅读原文确认细节"]


def _reason(category: IntelligenceCategory, tags: list[str], importance: int) -> str:
    if category == IntelligenceCategory.UNCATEGORIZED:
        return "内容与当前 AI Agent 学习主题关联较弱。"
    tag_text = "、".join(tags) if tags else category.value
    return f"与 {tag_text} 相关，适合 AI Agent 开发者跟进，重要性 {importance}/5。"
