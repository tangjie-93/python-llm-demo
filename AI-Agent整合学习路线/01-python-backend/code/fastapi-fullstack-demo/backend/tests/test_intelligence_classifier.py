from app.models.intelligence import IntelligenceCategory
from app.services.intelligence_classifier import classify_text


def test_intelligence_categories_are_fixed_navigation_labels():
    labels = [category.value for category in IntelligenceCategory]

    assert "Agent" in labels
    assert "RAG" in labels
    assert "LLM API" in labels
    assert "Deployment / Eval / Security" in labels


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
