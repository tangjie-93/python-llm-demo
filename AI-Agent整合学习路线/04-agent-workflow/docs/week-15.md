# Level 4-4 | 第 15 周：Multi-Agent 协作模式

> 🎭 **关卡名**：多面手联盟 · Multi-Agent 编排
> 📅 **时间**：第 15 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 理解 5 种 Multi-Agent 协作模式
- [ ] 能用 LangGraph 实现多 Agent 协作
- [ ] 了解 CrewAI / AutoGen 等多 Agent 框架

## 每日学习安排

### 周一（3h）· Multi-Agent 模式概览

- [ ] 学习：Router → Specialist 模式（路由分发）
- [ ] 学习：Sequential Pipeline 模式（链式处理）
- [ ] 学习：Debate / Review 模式（多 Agent 讨论评审）
- [ ] 学习：Hierarchical 模式（主 Agent 管理子 Agent）
- [ ] 学习：Parallel + Merge 模式（并行处理汇总）
- [ ] 前端衔接：Router → Specialist = 前端路由 + 页面组件

### 周二（4h）· LangGraph 多 Agent 实现

- [ ] 实践：用 LangGraph 构建 Router → Specialist 架构
- [ ] 实践：实现 Debate 模式（两个 Agent 互相评审对方的输出）
- [ ] 观察：多 Agent 之间的消息传递和状态同步

### 周三（4h）· CrewAI 入门

- [ ] 学习：CrewAI 的角色（Role）、任务（Task）、工具（Tool）定义
- [ ] 实践：用 CrewAI 构建一个「技术写作团队」
- [ ] 角色：研究员 Agent + 写手 Agent + 审校 Agent

### 周四（4h）· AutoGen 初探（了解）

- [ ] 了解：AutoGen 对话式 Agent 模式
- [ ] 了解：代码生成/执行 Agent
- [ ] 了解：Multi-Agent 对话管理
- [ ] 对比：CrewAI vs AutoGen vs LangGraph 的适用场景

### 周五（3h）· 综合实战

- [ ] 综合：实现「代码审查委员会」
- [ ] 功能：代码 → 安全审查 Agent + 性能审查 Agent + 风格审查 Agent → 汇总报告
- [ ] 练习：观察多 Agent 并行 vs 串行的性能差异

## 知识点清单

- [ ] Router → Specialist 模式
- [ ] Sequential Pipeline 模式
- [ ] Debate / Review 模式
- [ ] Hierarchical 模式
- [ ] Parallel + Merge 模式
- [ ] LangGraph 多 Agent 通信
- [ ] CrewAI 角色/任务/工具定义
- [ ] AutoGen 对话式多 Agent（了解）

## 本周产出

- ✅ LangGraph 多 Agent 协作系统
- ✅ CrewAI「技术写作团队」原型
- ✅ 代码审查委员会项目

## 通关标志

- [ ] 能画出 5 种 Multi-Agent 模式的架构图
- [ ] 能用 LangGraph 实现至少 2 种协作模式
- [ ] 能区分 CrewAI / AutoGen / LangGraph 的适用场景
- [ ] 能理解多 Agent 的通信开销和设计权衡

## 资源链接

| 资源 | 链接 |
|------|------|
| CrewAI 官方文档 | https://docs.crewai.com/ |
| AutoGen 文档 | https://microsoft.github.io/autogen/ |
| DeepLearning.AI: AI Agentic Design Patterns | https://www.deeplearning.ai/short-courses/ |

## 前端技能衔接提示

- Router → Specialist = 前端路由分发（一个路由 → 一个页面组件）
- Parallel + Merge = `Promise.all([a(), b(), c()])` 并发模式
- Hierarchical Mode = 父组件管理子组件
- Debate 模式 = Code Review 流程自动化
