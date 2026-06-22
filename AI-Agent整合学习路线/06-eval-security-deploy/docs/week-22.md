# Level 6-3 | 第 22 周：安全加固 + 最终部署 + 交付

> 🛡️ **关卡名**：最终守护者 · 生产级交付
> 📅 **时间**：第 22 周 | ⏱️ **学时**：~20h

## 本周学习目标

- [ ] 能实施 Agent 系统的安全加固
- [ ] 能完成完整 CI/CD 部署流水线
- [ ] 能交付一个生产就绪的 Agent 系统

## 每日学习安排

### 周一（4h）· API Key 安全管理

- [ ] 学习：Pydantic `SecretStr` 敏感信息类型
- [ ] 学习：环境变量注入 API Key
- [ ] 学习：`.env` 文件安全管理（`.gitignore` + 示例文件）
- [ ] 学习：Key Rotation 策略
- [ ] 前端衔接：API Key 管理 = 前端环境变量管理（`.env.local`）

### 周二（4h）· 输入/输出安全

- [ ] 学习：Prompt 注入攻击与防护
- [ ] 学习：输入长度限制、控制字符过滤
- [ ] 学习：输出安全审查—防护代码执行
- [ ] 学习：Tool 参数校验防注入
- [ ] 前端衔接：输入过滤 = XSS 防护；输出过滤 = CSP 策略

### 周三（4h）· 速率限制 + 健康检查

- [ ] 学习：`slowapi` 请求频率限制
- [ ] 学习：`/health` 健康检查端点
- [ ] 学习：优雅关闭（Graceful Shutdown）
- [ ] 学习：日志规范（结构化日志）

### 周四（4h）· 最终部署

- [ ] 完成：GitHub Actions 完整流水线（test → build → deploy）
- [ ] 完成：`docker compose up` 一键部署验证
- [ ] 完成：健康检查、日志监控确认
- [ ] 完成：README 最终完善

### 周五（4h）· 最终验收 + 总结

- [ ] 对照阶段六验收标准全面自检
- [ ] 整体回顾 22 周学习历程
- [ ] 整理 GitHub 项目仓库（6 个实战项目）
- [ ] 撰写学习总结 / Blog 文章

## 知识点清单

- [ ] `SecretStr` 敏感信息管理
- [ ] API Key 安全最佳实践
- [ ] Prompt 注入防护
- [ ] 输入验证与净化
- [ ] 输出安全审查
- [ ] Tool 参数防注入
- [ ] `slowapi` 速率限制
- [ ] `/health` 健康检查
- [ ] 优雅关闭（Graceful Shutdown）
- [ ] 结构化日志
- [ ] GitHub Actions 完整 CI/CD

## 本周产出

- ✅ 安全加固后的 Agent 系统
- ✅ 完整 CI/CD 流水线
- ✅ `docker compose up` 一键部署
- ✅ 最终 README + 部署文档

## 通关标志

- [ ] `docker compose up` 一键启动所有服务
- [ ] 可在 LangSmith/LangFuse 后台看到调用链路
- [ ] GitHub Actions 流水线绿灯（测试 → 构建 → 部署）
- [ ] 对话 API 有频率限制保护
- [ ] API Key 通过环境变量注入，不出现于代码中
- [ ] 健康检查端点 `/health` 返回正常
- [ ] Token 用量日志包含每次请求的成本信息

## 资源链接

| 资源 | 链接 |
|------|------|
| OpenAI 安全最佳实践 | https://platform.openai.com/docs/guides/safety-best-practices |
| slowapi 文档 | https://slowapi.readthedocs.io/ |
| Docker Compose 生产指南 | https://docs.docker.com/compose/production/ |

## 前端技能衔接提示

- Prompt 注入防护 = XSS 防护思维
- 速率限制 = 前端防抖/节流 + API Rate Limiting
- 健康检查 = 前端 Service Worker Health Check
- 结构化日志 = 前端日志上报系统（Sentry）

---

> 🎉 **恭喜完成 22 周 AI Agent 开发学习路线！**
>
> 你已经从一个资深前端工程师，成长为掌握 Python 后端 + LLM 原理 + RAG 系统 + Multi-Agent 架构 + MCP 协议 + 生产部署的全栈 AI Agent 工程师。
>
> **下一步建议**：
> - 将项目打磨开源，建立个人技术品牌
> - 在掘金/知乎/Medium 撰写 AI Agent 系列文章
> - 参与开源社区（LangChain、LlamaIndex、MCP）
> - 关注 AI Agent 前沿方向：Web Agent、具身智能、Agent Swarm
