# 03. Prompt 与 RAG

## 学什么

本阶段把 Prompt 模板、Few-shot、上下文工程、Embedding、切分、检索、重排、引用、拒答和 RAG 评估整合成一个知识库问答包。

## 文档

- `docs/overview.md`：阶段总览。
- `docs/week-08.md` 到 `docs/week-11.md`：每日安排、作业和通关标准。
- `docs/resources.md`：资源索引。

## Code

- `code/simple_rag.py`：一个不依赖向量库的最小 RAG，用关键词检索演示“检索 -> 拼上下文 -> 回答”的链路。

## 验收标准

- 能解释 chunk、embedding、top_k、rerank、citation。
- 能让回答带来源。
- 能在检索不到证据时拒答。

