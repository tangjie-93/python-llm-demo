# Level 5-2 | 第 18 周：MCP Server 开发实战

> 🏭 **关卡名**：服务器铸造师 · MCP Server 开发
> 📅 **时间**：第 18 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 能用 Python MCP SDK 开发完整的 MCP Server
- [ ] 能实现 Resources / Tools / Prompts 三大原语
- [ ] 能处理参数验证和错误情况

## 每日学习安排

### 周一（4h）· Python MCP SDK 入门

- [ ] 学习：`mcp.server.Server` 创建服务器实例
- [ ] 学习：装饰器注册（`@server.list_resources()` 等）
- [ ] 学习：`stdio_server()` 启动
- [ ] 实践：创建最小 MCP Server（Hello World）

### 周二（4h）· Resources 实现

- [ ] 实现：`@server.list_resources()` 资源列表
- [ ] 实现：`@server.read_resource()` 资源读取
- [ ] 实现：URI 模板设计（`github://repos/{owner}/{repo}/issues`）
- [ ] 实践：实现一个「笔记资源」MCP Server

### 周三（4h）· Tools 实现

- [ ] 实现：`@server.list_tools()` 工具列表
- [ ] 实现：`@server.call_tool()` 工具执行
- [ ] 实现：Tool inputSchema JSON Schema 验证
- [ ] 实践：实现「搜索笔记」「创建笔记」「删除笔记」Tools

### 周四（3h）· Prompts 实现

- [ ] 实现：`@server.list_prompts()` Prompt 模板列表
- [ ] 实现：`@server.get_prompt()` Prompt 生成
- [ ] 实现：带参数的 Prompt 模板
- [ ] 实践：实现「代码审查模板」「发布说明模板」

### 周五（3h）· 错误处理 + 综合测试

- [ ] 实现：参数验证错误返回
- [ ] 实现：工具执行异常捕获
- [ ] 实现：未知工具/资源请求的友好提示
- [ ] 测试：用 MCP Inspector 完整调试

## 知识点清单

- [ ] Python MCP SDK 服务器创建
- [ ] `@server.list_resources()` / `@server.read_resource()`
- [ ] `@server.list_tools()` / `@server.call_tool()`
- [ ] `@server.list_prompts()` / `@server.get_prompt()`
- [ ] URI 模板设计
- [ ] inputSchema JSON Schema 定义
- [ ] 错误处理与友好提示
- [ ] MCP Inspector 调试

## 本周产出

- ✅ 一个功能完整的 MCP Server（三原语齐全）
- ✅ MCP Inspector 可调试
- ✅ 错误处理覆盖

## 通关标志

- [ ] 能独立创建 MCP Server 并注册三大原语
- [ ] 能实现 URI 参数解析
- [ ] 能处理工具调用错误
- [ ] 能通过 MCP Inspector 调试
