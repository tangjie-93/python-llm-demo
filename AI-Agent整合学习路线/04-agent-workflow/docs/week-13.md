# Level 4-2 | 第 13 周：LangGraph 入门 — StateGraph 与工作流

> 🔀 **关卡名**：图灵绘师 · LangGraph 工作流
> 📅 **时间**：第 13 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 理解 LangGraph 的 StateGraph 概念
- [ ] 能定义节点、边、条件分支
- [ ] 能构建至少 3 个节点的 Agent 工作流

## 每日学习安排

### 周一（3h）· LangGraph 核心概念

- [ ] 学习：StateGraph 的工作原理（状态机 + 图计算）
- [ ] 学习：State 定义（TypedDict + Annotated reducer）
- [ ] 学习：Node（处理节点）、Edge（连接）、Conditional Edge（条件路由）
- [ ] 前端衔接：StateGraph = Vue Router 路由配置 + Vuex Store 合体

### 周二（3h）· 构建第一个 Agent 图

- [ ] 实践：定义 3 个节点的简单 Agent（Analyze → Process → Output）
- [ ] 学习：`workflow.add_node()` / `set_entry_point()` / `add_edge()`
- [ ] 学习：图编译（`workflow.compile()`）
- [ ] 学习：图执行（`app.invoke()` / `app.stream()`）

### 周三（4h）· 条件分支与路由

- [ ] 学习：`add_conditional_edges()` 条件路由
- [ ] 学习：路由函数设计（根据 State 决定下一步）
- [ ] 实践：实现意图路由 Agent（Router → Knowledge / Ticket / General）
- [ ] 前端衔接：条件路由 = Vue Router 的导航守卫 `beforeEach`

### 周四（4h）· Checkpoint 与持久化

- [ ] 学习：Checkpoint 概念——工作流执行状态快照
- [ ] 学习：`MemorySaver` 内存 Checkpointer
- [ ] 学习：`SqliteSaver` 数据库 Checkpointer
- [ ] 学习：中断恢复（`thread_id` 恢复之前的对话状态）
- [ ] 前端衔接：Checkpoint = Redux Persist / Vuex 持久化插件

### 周五（4h）· Human-in-the-Loop

- [ ] 学习：人机协同概念——Agent 不确定时请求人类决策
- [ ] 学习：`interrupt()` 中断机制
- [ ] 学习：人工审批流程
- [ ] 实践：在 Tool 调用前加人工确认环节

## 知识点清单

- [ ] LangGraph `StateGraph`
- [ ] State 定义（TypedDict + Annotated reducer）
- [ ] Node 处理节点
- [ ] Edge / Conditional Edge
- [ ] `workflow.compile()`
- [ ] `app.invoke()` / `app.stream()`
- [ ] Checkpoint 状态快照
- [ ] `MemorySaver` / `SqliteSaver`
- [ ] `thread_id` 对话恢复
- [ ] `interrupt()` 人机协同
- [ ] Human-in-the-Loop 模式

## 练习 / 作业

```python
# 作业 1：三节点工作流
# 用 LangGraph 构建：Analyze → Process → Output 三个节点的工作流

# 作业 2：意图路由系统
# 实现 Router → Knowledge/Ticket/General 条件路由
# Router 节点分析意图，决定分发给哪个专业节点

# 作业 3：带 Checkpoint 的对话系统
# 实现对话中断后可通过 thread_id 恢复，体验「断点续聊」
```

## 本周产出

- ✅ 三节点 LangGraph 工作流
- ✅ 带条件路由的意图分发系统
- ✅ 带 Checkpoint 恢复的对话系统

## 通关标志

- [ ] 能用 StateGraph 定义有状态的 Agent 工作流
- [ ] 能实现条件分支路由
- [ ] 能使用 Checkpoint 持久化和恢复状态
- [ ] 能实现简单的 Human-in-the-Loop 审批

## 资源链接

| 资源 | 链接 |
|------|------|
| LangGraph 官方文档 | https://langchain-ai.github.io/langgraph/ |
| LangGraph 示例仓库 | https://github.com/langchain-ai/langgraph/tree/main/examples |
| DeepLearning.AI: LangGraph 课程 | https://www.deeplearning.ai/short-courses/ |

## 前端技能衔接提示

- StateGraph Node = React Component（独立的处理单元）
- Conditional Edge = Vue Router `beforeEach` 导航守卫
- State Reducer = Redux Reducer / Vuex Mutation
- Checkpoint = Redux Persist / Pinia 持久化插件
- Human-in-the-Loop = 表单提交前的确认对话框
