import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

import app.core.database as db
from app.main import app
from app.utils.auth import get_password_hash
from app.models.user import User

# 使用 StaticPool 确保 SQLite 内存数据库在所有连接间共享
_test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
db.engine = _test_engine

# 模块级别创建所有表
SQLModel.metadata.create_all(_test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    数据库 Session fixture (function 级别)

    直接从 engine 创建 session，利用 StaticPool 保证共享同一连接。
    测试结束后清除所有数据。
    """
    session = Session(_test_engine)

    yield session

    # 清除所有表数据（按外键依赖倒序删除）
    for table in reversed(SQLModel.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    FastAPI TestClient fixture

    依赖覆盖：让所有 HTTP 请求共享同一个 db_session，
    确保 fixture 创建的数据在端点查询时可见。
    """
    def override_get_session():
        yield db_session

    app.dependency_overrides[db.get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """创建测试用普通用户"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("Test1234!"),
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def superuser(db_session):
    """创建测试用超级管理员"""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("Admin123!"),
        full_name="Admin User",
        is_active=True,
        is_superuser=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """普通用户的认证 headers"""
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "Test1234!"
    })
    data = response.json()["data"]
    return {"Authorization": f"Bearer {data['access_token']}"}


@pytest.fixture
def admin_headers(client, superuser):
    """超级管理员的认证 headers"""
    response = client.post("/api/auth/login", data={
        "username": "admin",
        "password": "Admin123!"
    })
    data = response.json()["data"]
    return {"Authorization": f"Bearer {data['access_token']}"}
