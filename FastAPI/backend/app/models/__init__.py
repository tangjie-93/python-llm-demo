"""
数据模型包

该包包含了所有的数据库模型定义。

模型说明：
- User: 用户模型，对应 users 表
- Item: 物品模型，对应 items 表

重要说明：
在创建数据库表之前，必须确保所有模型类都已被导入，
否则 SQLModel.metadata 中没有模型信息，create_all() 无法创建表。

导入方式（在 main.py 或 database.py 中）：
    import app.models.user
    import app.models.item

或者在 __init__.py 中导出：
    from app.models.user import User
    from app.models.item import Item
"""

# 该文件使 models 目录成为一个 Python 包
# 当前只包含文档字符串，不执行任何初始化代码
#
# 注意：如果你希望在其他模块中更方便地导入模型，
# 可以在这里添加导入语句：
#   from app.models.user import User, UserCreate, UserUpdate, UserResponse
#   from app.models.item import Item, ItemCreate, ItemUpdate, ItemResponse
