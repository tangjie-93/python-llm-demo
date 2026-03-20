"""
FastAPI 应用入口文件

该文件是整个后端应用的入口点，负责：
1. 创建 FastAPI 应用实例
2. 配置中间件、异常处理器、路由
3. 管理应用生命周期（启动和关闭）
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, create_db_and_tables
from app.middleware import setup_middleware
from app.routers import setup_routers
from app.exceptions import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理函数

    这是一个异步上下文管理器，用于处理应用启动和关闭时的逻辑。

    启动阶段：
        - 打印调试信息（当前配置）
        - 创建数据库表（如果不存在）

    关闭阶段：
        - 可以在这里添加清理逻辑（如关闭数据库连接）
        - 当前为空，因为 SQLAlchemy 会自动管理连接

    Args:
        app: FastAPI 应用实例

    Yields:
        控制权给应用运行
    """
    print("=== Application starting ===")
    print(f"DEBUG mode: {settings.DEBUG}")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    # 创建数据库表
    create_db_and_tables()
    print("=== Application started ===")
    yield
    # 应用关闭时的清理逻辑可以写在这里
    print("=== Application shutdown ===")


# 创建 FastAPI 应用实例
# 配置项说明：
# - title: API 文档中显示的应用名称
# - version: API 版本号
# - description: API 描述信息
# - docs_url: Swagger 文档访问地址（默认 /docs）
# - redoc_url: ReDoc 文档访问地址（默认 /redoc）
# - openapi_url: OpenAPI JSON 规范地址
# - debug: 调试模式开关
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.DEBUG,
)

# 按顺序配置应用的各个组件
# 顺序很重要：中间件 -> 异常处理 -> 路由
setup_middleware(app)           # 配置 CORS 中间件
setup_exception_handlers(app)   # 配置全局异常处理器
setup_routers(app)             # 注册路由


@app.get("/")
def root():
    """
    根路径路由 - 欢迎页面

    Returns:
        dict: 包含欢迎信息和版本号
    """
    return {"message": "Welcome to FastAPI Backend", "version": settings.VERSION}


@app.get("/health")
def health_check():
    """
    健康检查路由

    用于负载均衡器或容器编排系统检查应用状态

    Returns:
        dict: 固定返回 {"status": "healthy"}
    """
    return {"status": "healthy"}
