# FastAPI Backend Project

一个基于 FastAPI 框架的后端项目，使用 Poetry 管理依赖，提供完整的用户管理和物品管理功能。

## 1. 技术栈

- **框架**: FastAPI
- **包管理**: Poetry
- **数据库**: SQLite (SQLModel)
- **认证**: JWT
- **服务器**: Uvicorn
- **配置管理**: Pydantic Settings

## 2. 项目结构

```
backend/
├── app/                 # 应用主目录
│   ├── main.py          # 应用入口，创建 FastAPI 实例
│   ├── core/            # 核心配置
│   │   ├── config.py    # 配置管理（环境变量、应用设置）
│   │   └── database.py  # 数据库连接和会话管理
│   ├── models/          # 数据模型
│   │   ├── user.py      # 用户模型
│   │   └── item.py      # 物品模型
│   ├── routers/         # API 路由
│   │   ├── __init__.py  # 路由注册
│   │   ├── users.py     # 用户管理路由
│   │   ├── items.py     # 物品管理路由
│   │   └── auth.py      # 认证路由
│   └── middleware/      # 中间件
│       └── __init__.py  # 中间件注册
├── tests/               # 测试目录
├── pyproject.toml       # Poetry 配置文件
└── .env                 # 环境变量文件
```

## 3. 快速开始

### 3.1 安装依赖

```bash
# 进入后端目录
cd backend

# 使用 Poetry 安装依赖
poetry install
```

### 3.2 启动开发服务器

```bash
poetry run uvicorn app.main:app --reload
```

#### 3.2.1 命令解析
1. poetry run ：
   
   - poetry 是 Python 的包管理工具，用于管理项目依赖和虚拟环境
   - run 命令用于在 Poetry 创建的虚拟环境中执行指定的命令
   - 这确保了命令在正确的依赖环境中运行，避免与系统 Python 环境冲突
2. uvicorn ：
   
   - Uvicorn 是一个 ASGI（Asynchronous Server Gateway Interface）服务器
   - 专为运行异步 Python web 应用设计，是 FastAPI 的推荐服务器
   - 提供高性能的 HTTP 服务，支持 WebSocket 和异步请求处理
3. app.main:app ：
   
   - app.main ：指定应用所在的模块路径，即 app 目录下的 main.py 文件
   - :app ：指定应用实例的名称，即 main.py 文件中创建的 FastAPI 应用实例
   - 格式为 模块路径:应用实例名 ，告诉 Uvicorn 从哪里加载应用
4. --reload ：
   
   - 开发模式选项，启用热重载功能
   - 当代码文件发生变化时，Uvicorn 会自动重启服务器
   - 方便开发过程中实时查看代码修改效果，无需手动重启服务器

#### 3.2.2 适用场景
- **开发环境**：本地开发和调试，实时查看代码修改效果
- **测试环境**：快速验证代码变更
- **生产环境**：不建议使用 `--reload` 选项，应使用更稳定的启动方式

### 3.3 构建生产版本

```bash
poetry build
```

## 4. API 文档

服务启动后，可以访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 5. 主要功能

- ✅ 用户管理 (CRUD)
- ✅ 物品管理 (CRUD)
- ✅ JWT 认证
- ✅ 密码哈希加密
- ✅ SQLModel 数据库集成
- ✅ CORS 中间件支持
- ✅ 环境变量配置

## 6. 开发指南

### 6.1 代码风格

- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 遵循 PEP 8 代码规范

### 6.2 测试

```bash
# 运行测试
poetry run pytest
```

## 7. 部署

### 7.1 生产环境启动

```bash
# 不使用 --reload 选项
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 7.2 环境变量配置

在 `.env` 文件中配置以下环境变量：

```env
# 应用配置
APP_NAME=FastAPI Backend
APP_VERSION=1.0.0

# 数据库配置
DATABASE_URL=sqlite:///./fastapi.db

# JWT 配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 8. 贡献

欢迎提交 Issue 和 Pull Request！

## 9. 许可证

MIT License


