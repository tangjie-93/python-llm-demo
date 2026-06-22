from dataclasses import dataclass


@dataclass
class Document:
    id: str
    title: str
    text: str


DOCS = [
    Document("fastapi", "FastAPI", "FastAPI 适合构建 Python API，支持类型标注、依赖注入和自动文档。"),
    Document("rag", "RAG", "RAG 通过检索外部知识补充上下文，降低幻觉，并让答案可以引用来源。"),
    Document("agent", "Agent", "Agent 会在目标驱动下选择工具、观察结果，并继续规划下一步。"),
]


def retrieve(query: str, top_k: int = 2) -> list[Document]:
    words = set(query.lower().split())

    def score(doc: Document) -> int:
        haystack = f"{doc.title} {doc.text}".lower()
        return sum(1 for word in words if word in haystack)

    ranked = sorted(DOCS, key=score, reverse=True)
    return [doc for doc in ranked if score(doc) > 0][:top_k]


def build_prompt(query: str, docs: list[Document]) -> str:
    context = "\n".join(f"[{doc.id}] {doc.text}" for doc in docs)
    return f"""基于以下资料回答问题。
如果资料不足，回答“资料不足，无法确认”。
回答末尾列出来源 id。

资料：
{context}

问题：{query}
"""


def answer(query: str) -> str:
    docs = retrieve(query)
    if not docs:
        return "资料不足，无法确认。"
    return build_prompt(query, docs)


if __name__ == "__main__":
    print(answer("RAG 为什么能减少幻觉"))

