# Level 5-3 | 第 19 周：项目实战 + MCP 集成到 Agent

> 🔌 **关卡名**：万物互联 · MCP 项目交付
> 📅 **时间**：第 19 周 | ⏱️ **学时**：~20h

## 本周学习目标

- [ ] 完成阶段五实战项目 `github-mcp-server`
- [ ] 能将 MCP Server 集成到 LangGraph Agent
- [ ] 理解 MCP 生态的未来趋势

## 每日学习安排

### 周一（4h）· GitHub MCP Server - Resources

- [ ] 实现：`github://repos/{owner}/{repo}/issues` 资源
- [ ] 实现：`github://repos/{owner}/{repo}/pulls` 资源
- [ ] 实现：`github://repos/{owner}/{repo}/files` 资源

### 周二（4h）· GitHub MCP Server - Tools

- [ ] 实现：`create_issue` 创建 Issue
- [ ] 实现：`search_code` 代码搜索
- [ ] 实现：`list_repo_files` 文件列表
- [ ] 实现（可选）：`merge_pull_request` 合并 PR

### 周三（4h）· GitHub MCP Server - Prompts + 配置

- [ ] 实现：`code_review` Prompt 模板
- [ ] 实现：`release_notes` Prompt 模板
- [ ] 实现：环境变量配置 GitHub Token
- [ ] 实现：配置文件管理

### 周四（4h）· MCP 集成到 LangGraph

- [ ] 学习：`mcp.ClientSession` 客户端连接
- [ ] 学习：MCP Tools → LangChain Tools 转换
- [ ] 实践：在 Agent 工作流中集成 MCP Server
- [ ] 体验：Agent 通过 MCP 操作 GitHub

### 周五（4h）· 文档 + 验收

- [ ] 编写 README（安装、配置、使用）
- [ ] 用 MCP Inspector 完整测试
- [ ] 对照验收标准自检

## 本周产出

- ✅ **`github-mcp-server`** 完整的 GitHub MCP Server
- ✅ 3 Resources + 4 Tools + 2 Prompts
- ✅ MCP Server 集成到 Agent
- ✅ README 文档

## 通关标志

- [ ] MCP Server 可通过 MCP Inspector 调试
- [ ] `list_tools` 返回至少 3 个功能完整的工具
- [ ] `list_resources` 返回至少 2 个数据资源
- [ ] `list_prompts` 返回至少 2 个 Prompt 模板
- [ ] 每个工具处理参数验证和错误捕获
- [ ] 支持通过环境变量配置 GitHub Token
- [ ] README 包含安装配置说明

## 资源链接

| 资源 | 链接 |
|------|------|
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| Awesome MCP Servers | https://github.com/punkpeye/awesome-mcp-servers |
| Anthropic MCP Servers | https://github.com/anthropics/anthropic-tools |
| GitHub REST API | https://docs.github.com/en/rest |

## 前端技能衔接提示

- MCP Server 开发 = Node.js API 服务开发
- Tool 接口设计 = REST API 端点设计
- MCP Server 集成 = 前端 SDK 集成（类似接入微信 SDK）
- TypeScript MCP SDK 也可用，作为前端开发者有额外优势
