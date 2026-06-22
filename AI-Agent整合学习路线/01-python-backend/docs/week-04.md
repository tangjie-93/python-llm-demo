# Level 1-4 | 第 4 周：数据库操作 + 阶段一收尾

> 🗄️ **关卡名**：数据掌控者 · SQLAlchemy 与项目交付
> 📅 **时间**：第 4 周 | ⏱️ **学时**：~20h

## 本周学习目标

- [ ] 能用 SQLAlchemy 2.0 进行数据库 CRUD 操作
- [ ] 能使用 Alembic 进行数据库迁移
- [ ] 完成阶段一实战项目 `dev-note-api` 并写 README

## 每日学习安排

### 周一（4h）· SQLAlchemy ORM 入门

- [ ] 学习：SQLAlchemy 2.0 `DeclarativeBase` 声明式模型
- [ ] 学习：`Mapped` / `mapped_column` 字段映射
- [ ] 学习：关系定义（`relationship`、`ForeignKey`）
- [ ] 实践：定义 User、Note、Tag 三张表的 ORM 模型
- [ ] 前端衔接：ORM 模型定义 = TS `interface` + DB Schema 声明，类型安全

### 周二（4h）· CRUD 操作 + Session

- [ ] 学习：`AsyncSession` 异步数据库会话
- [ ] 学习：`select()` / `insert()` / `update()` / `delete()` 语句
- [ ] 学习：`where()` 条件过滤、`order_by()` 排序、`limit()` 分页
- [ ] 练习：为 Note 模型编写完整的 CRUD 操作函数

### 周三（4h）· Alembic 数据库迁移

- [ ] 学习：Alembic 安装与初始化（`alembic init`）
- [ ] 学习：自动生成迁移脚本（`alembic revision --autogenerate`）
- [ ] 学习：执行迁移（`alembic upgrade head`）、回滚（`alembic downgrade`）
- [ ] 实践：为项目配置 Alembic，创建第一次迁移
- [ ] 前端衔接：Alembic = Prisma Migrate / TypeORM Migration

### 周四（4h）· FastAPI + SQLAlchemy 整合

- [ ] 整合前三周知识：将 FastAPI 路由连接到 SQLAlchemy
- [ ] 实现 FastAPI Depends 中注入数据库 Session
- [ ] 实现：笔记 CRUD、用户注册/登录（带密码哈希）
- [ ] 添加笔记分类和标签功能

### 周五（4h）· 项目收尾 + 验收

- [ ] 编写完整的 pytest 测试（至少 12 个）
- [ ] 编写 README（项目说明、安装步骤、API 文档链接）
- [ ] 用 `uv sync` 确认依赖完整可复现
- [ ] 对照验收标准自检

## 知识点清单

- [ ] SQLAlchemy 2.0 `DeclarativeBase` 声明基类
- [ ] `Mapped` + `mapped_column` 字段映射
- [ ] `relationship()` 外键关系定义
- [ ] `select()` / `insert()` / `update()` / `delete()` CRUD
- [ ] `where()` / `order_by()` / `limit()` 查询过滤
- [ ] `AsyncSession` 异步会话
- [ ] `async with` 上下文管理
- [ ] Alembic 数据库版本迁移
- [ ] FastAPI `Depends(get_db)` 数据库会话注入
- [ ] `passlib` 密码哈希
- [ ] `python-jose` JWT 签发与验证
- [ ] `pytest-asyncio` 异步测试

## 练习 / 作业

```python
# 作业：完成 dev-note-api 全部功能
# 验收标准清单：
# [ ] GET /docs 可访问 Swagger UI 文档
# [ ] 支持笔记创建、查询列表、单条查询、更新、删除
# [ ] JWT 认证保护 API 端点
# [ ] 请求/响应数据通过 Pydantic 验证
# [ ] 至少 12 个单元测试通过
# [ ] 使用 uv 管理依赖
# [ ] 包含 README 文档
```

## 本周产出

- ✅ **`dev-note-api`** 完整可运行的 FastAPI 项目
- ✅ 数据库 ORM 模型 + Alembic 迁移
- ✅ 12+ 个 pytest 测试全绿
- ✅ README 文档齐全

## 通关标志

- [ ] 能独立用 SQLAlchemy 定义 ORM 模型和关系
- [ ] 能编写复杂的过滤和分页查询
- [ ] 能使用 Alembic 管理数据库版本
- [ ] 能将 FastAPI + SQLAlchemy + JWT 整合为完整服务
- [ ] 项目 README 清晰可读，他人可直接部署运行

## 资源链接

| 资源 | 链接 |
|------|------|
| SQLAlchemy 2.0 官方文档 | https://docs.sqlalchemy.org/en/20/ |
| Alembic 文档 | https://alembic.sqlalchemy.org/ |
| passlib 文档 | https://passlib.readthedocs.io/ |
| python-jose (JWT) | https://python-jose.readthedocs.io/ |

## 前端技能衔接提示

- ORM 的类型安全查询 = Prisma 的 TypeScript 类型推断，体验一致
- Alembic migration = Prisma Migrate / TypeORM Migration，概念几乎一样
- 数据库 Session 注入 = 数据库连接池 middleware
- 密码哈希 = 前端 bcrypt 概念直接复用
