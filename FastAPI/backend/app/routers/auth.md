# FastAPI 认证模块详解 - auth.py

## 目录

1. [模块概述](#1-模块概述)
2. [导入的依赖](#2-导入的依赖)
3. [全局配置](#3-全局配置)
4. [登录失败追踪器](#4-登录失败追踪器)
5. [数据模型](#5-数据模型)
6. [密码处理函数](#6-密码处理函数)
7. [JWT Token 处理](#7-jwt-token-处理)
8. [依赖注入函数](#8-依赖注入函数)
9. [API 路由端点](#9-api-路由端点)
10. [认证流程图](#10-认证流程图)
11. [使用示例](#11-使用示例)
12. [注意事项](#12-注意事项)

---

## 1. 模块概述

`auth.py` 是 FastAPI 项目的**认证路由模块**，负责处理所有与用户认证相关的功能：

| 功能 | 说明 |
|------|------|
| 用户登录 | 验证用户名密码，返回 JWT Token + Refresh Token |
| 用户注册 | 创建新用户账号 |
| 获取当前用户 | 验证 Token 并返回用户信息 |
| Token 刷新 | 使用 Refresh Token 刷新 Access Token |
| 用户登出 | 清除 Refresh Token |
| 密码加密 | 使用 `pbkdf2_sha256` 算法 |
| JWT 认证 | 使用 `python-jose` 库处理 Token |
| 登录限制 | 5 次失败后锁定账户 1 小时 |

**认证方式**：`OAuth2` + `JWT` (JSON Web Token) + `Refresh Token`

---

## 2. 导入的依赖

```python
from datetime import datetime, timedelta, timezone  # 时间处理
from typing import Optional, Dict  # 类型注解
import secrets  # 生成安全随机数
import re  # 正则表达式
from collections import defaultdict  # 默认字典
import threading  # 线程锁

from fastapi import APIRouter, Depends, status, HTTPException, Response, Request  # FastAPI 核心
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
| `secrets` | 生成安全的随机 Token |
| `threading` | 线程安全锁（登录失败追踪） |

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

## 4. 登录失败追踪器

### 4.1 LoginAttemptTracker 类

```python
class LoginAttemptTracker:
    """
    登录失败追踪器
    
    用于记录每个用户的登录失败次数，防止暴力破解。
    使用内存存储，生产环境建议使用 Redis。
    """
```

**功能特性**：

| 属性 | 说明 |
|------|------|
| `max_attempts = 5` | 最大失败次数 |
| `lockout_duration = timedelta(hours=1)` | 锁定时长 1 小时 |
| `_lock = threading.Lock()` | 线程锁，保证并发安全 |
| `failed_attempts: Dict[str, list]` | 记录每个用户的失败时间 |

### 4.2 核心方法

#### record_failed_attempt

```python
def record_failed_attempt(self, username: str) -> None:
    """记录一次失败尝试"""
```

#### get_failed_count

```python
def get_failed_count(self, username: str) -> int:
    """获取当前失败次数"""
```

#### is_locked_out

```python
def is_locked_out(self, username: str) -> tuple[bool, Optional[int]]:
    """
    检查是否被锁定
    
    Returns:
        tuple[bool, Optional[int]]: (是否锁定，剩余锁定时间（分钟）)
    """
```

#### reset_failed_attempts

```python
def reset_failed_attempts(self, username: str) -> None:
    """重置失败计数（登录成功后调用）"""
```

### 4.3 全局追踪器实例

```python
login_tracker = LoginAttemptTracker()
```

---

## 5. 数据模型

### 5.1 Token 模型

```python
class Token(BaseModel):
    access_token: str      # JWT 访问令牌
    token_type: str        # 令牌类型（"bearer"）
    refresh_token: str     # 刷新令牌
    expires_in: int        # access_token 过期时间（秒）
```

**用途**：登录成功后的响应数据格式

### 5.2 TokenData 模型

```python
class TokenData(BaseModel):
    username: Optional[str] = None  # 用户名（JWT 的 subject）
```

**用途**：解析 JWT 载荷中的用户数据

### 5.3 RefreshTokenRequest 模型

```python
class RefreshTokenRequest(BaseModel):
    refresh_token: str  # 刷新令牌
```

**用途**：刷新 Token 时的请求数据验证

### 5.4 UserCreate 模型

```python
class UserCreate(BaseModel):
    username: str  # 用户名 (4-32 位字母数字下划线)
    email: str     # 邮箱地址
    password: str  # 密码 (至少 8 位，包含大小写字母和数字)
```

**用途**：用户注册时的请求数据验证

---

## 6. 密码处理函数

### 6.1 密码强度验证

```python
def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    验证密码强度

    密码必须满足：
    - 至少 8 位
    - 包含大小写字母
    - 包含数字
    """
```

**验证规则**：

| 规则 | 说明 |
|------|------|
| 长度 | 至少 8 位 |
| 小写字母 | 必须包含至少 1 个 |
| 大写字母 | 必须包含至少 1 个 |
| 数字 | 必须包含至少 1 个 |

### 6.2 验证密码

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**功能**：将明文密码与数据库中的哈希密码进行比对

### 6.3 生成密码哈希

```python
def get_password_hash(password: str) -> str:
    password = password[:72]  # 截断到 72 字节，避免 bcrypt 限制
    return pwd_context.hash(password)
```

**功能**：将明文密码转换为哈希值存储到数据库

---

## 7. JWT Token 处理

### 7.1 创建访问令牌

```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # 默认 15 分钟
    
    to_encode.update({"exp": expire})  # 添加过期时间到载荷
    to_encode.update({"type": "access"})  # 添加 token 类型
    
    # 使用 JWT 编码
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `data` | `dict` | 要编码的数据，通常包含 `{"sub": username}` |
| `expires_delta` | `Optional[timedelta]` | 过期时间增量，默认 15 分钟 |
| `settings.SECRET_KEY` | `str` | JWT 签名密钥（从配置读取） |
| `settings.ALGORITHM` | `str` | 加密算法，如 `"HS256"` |

### 7.2 创建刷新令牌

```python
def create_refresh_token() -> str:
    """
    创建刷新令牌
    
    生成一个随机的 refresh token，用于刷新 access token。
    """
    return secrets.token_urlsafe(32)
```

**特点**：
- 使用 `secrets` 模块生成安全的随机字符串
- 有效期 7 天
- 存储在数据库和 HttpOnly Cookie 中

### 7.3 验证刷新令牌

```python
def verify_refresh_token(user: User, refresh_token: str) -> bool:
    """
    验证刷新令牌
    
    验证提供的 refresh token 是否与用户存储的匹配且未过期。
    """
    if not user.refresh_token or not user.token_expires_at:
        return False
    
    # 检查 token 是否匹配
    if user.refresh_token != refresh_token:
        return False
    
    # 检查是否过期
    expires_at = datetime.fromisoformat(user.token_expires_at)
    if datetime.now(timezone.utc) > expires_at:
        return False
    
    return True
```

---

## 8. 依赖注入函数

### 8.1 获取当前用户

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

## 9. API 路由端点

### 9.1 用户登录

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
    "token_type": "bearer",
    "expires_in": 900
  },
  "cookies": {
    "refresh_token": "HttpOnly Cookie"
  }
}
```

**安全特性**：

| 特性 | 说明 |
|------|------|
| 登录失败限制 | 5 次失败后锁定账户 1 小时 |
| 剩余尝试提示 | 显示还剩多少次尝试机会 |
| 锁定时间提示 | 显示还需等待多少分钟 |
| Refresh Token | HttpOnly Cookie，防止 XSS 攻击 |

**错误响应**：

| 情况 | 状态码 | 错误信息 |
|------|--------|----------|
| 用户名格式错误 | `400` | "用户名格式错误" |
| 账户已锁定 | `429` | "登录尝试次数过多，账户已锁定" |
| 用户不存在 | `401` | "用户不存在，请先注册" |
| 密码错误 | `401` | "密码错误，还剩 X 次尝试机会" |

---

### 9.2 用户注册

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
  "password": "Secret123"
}
```

**验证规则**：

| 字段 | 规则 |
|------|------|
| `username` | 4-32 位字母、数字或下划线 |
| `email` | 标准邮箱格式 |
| `password` | 至少 8 位，包含大小写字母和数字 |

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
| 用户名格式错误 | `400` | "用户名格式错误，应为 4-32 位字母、数字或下划线" |
| 密码强度不足 | `400` | "密码长度至少为 8 位" 等 |
| 邮箱格式错误 | `400` | "邮箱格式不正确" |
| 用户名/邮箱已存在 | `400` | "用户名或邮箱已存在" |

---

### 9.3 获取当前用户信息

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

### 9.4 刷新访问令牌

```python
@router.post("/refresh", response_model=ApiResponse)
async def refresh_access_token(
    request: Request,
    session: Session = Depends(get_session)
):
```

**请求方式**：
- 自动从 Cookie 中读取 `refresh_token`（HttpOnly）
- 无需手动传递参数

**响应示例**：

```json
{
  "code": 200,
  "message": "Token 刷新成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

**错误响应**：

| 情况 | 状态码 | 错误信息 |
|------|--------|----------|
| 未找到刷新令牌 | `401` | "未找到刷新令牌" |
| 无效的刷新令牌 | `401` | "无效的刷新令牌" |
| 刷新令牌过期 | `401` | "刷新令牌已过期或无效" |

**Token 有效期**：

| Token 类型 | 有效期 | 存储位置 |
|-----------|--------|----------|
| Access Token | 15 分钟 | 客户端内存 |
| Refresh Token | 7 天 | HttpOnly Cookie + 数据库 |

---

### 9.5 用户登出

```python
@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
```

**请求头**：

```
Authorization: Bearer <access_token>
```

**功能**：
- 清除数据库中用户的 `refresh_token` 和 `token_expires_at`
- 删除 HttpOnly Cookie 中的 `refresh_token`

**响应示例**：

```json
{
  "code": 200,
  "message": "登出成功"
}
```

---

## 10. 认证流程图

### 10.1 登录流程

```
┌─────────────┐     POST /api/auth/login     ┌─────────────┐
│   客户端     │ ───────────────────────────> │   服务器     │
│  (用户名/    │   username, password         │             │
│   密码)      │                              │  1. 验证格式  │
└─────────────┘                              │  2. 检查锁定  │
                                             │  3. 验证用户  │
                                             │  4. 验证密码  │
                                             │  5. 生成 JWT  │
                                             │  6. 生成      │
                                             │     Refresh   │
                                             │  7. 返回 Token│
┌─────────────┐     <access_token>           │             │
│   客户端     │ <─────────────────────────── └─────────────┘
│ (存储 Token)│     <refresh_token Cookie>
└─────────────┘
```

### 10.2 访问受保护资源流程

```
┌─────────────┐     GET /api/users/me        ┌─────────────┐
│   客户端     │ ───────────────────────────> │   服务器     │
│ (带 Token)   │   Authorization:             │             │
│              │   Bearer <token>             │  1. 提取 Token│
└─────────────┘                              │  2. 验证 JWT │
                                             │  3. 解析用户  │
                                             │  4. 查询用户  │
                                             │  5. 返回数据  │
┌─────────────┐     用户信息                  │             │
│   客户端     │ <─────────────────────────── └─────────────┘
└─────────────┘
```

### 10.3 刷新 Token 流程

```
┌─────────────┐     POST /api/auth/refresh   ┌─────────────┐
│   客户端     │ ───────────────────────────> │   服务器     │
│ (Access     │   Cookie: refresh_token      │             │
│  Token 过期) │                              │  1. 读取     │
└─────────────┘                              │     Cookie   │
                                             │  2. 验证     │
                                             │     Refresh  │
                                             │  3. 生成新    │
                                             │     Token    │
┌─────────────┐     <new access_token>       │             │
│   客户端     │ <─────────────────────────── └─────────────┘
│ (新 Token)  │     <new refresh_token Cookie>
└─────────────┘
```

---

## 11. 使用示例

### 11.1 登录获取 Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=Secret123"
```

### 11.2 使用 Token 访问受保护接口

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### 11.3 刷新 Token

```bash
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -H "Content-Type: application/json" \
  -b "refresh_token=your_refresh_token"
```

### 11.4 用户登出

```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### 11.5 在其他路由中使用认证依赖

```python
from app.routers.auth import get_current_user

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}"}
```

---

## 12. 注意事项

### 12.1 已知问题

| 问题 | 位置 | 说明 |
|------|------|------|
| `tokenUrl` 不匹配 | 第 118 行 | 配置为 `/api/auth/token`，实际路由是 `/api/auth/login` |

### 12.2 安全特性

| 特性 | 说明 |
|------|------|
| **登录失败限制** | 5 次失败后锁定账户 1 小时 |
| **密码强度验证** | 至少 8 位，包含大小写字母和数字 |
| **用户名格式验证** | 4-32 位字母、数字或下划线 |
| **HttpOnly Cookie** | Refresh Token 存储在 HttpOnly Cookie 中，防止 XSS |
| **SameSite Cookie** | 设置为 `lax`，防止 CSRF 攻击 |
| **密码截断** | 截断到 72 字节，避免 bcrypt 限制 |

### 12.3 安全建议

1. **使用 HTTPS**：生产环境必须使用 HTTPS 传输 Token
2. **设置 Secure Cookie**：生产环境将 `secure=True`（仅 HTTPS 传输 Cookie）
3. **实现 Token 黑名单**：当前未实现 Token 黑名单功能
4. **使用 Redis**：生产环境建议使用 Redis 存储登录失败记录
5. **实现登录日志**：记录用户登录行为，便于审计

### 12.4 配置项

在 `app/core/config.py` 中需要配置：

```python
SECRET_KEY = "your-secret-key"  # JWT 签名密钥
ALGORITHM = "HS256"             # JWT 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Token 过期时间（分钟）
REFRESH_TOKEN_EXPIRE_DAYS = 7     # Refresh Token 过期时间（天）
```

### 12.5 Token 策略

| Token 类型 | 有效期 | 用途 | 存储方式 |
|-----------|--------|------|----------|
| Access Token | 15 分钟 | 访问 API 资源 | 客户端内存，请求头携带 |
| Refresh Token | 7 天 | 刷新 Access Token | HttpOnly Cookie + 数据库 |

**优点**：
- Access Token 短期有效，降低泄露风险
- Refresh Token 长期有效，提升用户体验
- 双重验证（Cookie + 数据库），提高安全性

---

*文档更新时间：2026-04-16*
