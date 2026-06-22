# 阶段六：工程化与生产部署

> 🎯 **阶段总目标**：将 Agent 系统容器化部署上线，建立完整 CI/CD
> 📦 **阶段产出**：完整部署上线的 Agent 系统
> ⏱️ **阶段时长**：3 周 | **关卡数**：3

---

## 前置要求

- 完成阶段四和阶段五（具备完整 Agent 系统）
- 了解 Docker 基本概念（非必须，但建议）

## 学习目标

- 掌握 Agent 系统的可观测性方案
- 能进行 Token 成本分析和优化
- 能对 Agent 系统进行性能优化
- 能将 Agent 系统容器化并部署上线
- 能搭建 CI/CD 流水线

## 关卡列表

| 关卡 | 周次 | 关卡名 | BOSS | EXP |
|------|------|--------|------|-----|
| [Level 6-1](./week-20.md) | 第 20 周 | 📊 全视之眼 · 可观测性 | 💸 成本恶龙 CostDragon | ⭐⭐⭐ |
| [Level 6-2](./week-21.md) | 第 21 周 | 🐳 容器大师 · Docker 编排 | 🐋 鲸鱼巨兽 DockerWhale | ⭐⭐⭐ |
| [Level 6-3](./week-22.md) | 第 22 周 | 🛡️ 最终守护者 · 生产级交付 | 🛡️ 运维守卫 DevOpsGuardian | ⭐⭐⭐⭐ |

### 区域 BOSS

**🛡️ 运维守卫 DevOpsGuardian（最终 BOSS）** — 守护生产环境的终极守卫：安全+限流+健康检查+优雅关闭。

## 阶段验收标准

- [ ] 能用 Docker Compose 编排 Agent 完整服务栈
- [ ] 能搭建 Agent 可观测性系统
- [ ] 能在可观测性平台查看 Trace 和 Token 用量
- [ ] 能编写 GitHub Actions 工作流
- [ ] 理解 API Key 管理和输入/输出安全
- [ ] 完成实战项目全部验收标准

## 核心知识点一览

1. **Agent 可观测性**：LangSmith、LangFuse、Weights & Biases、OpenTelemetry
2. **核心观测指标**：Token 使用量、延迟、LLM 调用次数、工具调用成功率、用户反馈、成本
3. **成本控制**：Token 计数（tiktoken）、多模型成本对比、预算管理、ModelRouter、Prompt 缓存、语义缓存
4. **性能优化**：流式输出优化、并发调用、HTTP 连接池、模型降级策略
5. **Docker 容器化**：Dockerfile、Docker Compose 多服务编排、多阶段构建
6. **CI/CD**：GitHub Actions（test → build → deploy）
7. **安全**：API Key 管理（SecretStr）、Prompt 注入防护、输入/输出过滤、速率限制、健康检查、优雅关闭

## 前端技能迁移要点

- Docker = 前端项目容器化——技能直接迁移
- CI/CD = GitHub Actions 部署前端项目——经验完全复用
- 性能优化 = 前端性能优化（bundle size / lazy load / caching）——方法论一致
- 安全经验 = CSP / XSS 防护

## 实战项目

将阶段四的 `agent-support` 系统完整部署上线：

- Docker Compose 一键启动完整环境
- LangSmith / LangFuse 追踪每次对话
- GitHub Actions CI/CD 自动测试和部署
- Token 用量日报 + 成本监控
- API Key 安全管理和请求频率限制
- 健康检查 + 优雅关闭
