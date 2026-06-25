"""
FastAPI 后端应用包

这是整个后端应用的根包。

包结构说明：
├── app/
│   ├── __init__.py          # 应用根包初始化
│   ├── main.py              # 应用入口
│   ├── core/                # 核心模块
│   │   ├── config.py        # 配置管理
│   │   └── database.py     # 数据库连接
│   ├── models/              # 数据模型
│   │   ├── user.py          # 用户模型
│   │   └── item.py          # 物品模型
│   ├── routers/             # 路由模块
│   │   ├── auth.py          # 认证路由
│   │   ├── users.py         # 用户管理路由
│   │   └── items.py         # 物品管理路由
│   ├── middleware/          # 中间件
│   │   └── __init__.py      # CORS 中间件配置
│   └── exceptions/          # 异常处理
│       └── __init__.py      # 全局异常处理器
"""

# 该文件使 app 目录成为一个 Python 包
# 当前只包含文档字符串，不执行任何初始化代码
