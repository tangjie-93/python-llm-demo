# 阶段四：AI Agent 框架

> 🎯 **阶段总目标**：掌握 Agent 设计模式，能构建多 Agent 协作系统
> 📦 **阶段产出**：`agent-support` — 多 Agent 智能客服系统
> ⏱️ **阶段时长**：5 周 | **关卡数**：5（最大阶段）

---

## 前置要求

- 完成阶段三（RAG）
- 理解 LLM API 和 Prompt Engineering

## 学习目标

- 理解 Agent 的核心设计模式
- 掌握 Tool Calling / Function Calling 机制
- 能使用 LangGraph 构建复杂 Agent 工作流
- 理解 Multi-Agent 协作模式

## 关卡列表

| 关卡 | 周次 | 关卡名 | BOSS | EXP |
|------|------|--------|------|-----|
| [Level 4-1](./week-12.md) | 第 12 周 | 🤖 智能体觉醒 · Agent 基础 | 🔄 ReAct 循环巨兽 ReActCyclops | ⭐⭐⭐ |
| [Level 4-2](./week-13.md) | 第 13 周 | 🔀 图灵绘师 · LangGraph 工作流 | 🌳 图灵织网者 GraphWeaver | ⭐⭐⭐⭐ |
| [Level 4-3](./week-14.md) | 第 14 周 | 🛠️ 装备大师 · Tool 与 Memory | 💭 记忆吞噬者 MemoryDevourer | ⭐⭐⭐ |
| [Level 4-4](./week-15.md) | 第 15 周 | 🎭 多面手联盟 · Multi-Agent | 👥 五头协调兽 PentCoordinator | ⭐⭐⭐⭐ |
| [Level 4-5](./week-16.md) | 第 16 周 | 🏢 客服帝国 · 项目交付 | 🐲 状态机巨龙 StateMachineDragon | ⭐⭐⭐⭐⭐ |

### 区域 BOSS

**🐲 状态机巨龙 StateMachineDragon** — 管理 Agent 复杂状态流转的远古巨龙。4 个 Agent 的复杂状态流转，是整个路线中最核心的挑战。

## 阶段验收标准

- [ ] 能解释 ReAct 循环的工作原理
- [ ] 能设计和实现 Tool / Function Calling
- [ ] 能用 LangGraph 构建至少 3 个节点的 Agent 工作流
- [ ] 理解 Checkpoint 和 Human-in-the-loop 的作用
- [ ] 能设计 Multi-Agent 系统架构
- [ ] 完成实战项目 `agent-support` 全部验收标准

## 核心知识点一览

1. **Agent 核心概念**：Agent = LLM + Tools + Memory + Planning
2. **ReAct 模式**：Thought → Action → Observation 循环
3. **Function Calling / Tool Definition**：OpenAI 格式，JSON Schema 参数定义
4. **主流框架**：LangGraph（重点推荐）、LangChain Agent、LlamaIndex Agent、CrewAI、AutoGen、Agno、Dify/Coze
5. **LangGraph 深入**：StateGraph、节点/边/条件分支、Checkpoint、Human-in-the-Loop
6. **Multi-Agent 协作**：Router→Specialist、Sequential Pipeline、Debate/Review、Hierarchical、Parallel+Merge

## 前端技能迁移要点

- Agent Node = React Component（独立处理单元）
- StateGraph = Vue Router 路由配置 + Vuex Store 合体
- Conditional Edge = Vue Router `beforeEach` 导航守卫
- Checkpoint = Redux Persist / Pinia 持久化插件
- Multi-Agent Router→Specialist = 前端路由分发

## 实战项目

**`agent-support`** — 多 Agent 协作的智能客服系统

- **Router Agent**：意图识别（知识查询 / 工单创建 / 一般问答）
- **Knowledge Agent**：搜索内部知识库，回答技术问题
- **Ticket Agent**：自动创建和管理工单
- **Summarize Agent**：对话结束后生成摘要
- 支持多轮对话、Checkpoint 恢复
