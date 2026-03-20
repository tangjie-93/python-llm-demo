"""
配置模块

该模块负责应用的所有配置管理，使用 Pydantic Settings 进行配置管理。
支持从环境变量或 .env 文件读取配置。
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    应用配置类

    继承自 Pydantic 的 BaseSettings，自动从环境变量或 .env 文件加载配置。
    配置项说明：
    - APP_NAME: 应用名称
    - VERSION: 应用版本号
    - DESCRIPTION: 应用描述
    - DEBUG: 调试模式开关（生产环境应设为 False）
    - DATABASE_URL: 数据库连接字符串
    - SECRET_KEY: JWT 密钥（生产环境应使用复杂的随机密钥）
    - ALGORITHM: JWT 算法（HS256 是最常用的）
    - ACCESS_TOKEN_EXPIRE_MINUTES: JWT 令牌过期时间（分钟）
    - CORS_ORIGINS: 允许的跨域来源列表
    """

    # 应用基本信息
    APP_NAME: str = "FastAPI Backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI Backend API"
    DEBUG: bool = True

    # 数据库配置
    # 格式说明：
    # - sqlite:///./fastapi.db: 相对路径，当前目录下的 fastapi.db
    # - sqlite:////absolute/path: 绝对路径
    # - postgresql://user:pass@localhost/dbname: PostgreSQL
    DATABASE_URL: str = "sqlite:///./fastapi.db"

    # JWT 认证配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS 跨域配置
    # 列出允许访问 API 的前端域名
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        """
        Pydantic Settings 配置

        - env_file: 指定 .env 文件路径
        - case_sensitive: 配置键是否区分大小写（通常生产配置应区分大小写）
        """
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置单例

    使用 @lru_cache 装饰器确保配置对象只被创建一次，
    避免每次导入时都重新读取配置。

    Returns:
        Settings: 配置对象实例
    """
    return Settings()


# 创建全局配置实例
# 在应用任何地方都可以通过 from app.core.config import settings 导入使用
settings = get_settings()
