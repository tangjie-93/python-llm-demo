# FastAPI Backend 项目结构与功能梳理

本文档梳理 `backend/app` 的目录结构、分层职责和已经实现的后端功能。

## 项目概览

这是一个基于 FastAPI 的后端应用，使用 SQLModel 管理数据库模型和查询，默认连接 PostgreSQL。

当前已实现：

- FastAPI 应用入口与生命周期管理
- SQLModel 数据库模型与自动建表
- JWT 登录认证
- Refresh Token + HttpOnly Cookie
- 用户 CRUD
- 物品 CRUD
- 博客文章 CRUD
- 标签管理
- 文章与标签多对多关联
- CORS 中间件
- 安全响应头
- 全局异常处理
- 统一 API 响应格式

## 目录结构

```text
backend/app/
  main.py
  core/
    config.py
    database.py
    response.py
  routers/
    __init__.py
    auth.py
    auth.md
    users.py
    items.py
    posts.py
  models/
    __init__.py
    user.py
    item.py
    post.py
    tag.py
    response.py
  schemas/
    __init__.py
    auth.py
  services/
    __init__.py
    auth_service.py
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
| 服务层 | `services/` | 放认证相关业务逻辑，例如登录失败追踪、字段校验 |
| 依赖注入 | `dependencies/` | 定义需要被路由复用的依赖，例如当前登录用户 |
| 工具函数 | `utils/` | 密码哈希、JWT、Refresh Token 等底层工具 |
| 中间件 | `middleware/` | CORS 和安全响应头 |
| 异常处理 | `exceptions/` | 全局异常处理器 |

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
/api/auth   认证接口
/api/users  用户接口
/api/items  物品接口
/api/posts  文章与标签接口
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
- 更新用户
- 删除用户
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

注意：用户 CRUD 接口当前没有管理员权限控制，更像教学或后台基础接口。

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
- 创建物品
- 更新物品
- 删除物品
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
- 创建文章
- 更新文章
- 删除文章
- 发布文章
- 取消发布文章
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

注意：创建文章时 `author_id` 当前由请求参数传入，代码注释也说明实际项目中应从 JWT Token 中获取当前用户。

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
- 给文章添加标签
- 从文章移除标签
- 标签名唯一校验
- 文章和标签多对多关联

标签核心字段：

```text
id
name
description
created_at
```

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

## 目前看到的实现风险

### 1. `auth.refresh` 和 `auth.logout` 可能有响应构造 bug

`success_response()` 当前返回 `ApiResponse` 模型对象，但 `auth.py` 的 `refresh` 和 `logout` 中有类似写法：

```python
success_response(... )["detail"]
```

这会把 Pydantic 模型当字典使用，运行时可能报错。

更一致的写法应类似登录接口：

```python
response_data = success_response(...).model_dump_json()
response = Response(content=response_data, media_type="application/json")
```

### 2. 权限控制还不完整

当前 `users`、`items`、`posts` 的大部分 CRUD 接口没有严格依赖当前登录用户。

例如：

- 用户 CRUD 没有管理员权限限制。
- 创建文章时 `author_id` 由请求参数传入，而不是从 JWT 当前用户中读取。
- 物品 CRUD 没有限制只能由 owner 操作。

### 3. 登录失败追踪使用内存存储

`LoginAttemptTracker` 使用进程内内存保存失败次数。

这适合本地开发或教学，但生产环境存在问题：

- 服务重启后记录丢失。
- 多进程 / 多实例之间不共享状态。

生产环境更适合使用 Redis。

### 4. 自动建表适合开发，不适合正式迁移

当前启动时调用：

```python
SQLModel.metadata.create_all(engine)
```

这适合开发阶段快速建表。生产环境建议使用 Alembic 管理数据库迁移。

### 5. 默认配置不适合生产

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
- 中间件
- 异常处理
- 统一响应

如果继续演进，建议优先处理：

1. 修复 `refresh/logout` 响应构造问题。
2. 把文章作者改为从当前登录用户读取。
3. 给用户、物品、文章接口补权限控制。
4. 用 Alembic 替代启动自动建表。
5. 把登录失败追踪迁移到 Redis。
6. 清理 `__pycache__`，避免缓存文件进入项目结构。
