# FastAPI Backend 项目结构与功能梳理

本文档梳理 `backend` 的目录结构、分层职责和已经实现的后端功能。

## 项目概览

这是一个基于 FastAPI 的后端应用，使用 SQLModel 管理数据库模型和查询，默认连接 PostgreSQL。

当前已实现：

- FastAPI 应用入口与生命周期管理
- SQLModel 数据库模型与自动建表
- JWT 登录认证
- Refresh Token + HttpOnly Cookie
- 用户 CRUD（含权限控制）
- 物品 CRUD（含所有权校验）
- 博客文章 CRUD（含作者校验）
- 标签管理
- 文章与标签多对多关联
- BackgroundTasks 后台任务
- CORS 中间件
- 安全响应头
- 全局异常处理
- 统一 API 响应格式
- pytest 测试体系（47 个测试用例）
- Alembic 数据库迁移
- uv 包管理配置
- asyncio / httpx 异步并发示例
- SQLAlchemy 2.0 原生 ORM 示例

## 目录结构

```text
backend/
  main.py                          # FastAPI 应用入口
  pyproject.toml                   # Poetry 项目配置
  requirements.txt                 # pip 依赖清单
  alembic.ini                      # Alembic 迁移配置
  .env.example                     # 环境变量示例

  alembic/
    env.py                         # 迁移环境（含 SQLModel metadata）
    script.py.mako                 # 迁移脚本模板
    versions/                      # 迁移版本文件

  uv-setup/
    pyproject.toml                 # uv PEP 621 标准配置
    README.md                      # uv 迁移指南

  examples/
    async_demo.py                  # asyncio + httpx 异步并发 4 个示例
    sqlalchemy_native_demo.py      # SQLAlchemy 2.0 原生 ORM 对比

  tests/
    conftest.py                    # pytest fixtures（engine/session/client/auth）
    test_auth.py                   # 认证接口测试（8 个）
    test_users.py                  # 用户 CRUD 测试（8 个）
    test_items.py                  # 物品 CRUD 测试（8 个）
    test_posts.py                  # 文章/标签测试（12 个）
    test_background_tasks.py       # 后台任务测试（1 个）
    test_intelligence_api.py       # 情报 API 测试
    test_intelligence_classifier.py
    test_intelligence_ingest.py
    test_markdown_scanner.py

  app/
    __init__.py
    main.py

    core/
      __init__.py
      config.py
      database.py
      response.py

    routers/
      __init__.py
      auth.py
      users.py
      items.py
      posts.py
      tasks.py                    # BackgroundTasks 后台任务路由
      intelligence.py

    models/
      __init__.py
      user.py
      item.py
      post.py
      tag.py
      response.py
      intelligence.py

    schemas/
      __init__.py
      auth.py

    services/
      __init__.py
      auth_service.py
      daily_brief.py
      intelligence_classifier.py
      intelligence_ingest.py
      intelligence_search.py
      markdown_scanner.py

    dependencies/
      __init__.py
      auth.py

    utils/
      __init__.py
      auth.py

    middleware/
      __init__.py

    exceptions/
      __init__.py
```

## 分层职责

| 层级 | 目录 / 文件 | 职责 |
| --- | --- | --- |
| 应用入口 | `main.py` | 创建 FastAPI 实例，配置生命周期、中间件、异常处理和路由 |
| 核心配置 | `core/config.py` | 使用 Pydantic Settings 管理应用配置 |
| 数据库 | `core/database.py` | 创建数据库 engine、Session 依赖、自动建表 |
| 统一响应 | `core/response.py`、`models/response.py` | 定义 `ApiResponse`、成功响应和错误响应 |
| 路由层 | `routers/` | 定义 HTTP API 接口 |
| 数据模型 | `models/` | 定义 SQLModel 表模型、请求模型和响应模型 |
| 请求 DTO | `schemas/` | 定义认证相关 Pydantic DTO |
| 服务层 | `services/` | 业务逻辑，例如登录失败追踪、情报分类、Markdown 扫描 |
| 依赖注入 | `dependencies/` | 定义需要被路由复用的依赖，例如当前登录用户 |
| 工具函数 | `utils/` | 密码哈希、JWT、Refresh Token 等底层工具 |
| 中间件 | `middleware/` | CORS 和安全响应头 |
| 异常处理 | `exceptions/` | 全局异常处理器 |
| 测试 | `tests/` | pytest 测试用例，覆盖认证、CRUD、权限、后台任务 |
| 迁移 | `alembic/` | Alembic 数据库迁移管理 |
| 示例 | `examples/` | asyncio 并发、SQLAlchemy 2.0 原生写法等学习参考 |
| 包管理 | `uv-setup/` | uv 包管理器的 PEP 621 配置和迁移指南 |

## 应用入口

入口文件是 `app/main.py`。

启动时执行：

1. 创建 FastAPI 应用实例。
2. 读取 `settings` 配置。
3. 注册 CORS 和安全响应头中间件。
4. 注册全局异常处理器。
5. 注册业务路由。
6. 在 lifespan 启动阶段调用 `create_db_and_tables()` 自动创建数据库表。

基础接口：

```text
GET /        欢迎信息
GET /health  健康检查
```

## 配置与数据库

配置文件：`app/core/config.py`

主要配置项：

- `APP_NAME`
- `VERSION`
- `DESCRIPTION`
- `DEBUG`
- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_DAYS`
- `CORS_ORIGINS`

默认数据库连接：

```text
postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_db
```

数据库文件：`app/core/database.py`

已实现：

- 创建 SQLModel engine
- 自动导入模型
- `SQLModel.metadata.create_all(engine)` 自动建表
- `get_session()` 提供请求级数据库会话

## 路由注册

路由集中注册在 `app/routers/__init__.py`。

```text
/api/auth    认证接口
/api/users   用户接口
/api/items   物品接口
/api/posts   文章与标签接口
/api/tasks   后台任务演示接口
```

## 认证功能

相关文件：

- `app/routers/auth.py`
- `app/services/auth_service.py`
- `app/utils/auth.py`
- `app/dependencies/auth.py`
- `app/schemas/auth.py`

接口：

```text
POST /api/auth/login
POST /api/auth/register
GET  /api/auth/me
POST /api/auth/refresh
POST /api/auth/logout
```

已实现能力：

- 用户注册
- 用户登录
- 当前用户信息查询
- Access Token 生成
- Refresh Token 生成
- Refresh Token 存入 HttpOnly Cookie
- 使用 Refresh Token 刷新 Access Token
- 登出时清理 Refresh Token
- 密码哈希存储
- 用户名格式校验
- 邮箱格式校验
- 密码强度校验
- 登录失败追踪
- 5 次失败后锁定 1 小时

认证方式：

```text
OAuth2PasswordRequestForm + JWT Access Token + Refresh Token Cookie
```

密码哈希算法：

```text
pbkdf2_sha256
```

Access Token 默认有效期：

```text
15 分钟
```

Refresh Token 默认有效期：

```text
7 天
```

## 用户管理功能

相关文件：

- `app/routers/users.py`
- `app/models/user.py`

接口：

```text
GET    /api/users/
GET    /api/users/{user_id}
POST   /api/users/
PUT    /api/users/{user_id}
DELETE /api/users/{user_id}
```

已实现能力：

- 获取用户列表
- 获取单个用户
- 创建用户
- 更新用户（仅超级管理员或用户本人可操作）
- 删除用户（仅超级管理员或用户本人可操作）
- 创建和更新用户时进行密码哈希
- 响应模型隐藏敏感字段

用户核心字段：

```text
id
username
email
hashed_password
full_name
is_active
is_superuser
refresh_token
token_expires_at
```

## 物品管理功能

相关文件：

- `app/routers/items.py`
- `app/models/item.py`

接口：

```text
GET    /api/items/
GET    /api/items/{item_id}
POST   /api/items/
PUT    /api/items/{item_id}
DELETE /api/items/{item_id}
```

已实现能力：

- 获取物品列表
- 获取单个物品
- 创建物品（`owner_id` 从 JWT 当前用户自动获取）
- 更新物品（仅物品所有者或超级管理员可操作）
- 删除物品（仅物品所有者或超级管理员可操作）
- 列表接口支持 `skip` / `limit` 分页
- 物品通过 `owner_id` 关联用户
- 列表响应会补充 owner 信息

物品核心字段：

```text
id
title
description
price
tax
owner_id
```

## 博客文章功能

相关文件：

- `app/routers/posts.py`
- `app/models/post.py`
- `app/models/tag.py`

文章接口：

```text
GET    /api/posts/
GET    /api/posts/{post_id}
POST   /api/posts/
PATCH  /api/posts/{post_id}
DELETE /api/posts/{post_id}
POST   /api/posts/{post_id}/publish
POST   /api/posts/{post_id}/unpublish
```

已实现能力：

- 获取文章列表
- 获取文章详情
- 创建文章（`author_id` 从 JWT 当前用户自动获取）
- 更新文章（仅文章作者或超级管理员可操作）
- 删除文章（仅文章作者或超级管理员可操作）
- 发布文章（仅文章作者或超级管理员可操作）
- 取消发布文章（仅文章作者或超级管理员可操作）
- 查看详情时增加浏览量
- 按发布时间倒序列表展示
- 支持分页
- 支持按发布状态筛选
- 支持按作者筛选
- 支持按标签筛选

文章核心字段：

```text
id
title
content
summary
author_id
is_published
view_count
created_at
updated_at
```

## 标签功能

标签接口：

```text
GET    /api/posts/tags/
GET    /api/posts/tags/{tag_id}
POST   /api/posts/tags/
PATCH  /api/posts/tags/{tag_id}
DELETE /api/posts/tags/{tag_id}
POST   /api/posts/{post_id}/tags/{tag_id}
DELETE /api/posts/{post_id}/tags/{tag_id}
```

已实现能力：

- 获取标签列表
- 获取标签详情
- 创建标签
- 更新标签
- 删除标签
- 给文章添加标签（仅文章作者或超级管理员可操作）
- 从文章移除标签（仅文章作者或超级管理员可操作）
- 标签名唯一校验
- 文章和标签多对多关联

标签核心字段：

```text
id
name
description
created_at
```

## 后台任务（BackgroundTasks）

相关文件：

- `app/routers/tasks.py`

接口：

```text
POST /api/tasks/send-notification   发送通知演示
POST /api/tasks/audit               操作审计日志演示
```

已实现能力：

- 使用 FastAPI `BackgroundTasks` 在请求返回后执行异步任务
- 模拟发送通知（写日志）
- 模拟审计日志记录（带时间戳和操作人）

用途说明：BackgroundTasks 适合发邮件、写审计日志、异步通知等不需要立即返回结果的场景。

## 数据关系

```text
User 1 --- N Post
User 1 --- N Item
Post N --- N Tag
```

对应模型：

- `User.posts`：用户和文章一对多
- `Item.owner_id`：物品和用户多对一
- `Post.tags`：文章和标签多对多
- `PostTagLink`：文章标签关联表

## 权限控制总览

| 模块 | 操作 | 权限规则 |
| --- | --- | --- |
| users | PUT / DELETE | 仅超级管理员或用户本人 |
| items | POST | owner_id 从 JWT 自动获取（请求体忽略） |
| items | PUT / DELETE | 仅物品所有者或超级管理员 |
| posts | PATCH / DELETE / publish / unpublish | 仅文章作者或超级管理员 |
| posts | 添加/移除标签 | 仅文章作者或超级管理员 |
| posts | POST (create) | author_id 从 JWT 自动获取 |

权限校验由 `dependencies/auth.py` 中的 `get_current_user` 依赖注入实现，各路由通过 `current_user: User = Depends(get_current_user)` 获取当前用户后比对 `id` 或 `is_superuser`。

## 中间件

文件：`app/middleware/__init__.py`

已实现：

- CORS
- 安全响应头

CORS 允许的前端来源来自配置项 `CORS_ORIGINS`，默认包括：

```text
http://localhost:5173
http://localhost:5174
http://localhost:3000
```

安全响应头：

```text
X-Frame-Options
X-Content-Type-Options
X-XSS-Protection
Strict-Transport-Security
Content-Security-Policy
Referrer-Policy
```

## 异常处理

文件：`app/exceptions/__init__.py`

已处理异常类型：

- `HTTPException`
- `RequestValidationError`
- `ValidationError`
- 普通 `Exception`

异常响应会通过 `error_response()` 统一为类似格式：

```json
{
  "success": false,
  "message": "错误信息",
  "data": null
}
```

## 统一响应格式

文件：

- `app/models/response.py`
- `app/core/response.py`

统一响应模型：

```python
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
```

成功响应：

```json
{
  "success": true,
  "message": "操作成功",
  "data": {}
}
```

失败响应：

```json
{
  "success": false,
  "message": "操作失败",
  "data": null
}
```

## 测试体系

文件：`tests/` 目录，共 47 个测试用例。

### 测试基础设施

- `conftest.py`：使用 SQLite 内存数据库 + `StaticPool` + 表清理策略
- `client` fixture：共享 `db_session`，确保 fixture 创建的测试数据在端点中可见
- `auth_headers` fixture：普通用户 `testuser` 的认证头
- `admin_headers` fixture：超级管理员 `admin` 的认证头

### 测试覆盖

| 测试文件 | 用例数 | 覆盖内容 |
| --- | --- | --- |
| `test_auth.py` | 8 | 注册、登录、密码错误、用户不存在、me、无 token、登出 |
| `test_users.py` | 8 | 列表、详情、创建、更新（含越权）、删除（含越权） |
| `test_items.py` | 8 | 列表、创建、详情、更新（含越权）、删除（含越权） |
| `test_posts.py` | 12 | 列表、创建、详情、更新（含越权）、发布、取消、删除（含越权）、标签 |
| `test_background_tasks.py` | 1 | 后台通知任务 |

运行方式：

```bash
cd backend
PYTHONPATH=. pytest tests/ -v
```

## Alembic 数据库迁移

相关文件：

- `alembic.ini` — Alembic 配置文件
- `alembic/env.py` — 迁移环境（已集成 SQLModel metadata，支持自动生成）
- `alembic/script.py.mako` — 迁移脚本模板
- `alembic/versions/` — 迁移版本存放目录

常用命令：

```bash
# 生成迁移脚本（自动检测模型变化）
alembic revision --autogenerate -m "描述"

# 升级到最新版本
alembic upgrade head

# 回滚一个版本
alembic downgrade -1

# 查看当前版本
alembic current
```

注意：当前启动时仍使用 `SQLModel.metadata.create_all(engine)` 自动建表（适合开发），生产环境应使用 `alembic upgrade head`。

## 配套学习资源

### asyncio / httpx 异步并发

文件：`examples/async_demo.py`

包含 4 个从基础到进阶的示例：

1. 基本异步 HTTP 请求
2. `asyncio.gather` 并发请求多个 API
3. 带超时和重试的异步客户端
4. `asyncio.Semaphore` 并发限制

### SQLAlchemy 2.0 原生 ORM

文件：`examples/sqlalchemy_native_demo.py`

演示纯 SQLAlchemy 2.0 的 `DeclarativeBase`、`Mapped`、`mapped_column`、`relationship` 等新式声明语法，并与 SQLModel 进行对比。

### uv 包管理

文件：`uv-setup/`

- `pyproject.toml`：PEP 621 标准的 uv 项目配置
- `README.md`：uv 迁移指南，含 pip/poetry 对比和 npm/pnpm 前端类比

## 仍存在的实现风险

### 1. 登录失败追踪使用内存存储

`LoginAttemptTracker` 使用进程内内存保存失败次数。

这适合本地开发或教学，但生产环境存在问题：

- 服务重启后记录丢失。
- 多进程 / 多实例之间不共享状态。

生产环境更适合使用 Redis。

### 2. 自动建表适合开发，不适合正式迁移

当前启动时调用：

```python
SQLModel.metadata.create_all(engine)
```

这适合开发阶段快速建表。生产环境建议使用 Alembic 管理数据库迁移（已配置就绪，需切换启动方式）。

### 3. 默认配置不适合生产

当前默认配置包括：

- `DEBUG=True`
- 固定 `SECRET_KEY`
- refresh cookie `secure=False`
- 默认数据库账号密码

生产环境需要通过环境变量覆盖。

## 总体评价

这个项目是一个功能较完整的 FastAPI 教学/练习型后端，已经覆盖后端工程常见模块：

- 应用初始化
- 配置管理
- 数据库连接
- ORM 模型
- 路由拆分
- 用户认证
- JWT
- Refresh Token
- CRUD
- 多对多关系
- 权限控制（JWT 注入 + 所有权/角色校验）
- BackgroundTasks 后台任务
- 中间件
- 异常处理
- 统一响应
- pytest 测试体系
- Alembic 迁移
- asyncio/httpx 异步并发
- SQLAlchemy 2.0 原生 ORM
- uv 包管理

如果继续演进，建议优先处理：

1. 把登录失败追踪迁移到 Redis。
2. 生产环境切换为 Alembic 启动迁移。
3. 清理 `__pycache__`，避免缓存文件进入项目结构。
4. 前端 `create_post` 调用去掉 `owner_id` 参数（后端已忽略）。
