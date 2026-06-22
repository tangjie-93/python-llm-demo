# 阶段二：LLM 基础原理

> 🎯 **阶段总目标**：理解 LLM 工作原理，能调用 API 开发应用
> 📦 **阶段产出**：`ai-code-review` — AI 驱动的代码审查 CLI 工具
> ⏱️ **阶段时长**：3 周 | **关卡数**：3

---

## 前置要求

- 完成阶段一（Python 基础）
- 了解 HTTP 和 API 调用

## 学习目标

- 理解 LLM 的核心工作原理（无需深入数学推导）
- 了解主流模型生态及选型策略
- 能熟练调用 OpenAI 及兼容 API
- 能开发调用 LLM 的 CLI 应用

## 关卡列表

| 关卡 | 周次 | 关卡名 | BOSS | EXP |
|------|------|--------|------|-----|
| [Level 2-1](./week-05.md) | 第 5 周 | 🧠 思维觉醒 · 理解大模型 | 🔮 注意力之眼 AttentionEye | ⭐⭐ |
| [Level 2-2](./week-06.md) | 第 6 周 | 🔌 API 召唤师 · 调用大模型 | 🌡️ 温控元素使 TemperatureElemental | ⭐⭐ |
| [Level 2-3](./week-07.md) | 第 7 周 | 🔍 代码审查官 · AI CR 工具 | 👁️ Token 守护者 TokenGuardian | ⭐⭐⭐ |

### 区域 BOSS

**👁️ Token 守护者 TokenGuardian** — 守护 LLM 核心秘密的神殿守卫。用 AI 守护代码质量是最终考验。

## 阶段验收标准

- [ ] 能解释 Token、Embedding、Attention 的基本概念
- [ ] 了解至少 3 个主流模型的适用场景
- [ ] 能使用 OpenAI SDK 进行对话和流式调用
- [ ] 理解 temperature、system prompt 对输出的影响
- [ ] 完成实战项目 `ai-code-review` 全部验收标准

## 核心知识点一览

1. **LLM 核心概念**：Token、Tokenizer、Embedding、Transformer、Attention、Context Window、Temperature
2. **主流模型生态**：GPT-4o、Claude、Gemini、DeepSeek、Qwen、Llama
3. **OpenAI 兼容 API**：对话调用、流式输出、关键参数调优
4. **模型选型决策树**

## 前端技能迁移要点

- Token 分片 ≈ 字符串 encode/decode
- Embedding 降维可视化 ≈ 前端数据可视化
- Attention 权重分配 ≈ CSS 优先级计算
- Context Window 限制 ≈ LocalStorage 5MB 限制

## 实战项目

**`ai-code-review`** — AI 驱动的代码审查命令行工具

- 接收文件路径或代码片段作为输入
- 分析代码质量、安全问题、性能隐患
- 输出结构化的审查报告（Markdown 格式）
- 支持多种编程语言
- 支持 Git diff 模式
