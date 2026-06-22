# Level 6-2 | 第 21 周：Docker 容器化与性能优化

> 🐳 **关卡名**：容器大师 · Docker 编排
> 📅 **时间**：第 21 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 能用 Docker 容器化 Agent 服务
- [ ] 能用 Docker Compose 编排多服务栈
- [ ] 能进行 Agent 性能优化

## 每日学习安排

### 周一（3h）· Docker 基础

- [ ] 学习：Docker 核心概念（Image / Container / Volume / Network）
- [ ] 学习：Dockerfile 编写（FROM / WORKDIR / COPY / RUN / CMD）
- [ ] 实践：为 FastAPI 服务编写 Dockerfile
- [ ] 前端衔接：Docker = 前端构建产物容器化（你已熟悉的部署方式）

### 周二（4h）· Docker Compose 多服务

- [ ] 学习：Docker Compose 文件结构
- [ ] 学习：服务依赖（`depends_on` + `condition: service_healthy`）
- [ ] 实践：编排 FastAPI + PostgreSQL + Qdrant + LangFuse 四服务
- [ ] 实践：`docker compose up` 一键启动

### 周三（4h）· 性能优化

- [ ] 学习：流式输出优化—降低首字节延迟
- [ ] 学习：`asyncio.gather` 并发调用多个 LLM
- [ ] 学习：HTTP 连接池复用
- [ ] 实践：对 Agent 系统进行性能分析，找到瓶颈

### 周四（4h）· 多阶段构建 + 镜像优化

- [ ] 学习：多阶段 Docker 构建（减小镜像体积）
- [ ] 学习：`uv` 在 Docker 中的最佳实践
- [ ] 学习：非 root 用户安全实践
- [ ] 实践：优化 Dockerfile（用小体积 base image）

### 周五（3h）· CI/CD 起步

- [ ] 了解：GitHub Actions 工作流结构
- [ ] 实践：编写 `test` job（安装依赖、运行测试）
- [ ] 实践：编写 `build` job（Docker 构建）
- [ ] 了解：`deploy` job（SSH 部署）

## 知识点清单

- [ ] Docker Image / Container / Volume
- [ ] Dockerfile 编写
- [ ] Docker Compose 多服务编排
- [ ] 多阶段 Docker 构建
- [ ] 非 root 用户安全
- [ ] 流式输出性能优化
- [ ] `asyncio.gather` 并发优化
- [ ] HTTP 连接池
- [ ] GitHub Actions 基本结构

## 本周产出

- ✅ Dockerfile + docker-compose.yml
- ✅ 一键启动的完整服务栈
- ✅ GitHub Actions CI 工作流

## 通关标志

- [ ] 能编写生产级 Dockerfile
- [ ] 能用 Docker Compose 编排 3+ 个服务
- [ ] 能实施至少 3 种性能优化策略
- [ ] 能编写 GitHub Actions 测试流水线

## 资源链接

| 资源 | 链接 |
|------|------|
| Docker 官方文档 | https://docs.docker.com/ |
| Docker Compose 文档 | https://docs.docker.com/compose/ |
| GitHub Actions 文档 | https://docs.github.com/en/actions |
| uv in Docker | https://docs.astral.sh/uv/guides/integration/docker/ |

## 前端技能衔接提示

- Docker = 前端项目容器化（Dockerize Next.js App）— 技能直接迁移
- Docker Compose = 前端微前端编排
- 性能优化 = 前端性能优化（bundle size / lazy load / caching）— 方法论一致
- CI/CD = GitHub Actions 部署前端项目 — 经验完全复用
