# FastAPI 认证模块详解 - auth.py

## 目录

1. [模块概述](#1-模块概述)
2. [导入的依赖](#2-导入的依赖)
3. [全局配置](#3-全局配置)
4. [数据模型](#4-数据模型)
5. [密码处理函数](#5-密码处理函数)
6. [JWT Token 处理](#6-jwt-token-处理)
7. [依赖注入函数](#7-依赖注入函数)
8. [API 路由端点](#8-api-路由端点)
9. [认证流程图](#9-认证流程图)
10. [使用示例](#10-使用示例)
11. [注意事项](#11-注意事项)

---

## 1. 模块概述

`auth.py` 是 FastAPI 项目的**认证路由模块**，负责处理所有与用户认证相关的功能：

| 功能 | 说明 |
|------|------|
| 用户登录 | 验证用户名密码，返回 JWT Token |
| 用户注册 | 创建新用户账号 |
| 获取当前用户 | 验证 Token 并返回用户信息 |
| 密码加密 | 使用 `pbkdf2_sha256` 算法 |
| JWT 认证 | 使用 `python-jose` 库处理 Token |

**认证方式**：`OAuth2` + `JWT` (JSON Web Token)

---

## 2. 导入的依赖

```python
from datetime import datetime, timedelta, timezone  # 时间处理
from typing import Optional  # 类型注解

from fastapi import APIRouter, Depends, status, HTTPException  # FastAPI 核心
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # OAuth2 认证
from jose import JWTError, jwt  # JWT 处理
from passlib.context import CryptContext  # 密码加密
from pydantic import BaseModel  # 数据模型
from sqlmodel import Session, select  # 数据库 ORM

from app.core.config import settings  # 应用配置
from app.core.database import get_session  # 数据库会话
from app.core.response import success_response, error_response  # 统一响应
from app.models.user import User  # 用户模型
from app.models.response import ApiResponse  # 响应模型
```

### 依赖说明

| 依赖 | 用途 |
|------|------|
| `fastapi.security.OAuth2PasswordBearer` | 从请求头提取 Token |
| `fastapi.security.OAuth2PasswordRequestForm` | 处理登录表单数据 |
| `jose.jwt` | 编码和解码 JWT Token |
| `passlib.CryptContext` | 密码哈希加密和验证 |
| `sqlmodel` | 数据库查询和操作 |

---

## 3. 全局配置

### 3.1 路由器实例

```python
router = APIRouter()
```

- 注意：`prefix` 已在 `routers/__init__.py` 中设置为 `/api/auth`
- 所以该模块的所有路由前缀都是 `/api/auth`

### 3.2 密码加密上下文

```python
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
```

| 参数 | 说明 |
|------|------|
| `schemes=["pbkdf2_sha256"]` | 使用 `pbkdf2_sha256` 算法 |
| `deprecated="auto"` | 允许密码算法自动升级 |

### 3.3 OAuth2 认证方案

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
```

| 参数 | 说明 |
|------|------|
| `tokenUrl` | 获取 Token 的 URL（供 Swagger UI 使用） |

⚠️ **注意**：实际登录路由是 `/api/auth/login`，但这里配置的是 `/api/auth/token`，两者不一致。

---

## 4. 数据模型

### 4.1 Token 模型

```python
class Token(BaseModel):
    access_token: str  # JWT 访问令牌
    token_type: str    # 令牌类型（通常为 "bearer"）
```

**用途**：登录成功后的响应数据格式

### 4.2 TokenData 模型

```python
class TokenData(BaseModel):
    username: Optional[str] = None  # 用户名（JWT 的 subject）
```

**用途**：解析 JWT 载荷中的用户数据

### 4.3 UserCreate 模型

```python
class UserCreate(BaseModel):
    username: str  # 用户名
    email: str     # 邮箱地址
    password: str  # 密码
```

**用途**：用户注册时的请求数据验证

---

## 5. 密码处理函数

### 5.1 验证密码

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**功能**：将明文密码与数据库中的哈希密码进行比对

### 5.2 生成密码哈希

```python
def get_password_hash(password: str) -> str:
    password = password[:72]  # 截断到 72 字节，避免 bcrypt 限制
    return pwd_context.hash(password)
```

**功能**：将明文密码转换为哈希值存储到数据库

---

## 6. JWT Token 处理

### 6.1 创建访问令牌

```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=24)  # 默认 24 小时
    
    to_encode.update({"exp": expire})  # 添加过期时间到载荷
    
    # 使用 JWT 编码
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `data` | `dict` | 要编码的数据，通常包含 `{"sub": username}` |
| `expires_delta` | `Optional[timedelta]` | 过期时间增量，默认 24 小时 |
| `settings.SECRET_KEY` | `str` | JWT 签名密钥（从配置读取） |
| `settings.ALGORITHM` | `str` | 加密算法，如 `"HS256"` |

---

## 7. 依赖注入函数

### 7.1 获取当前用户

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),      # 从请求头提取 Token
    session: Session = Depends(get_session)   # 数据库会话
) -> User:
```

**功能流程**：

```
┌─────────────────┐
│  从请求头提取    │
│  Authorization: │
│  Bearer <token> │
└────────┬────────┘
         ▼
┌─────────────────┐
│  解码 JWT Token  │
│  jwt.decode()   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  获取 username  │
│  payload["sub"] │
└────────┬────────┘
         ▼
┌─────────────────┐
│  查询数据库      │
│  获取用户对象    │
└────────┬────────┘
         ▼
┌─────────────────┐
│  返回 User 对象  │
│  或抛出 401 异常 │
└─────────────────┘
```

**异常处理**：

| 情况 | 响应 |
|------|------|
| Token 无效 | `401 Unauthorized` |
| Token 过期 | `401 Unauthorized` |
| 用户不存在 | `401 Unauthorized` |

**使用方式**：

```python
@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    # current_user 就是当前登录的用户对象
    return current_user
```

---

## 8. API 路由端点

### 8.1 用户登录

```python
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
```

**请求格式**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `username` | `string` | 用户名 |
| `password` | `string` | 密码 |

**Content-Type**：`application/x-www-form-urlencoded`

**响应示例**：

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  }
}
```

**错误响应**：

| 情况 | 状态码 | 错误信息 |
|------|--------|----------|
| 用户不存在 | `401` | "用户不存在,请先注册" |
| 密码错误 | `401` | "密码错误" |

---

### 8.2 用户注册

```python
@router.post("/register", response_model=ApiResponse)
async def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
```

**请求体**（`JSON`）：

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

**响应示例**：

```json
{
  "code": 200,
  "message": "用户注册成功",
  "data": {
    "user_id": 1
  }
}
```

**错误响应**：

| 情况 | 状态码 | 错误信息 |
|------|--------|----------|
| 用户名/邮箱已存在 | `400` | "用户名或邮箱已存在" |

---

### 8.3 获取当前用户信息

```python
@router.get("/me", response_model=ApiResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
```

**请求头**：

```
Authorization: Bearer <access_token>
```

**响应示例**：

```json
{
  "code": 200,
  "message": "获取用户信息成功",
  "data": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_active": true
  }
}
```

---

## 9. 认证流程图

### 9.1 登录流程

```
┌─────────────┐     POST /api/auth/login     ┌─────────────┐
│   客户端     │ ───────────────────────────> │   服务器     │
│  (用户名/    │   username, password         │             │
│   密码)      │                              │  1. 验证用户  │
└─────────────┘                              │     存在？   │
                                             │  2. 验证密码  │
                                             │     正确？   │
                                             │  3. 生成 JWT  │
                                             │  4. 返回 Token│
┌─────────────┐     <access_token>           │             │
│   客户端     │ <─────────────────────────── └─────────────┘
│  (存储 Token)│
└─────────────┘
```

### 9.2 访问受保护资源流程

```
┌─────────────┐     GET /api/users/me        ┌─────────────┐
│   客户端     │ ───────────────────────────> │   服务器     │
│ (带 Token)   │   Authorization:             │             │
│              │   Bearer <token>             │  1. 提取 Token│
└─────────────┘                              │  2. 验证 JWT │
                                             │  3. 解析用户  │
                                             │  4. 查询用户  │
┌─────────────┐     用户信息                  │  5. 返回数据  │
│   客户端     │ <─────────────────────────── └─────────────┘
└─────────────┘
```

---

## 10. 使用示例

### 10.1 登录获取 Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret123"
```

### 10.2 使用 Token 访问受保护接口

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### 10.3 在其他路由中使用认证依赖

```python
from app.routers.auth import get_current_user

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}"}
```

---

## 11. 注意事项

### 11.1 已知问题

| 问题 | 位置 | 说明 |
|------|------|------|
| `tokenUrl` 不匹配 | 第 41 行 | 配置为 `/api/auth/token`，实际路由是 `/api/auth/login` |

### 11.2 安全建议

1. **使用 HTTPS**：生产环境必须使用 HTTPS 传输 Token
2. **设置合理的 Token 过期时间**：当前默认 24 小时
3. **实现 Token 刷新机制**：当前未实现 Refresh Token
4. **密码强度验证**：当前仅限制长度 72 字节
5. **实现登出功能**：当前未实现 Token 黑名单

### 11.3 配置项

在 `app/core/config.py` 中需要配置：

```python
SECRET_KEY = "your-secret-key"  # JWT 签名密钥
ALGORITHM = "HS256"             # JWT 算法
ACCESS_TOKEN_EXPIRE_DAYS = 7    # Token 过期天数
```

---

*文档生成时间：2026-04-15*
