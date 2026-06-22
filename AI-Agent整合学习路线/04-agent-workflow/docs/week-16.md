# Level 4-5 | 第 16 周：项目实战 — 多 Agent 智能客服系统

> 🏢 **关卡名**：客服帝国 · 多 Agent 系统交付
> 📅 **时间**：第 16 周 | ⏱️ **学时**：~20h

## 本周学习目标

- [ ] 完成阶段四实战项目 `agent-support`
- [ ] 实现 4 个专业 Agent 的协作系统
- [ ] 理解生产级 Multi-Agent 系统的设计考量

## 每日学习安排

### 周一（4h）· 系统架构设计

- [ ] 设计：Router Agent → Knowledge/Ticket/General → Summarize 架构
- [ ] 设计：AgentState 数据结构
- [ ] 设计：知识库集成方案

### 周二（4h）· 各 Agent 节点实现

- [ ] 实现：Router Agent（意图识别）
- [ ] 实现：Knowledge Agent（RAG 知识检索）
- [ ] 实现：Ticket Agent（工单创建/查询）

### 周三（4h）· 系统整合

- [ ] 实现：Summarize Agent（对话摘要）
- [ ] 整合：LangGraph 工作流 + 条件路由
- [ ] 实现：Checkpoint 持久化

### 周四（4h）· 前端 + 接口

- [ ] 实现：FastAPI + WebSocket 对外接口
- [ ] 实现：简单前端对话界面（可选）
- [ ] 实现：对话历史查询 API

### 周五（4h）· 测试 + 文档

- [ ] 编写多场景测试用例
- [ ] 编写 README + 架构文档
- [ ] 对照验收标准自检

## 本周产出

- ✅ **`agent-support`** 多 Agent 智能客服系统
- ✅ Router / Knowledge / Ticket / Summarize 四个 Agent
- ✅ LangGraph 工作流 + Checkpoint
- ✅ FastAPI + WebSocket 接口

## 通关标志

- [ ] Router Agent 能正确识别至少 3 种意图类型
- [ ] Knowledge Agent 能从知识库中检索并给出准确回答
- [ ] Ticket Agent 能创建工单记录到数据库
- [ ] Summarize Agent 能生成包含关键信息的对话摘要
- [ ] 系统支持 Checkpoint 恢复中断的对话
- [ ] 多轮对话上下文不丢失
- [ ] 答案明确标注信息来源（知识库 / AI 生成 / 工单编号）
