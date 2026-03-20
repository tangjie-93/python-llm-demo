"""
核心模块包

该包包含了应用的核心功能：

- config.py: 配置管理
    - Settings 类：从环境变量或 .env 文件加载配置
    - settings 对象：全局配置实例
    - get_settings() 函数：获取配置单例

- database.py: 数据库连接
    - engine: SQLAlchemy 数据库引擎
    - create_db_and_tables(): 创建数据库表
    - get_session(): 获取数据库会话的依赖注入函数

使用方式：
    from app.core.config import settings
    from app.core.database import get_session, engine
"""

# 该文件使 core 目录成为一个 Python 包
# 当前只包含文档字符串，不执行任何初始化代码
