# Level 5-1 | 第 17 周：MCP 协议架构与核心概念

> 📡 **关卡名**：协议破译者 · MCP 架构理解
> 📅 **时间**：第 17 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 理解 MCP 协议的架构设计理念
- [ ] 掌握 MCP 三大原语（Resources / Tools / Prompts）
- [ ] 能使用现有 MCP Server

## 每日学习安排

### 周一（3h）· MCP 协议概念

- [ ] 学习：MCP 是什么——AI 应用的「USB-C 接口」
- [ ] 学习：MCP Host / Server / Client 三角色模型
- [ ] 学习：JSON-RPC 通信协议
- [ ] 前端衔接：MCP = 前端的微服务 API 网关

### 周二（3h）· 三大原语深入

- [ ] 学习：Resources 原语——暴露数据资源（类似 REST GET）
- [ ] 学习：Tools 原语——可执行的操作（类似 REST POST/PATCH）
- [ ] 学习：Prompts 原语——预定义 Prompt 模板
- [ ] 前端衔接：Resources = GET 接口；Tools = POST/PUT 接口；Prompts = 组件模板

### 周三（4h）· 传输方式

- [ ] 学习：stdio 传输（本地进程通信）
- [ ] 学习：SSE HTTP 传输（远程服务）
- [ ] 学习：Streamable HTTP 传输（最新标准）
- [ ] 实践：配置并使用一个本地 MCP Server

### 周四（4h）· 使用现有 MCP Server

- [ ] 实践：通过 Claude Desktop / VS Code 配置 MCP Server
- [ ] 实践：使用 `filesystem` MCP Server 进行文件操作
- [ ] 实践：使用 `github` MCP Server 操作 GitHub
- [ ] 体验：Agent 通过 MCP 扩展能力后的变化

### 周五（4h）· MCP Inspector 调试

- [ ] 学习：`npx @anthropic/mcp-inspector` 调试工具
- [ ] 实践：调试一个 MCP Server 的工具列表和调用
- [ ] 理解：MCP 协议的完整交互流程

## 知识点清单

- [ ] MCP Host / Server / Client 角色
- [ ] JSON-RPC 通信协议
- [ ] Resources 原语（数据暴露）
- [ ] Tools 原语（可执行操作）
- [ ] Prompts 原语（Prompt 模板）
- [ ] stdio 传输
- [ ] SSE HTTP 传输
- [ ] Streamable HTTP 传输
- [ ] MCP Inspector 调试工具
- [ ] 现有 MCP Server 生态

## 本周产出

- ✅ MCP 协议概念笔记
- ✅ 本地 MCP Server 配置和使用
- ✅ MCP Inspector 调试记录

## 通关标志

- [ ] 能画出 MCP 协议的 Host-Server-Client 架构图
- [ ] 能解释三大原语的用途和区别
- [ ] 能用 MCP Inspector 调试 Server
- [ ] 能配置并使用至少 2 个现有 MCP Server

## 资源链接

| 资源 | 链接 |
|------|------|
| MCP 协议规范 | https://modelcontextprotocol.io/ |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| MCP TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| MCP Inspector | https://modelcontextprotocol.io/docs/tools/inspector |

## 前端技能衔接提示

- MCP 协议 = 前端熟悉的 API Gateway 模式
- Resources 定义 = RESTful API 资源设计
- Tool inputSchema = OpenAPI / Zod schema
- MCP Server 开发 = Node.js Express 服务开发，思维一致
