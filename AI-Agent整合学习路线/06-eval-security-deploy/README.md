# 06. 评测、安全与部署

## 学什么

本阶段把 Golden Dataset、检索评测、答案评测、工具调用评测、Tracing、成本控制、Prompt Injection、防护、PII 脱敏、Docker、CI/CD 和部署检查清单整合成一个生产化包。

## 文档

- `docs/overview.md`：工程化与部署总览。
- `docs/week-20.md` 到 `docs/week-22.md`：每日安排、作业和通关标准。
- `docs/05-评测Tracing与质量工程.md`：评测与 tracing 专题。
- `docs/resources.md`：资源索引。

## Code

- `code/eval_harness.py`：一个最小评测框架，包含 golden case、答案命中、拒答和注入检测。

## 验收标准

- 能为 Agent 建立最小评测集。
- 能记录每一步工具调用和成本。
- 能对高风险输入做拦截、降权或人工审批。

