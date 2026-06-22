# 阶段五：MCP 协议与工具生态

> 🎯 **阶段总目标**：理解 MCP 协议，能开发自定义 MCP Server
> 📦 **阶段产出**：`github-mcp-server` — GitHub Agent MCP Server
> ⏱️ **阶段时长**：3 周 | **关卡数**：3

---

## 前置要求

- 完成阶段四（Agent 框架）
- 理解 Tool / Function Calling

## 学习目标

- 理解 MCP 协议的架构和设计理念
- 能开发自定义 MCP Server
- 能集成现有 MCP Server 到 Agent
- 理解 MCP 生态的应用场景

## 关卡列表

| 关卡 | 周次 | 关卡名 | BOSS | EXP |
|------|------|--------|------|-----|
| [Level 5-1](./week-17.md) | 第 17 周 | 📡 协议破译者 · MCP 架构 | 🔌 三头接口兽 TripleInterfaceBeast | ⭐⭐ |
| [Level 5-2](./week-18.md) | 第 18 周 | 🏭 服务器铸造师 · MCP Server 开发 | ⚒️ 锻造巨锤 ForgeHammer | ⭐⭐⭐ |
| [Level 5-3](./week-19.md) | 第 19 周 | 🔌 万物互联 · 项目交付 | 🏗️ 协议巨人 MCPColossus | ⭐⭐⭐⭐ |

### 区域 BOSS

**🏗️ 协议巨人 MCPColossus** — 守护标准化工具接口的巨像。需要将 MCP Server 集成到 Agent 才能击败。

## 阶段验收标准

- [ ] 能解释 MCP 协议的架构和三大原语（Resources/Tools/Prompts）
- [ ] 能独立开发 MCP Server 并本地调试
- [ ] 能将 MCP Server 集成到 Agent 中
- [ ] 了解常用 MCP Server 生态并知道如何选型
- [ ] 完成实战项目 `github-mcp-server` 全部验收标准

## 核心知识点一览

1. **MCP 协议架构**：Host / Server / Client 三角色，JSON-RPC 通信，stdio / SSE HTTP / Streamable HTTP 传输
2. **三大原语**：Resources（数据资源）、Tools（可执行操作）、Prompts（Prompt 模板）
3. **MCP Server 开发**：Python MCP SDK，装饰器注册，参数验证，错误处理
4. **MCP 生态**：filesystem、github、postgres、puppeteer、brave-search、fetch、memory、sequential-thinking
5. **MCP Server 集成到 LangGraph**：ClientSession、Tool 转换

## 前端技能迁移要点

- MCP 协议 = 前端的微服务 API 网关
- Resources 定义 = RESTful API 资源设计
- Tool inputSchema = OpenAPI / Zod schema
- MCP Server 开发 = Node.js Express 服务开发

## 实战项目

**`github-mcp-server`** — 为 Agent 提供 GitHub 操作能力的 MCP Server

- **Resources**：Repository Issues、Pull Requests、Files
- **Tools**：创建 Issue、搜索代码、列出文件、获取 PR 信息
- **Prompts**：代码审查模板、发布说明模板
