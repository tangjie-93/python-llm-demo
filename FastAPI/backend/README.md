# FastAPI Backend Project

FastAPI 后端项目，基于 Poetry 管理依赖。

## 项目结构

```
backend/
├── app/
│   ├── main.py              # 应用入口
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   └── database.py      # 数据库连接
│   ├── models/              # SQLModel 数据模型
│   │   ├── user.py
│   │   └── item.py
│   ├── routers/             # API 路由
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── items.py
│   │   └── auth.py
│   └── middleware/          # 中间件
│       └── __init__.py
├── tests/                   # 测试目录
├── pyproject.toml           # Poetry 配置
└── .env                     # 环境变量
```

## 快速开始

### 安装依赖

```bash
cd backend
poetry install
```

### 启动开发服务器

```bash
poetry run uvicorn app.main:app --reload
```

### 构建生产版本

```bash
poetry build
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## 主要功能

- [x] 用户管理 (CRUD)
- [x] 物品管理 (CRUD)
- [x] JWT 认证
- [x] 密码哈希
- [x] SQLModel 数据库集成
- [x] CORS 中间件
- [x] 环境变量配置
