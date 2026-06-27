"""
SQLAlchemy 2.0 原生 ORM 写法示例

对比 SQLModel 与 SQLAlchemy 2.0 原生写法的区别。
SQLModel 底层就是 SQLAlchemy，但提供了 Pydantic 集成。
本文件展示纯 SQLAlchemy 2.0 的写法。
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)


# ====== 1. 声明基类 ======

class Base(DeclarativeBase):
    pass


# ====== 2. 模型定义 (SQLAlchemy 2.0 原生) ======

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    # 一对多关系
    notes: Mapped[list["Note"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    notes: Mapped[list["Note"]] = relationship(
        secondary="note_tags", back_populates="tags"
    )


# 多对多关联表
class NoteTag(Base):
    __tablename__ = "note_tags"

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None, onupdate=datetime.now)

    # 关系
    author: Mapped[User] = relationship(back_populates="notes")
    tags: Mapped[list[Tag]] = relationship(secondary="note_tags", back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note(id={self.id}, title='{self.title}')>"


# ====== 3. 对比：SQLModel vs SQLAlchemy 2.0 ======

def print_comparison():
    print("""
┌──────────────────────────┬───────────────────────────────────┐
│ SQLModel (当前项目使用)    │ SQLAlchemy 2.0 原生               │
├──────────────────────────┼───────────────────────────────────┤
│ class User(SQLModel,     │ class User(Base):                 │
│            table=True):  │     __tablename__ = "users"       │
│   id: Optional[int] =    │   id: Mapped[int] =               │
│     Field(primary_key=..)│     mapped_column(primary_key=..) │
│   username: str =        │   username: Mapped[str] =         │
│     Field(index=True)    │     mapped_column(String(50))     │
├──────────────────────────┼───────────────────────────────────┤
│ SQLModel = Pydantic +    │ 纯 SQLAlchemy，需要单独定义       │
│   SQLAlchemy             │ Pydantic 请求/响应模型            │
├──────────────────────────┼───────────────────────────────────┤
│ 适合：FastAPI 项目       │ 适合：需要精细控制 ORM 行为       │
│ 优点：一个模型同时       │ 优点：完全控制，与 FastAPI 无关   │
│   用于 DB + 验证         │ 缺点：需要额外写 Pydantic 模型    │
└──────────────────────────┴───────────────────────────────────┘
    """)


# ====== 4. 用法示例 ======

def demo():
    engine = create_engine("sqlite://", echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # 创建用户
        user = User(username="alice", email="alice@example.com")
        session.add(user)
        session.commit()

        # 创建标签
        tag_py = Tag(name="python")
        tag_web = Tag(name="web")
        session.add_all([tag_py, tag_web])
        session.commit()

        # 创建笔记并关联标签
        note = Note(
            title="SQLAlchemy 学习笔记",
            content="Mapped 和 mapped_column 是 SQLAlchemy 2.0 的核心",
            author_id=user.id,
            tags=[tag_py, tag_web],
        )
        session.add(note)
        session.commit()

        # 查询
        stmt = select(Note).where(Note.is_published == False)
        notes = session.scalars(stmt).all()
        for n in notes:
            print(f"  {n.title} by {n.author.username} tags={[t.name for t in n.tags]}")

        # 统计
        count = session.scalar(select(Note).where(Note.author_id == user.id))
        print(f"\n  用户 {user.username} 共有 {count} 篇笔记")


if __name__ == "__main__":
    print_comparison()
    demo()
