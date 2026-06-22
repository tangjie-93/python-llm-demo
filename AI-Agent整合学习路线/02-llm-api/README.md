# 02. LLM API 基础

## 学什么

本阶段把 Token、上下文窗口、模型参数、结构化输出、流式输出、多轮对话、错误处理和多模型适配整合成一个 LLM 调用基础包。

## 文档

- `docs/overview.md`：阶段总览。
- `docs/week-05.md` 到 `docs/week-07.md`：每日安排、作业和通关标准。
- `docs/resources.md`：资源索引。

## Code

- `code/llm_client.py`：一个最小 LLM Client，封装消息、参数、环境变量和 JSON 输出。

## 验收标准

- 能解释 temperature、max tokens、system prompt、上下文截断。
- 能把一次性调用改成多轮对话。
- 能处理 API key、超时、重试和结构化输出失败。

