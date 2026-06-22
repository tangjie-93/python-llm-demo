# 阶段一：Python 后端基础

> 🎯 **阶段总目标**：用 Python 独立完成一个 FastAPI RESTful API 服务
> 📦 **阶段产出**：`dev-note-api` — 开发者笔记管理 API
> ⏱️ **阶段时长**：4 周 | **关卡数**：4

---

## 前置要求

- 精通 TypeScript/JavaScript
- 熟悉 Node.js 后端开发
- 了解 HTTP 协议与 RESTful 设计

## 学习目标

- 能用 Python 编写中等复杂度的后端服务
- 理解 Python 异步编程模型
- 能用 FastAPI 搭建带文档的 API 服务
- 掌握 SQLAlchemy 进行数据库操作

## 关卡列表

| 关卡 | 周次 | 关卡名 | BOSS | EXP |
|------|------|--------|------|-----|
| [Level 1-1](./week-01.md) | 第 1 周 | 🐍 蛇语觉醒 · Python 基础语法 | 🐍 缩进巨蟒 IndentationError | ⭐⭐ |
| [Level 1-2](./week-02.md) | 第 2 周 | 📦 包管理器大师 · 工程化入门 | 🌀 依赖地狱犬 DependencyHell | ⭐⭐ |
| [Level 1-3](./week-03.md) | 第 3 周 | 🚀 疾风 API · FastAPI 精通 | ⚡ 路由九头蛇 RouteHydra | ⭐⭐⭐ |
| [Level 1-4](./week-04.md) | 第 4 周 | 🗄️ 数据掌控者 · SQLAlchemy 与项目 | 🐉 异步魔龙 asyncio | ⭐⭐⭐ |

### 区域 BOSS

**🐉 异步魔龙 asyncio** — 拥有强大的并发吐息，需用协程护盾抵挡。多表联查攻击 + 迁移诅咒。

## 阶段验收标准

- [ ] 能独立用 FastAPI 搭建完整 API 服务
- [ ] 理解 Python 装饰器、上下文管理器、async/await
- [ ] 能使用 Pydantic 进行复杂数据校验
- [ ] 能使用 SQLAlchemy 进行基本 CRUD 操作
- [ ] 完成实战项目 `dev-note-api` 全部验收标准

## 核心知识点一览

1. **Python 语法速成（对比 TypeScript）**：类型系统、控制流、函数、类、模块
2. **包管理与虚拟环境**：`uv`、`pyproject.toml`、`.venv`
3. **FastAPI 框架**：路由、Pydantic 数据模型、依赖注入、中间件
4. **数据库操作**：SQLAlchemy 2.0 ORM、Alembic 迁移
5. **Python 异步编程**：asyncio、httpx 异步客户端

## 前端技能迁移要点

- TS 类型思维 → Python type hints + Pydantic，几乎零学习曲线
- Express/Koa 中间件 → FastAPI Depends 依赖注入
- async/await 异步编程模型基本一致
- RESTful API 设计经验 100% 复用

## 实战项目

**`dev-note-api`** — 开发者笔记管理 API

- 笔记的 CRUD 操作
- 用户注册/登录（JWT 认证）
- 笔记分类与标签
- 自动生成的 Swagger 文档
