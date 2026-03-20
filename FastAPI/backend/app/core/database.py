"""
数据库模块

该模块负责数据库连接管理和会话管理。
使用 SQLModel（SQLAlchemy + Pydantic）作为 ORM。
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from app.core.config import settings

# 打印数据库连接信息
print(f"Creating engine with DATABASE_URL: {settings.DATABASE_URL}")

# 创建数据库引擎
# 参数说明：
# - DATABASE_URL: 数据库连接字符串
#   - sqlite:///./fastapi.db: 相对路径，数据库文件在当前目录
#   - echo: 是否打印 SQL 语句（调试时很有用）
#   - connect_args: 特定数据库的连接参数
#     - check_same_thread: SQLite 特有，用于多线程访问
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)


def create_db_and_tables():
    """
    创建数据库表

    根据 SQLModel 中定义的模型类，自动创建对应的数据库表。
    如果表已存在，则不会重复创建（相当于 CREATE TABLE IF NOT EXISTS）。

    注意：
    - 在调用此函数之前，必须确保所有模型类都已被导入
    - 否则 SQLModel.metadata 中没有模型信息，无法创建表

    Raises:
        Exception: 创建表失败时抛出异常
    """
    print("=== Creating database tables ===")
    # 打印当前已注册的模型表信息
    print(f"SQLModel.metadata tables: {list(SQLModel.metadata.tables.keys())}")
    try:
        SQLModel.metadata.create_all(engine)
        print("=== Database tables created successfully ===")
    except Exception as e:
        print(f"=== Error creating database tables: {e} ===")
        import traceback
        traceback.print_exc()


def get_session() -> Generator[Session, None, None]:
    """
    获取数据库会话的依赖注入函数

    这是一个 FastAPI 依赖注入函数，用于在每个请求中获取数据库会话。
    使用 yield 模式：yield 之前的代码相当于 __enter__，之后的代码相当于 __exit__。

    使用方式：
        @app.get("/users")
        def get_users(session: Session = Depends(get_session)):
            ...

    Yields:
        Session: 数据库会话对象

    Note:
        - Session 是 SQLAlchemy 的会话对象
        - 每次请求结束，会话会自动关闭
        - 如果发生异常，事务会自动回滚
    """
    # 创建会话
    with Session(engine) as session:
        try:
            # yield 会话给路由函数使用
            yield session
        finally:
            # 确保会话被正确关闭
            session.close()
