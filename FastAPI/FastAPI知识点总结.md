# FastAPI 完整知识点总结

FastAPI 是一个现代、快速的 Python Web 框架，用于构建 API。它基于 Python 类型提示构建，天生支持异步编程，具有自动文档生成、类型验证等特性。

---

## 目录

1. [基础入门](#1-基础入门)
2. [路由与请求处理](#2-路由与请求处理)
3. [Pydantic 数据模型](#3-pydantic-数据模型)
4. [响应处理](#4-响应处理)
5. [依赖注入系统](#5-依赖注入系统)
6. [中间件](#6-中间件)
7. [错误处理](#7-错误处理)
8. [安全与认证](#8-安全与认证)
9. [数据库集成](#9-数据库集成)
10. [异步编程](#10-异步编程)
11. [WebSocket](#11-websocket)
12. [配置管理](#12-配置管理)
13. [测试](#13-测试)
14. [部署与性能优化](#14-部署与性能优化)
15. [最佳实践](#15-最佳实践)

---

## 1. 基础入门

### 1.1 安装与环境配置

```bash
# 使用 Poetry 安装（推荐）
poetry add fastapi uvicorn

# 或使用 pip 安装
pip install fastapi

# 安装 uvicorn 作为 ASGI 服务器
pip install "uvicorn[standard]"

# 安装所有可选依赖
pip install "fastapi[all]"
```

### 1.2 Poetry 项目配置

```bash
# 初始化 Poetry 项目
poetry new fastapi-project

# 安装项目依赖
poetry install

# 添加依赖
poetry add fastapi uvicorn

# 添加开发依赖
poetry add --group dev pytest black ruff

# 更新依赖
poetry update

# 生成 requirements.txt（用于某些不支持 Poetry 的环境）
poetry export -f requirements.txt --output requirements.txt

# 激活虚拟环境
poetry shell

# 查看依赖树
poetry show --tree

# 检查过时的依赖
poetry show --outdated

# 运行开发服务器
poetry run uvicorn main:app --reload

# 运行测试
poetry run pytest
```

### 1.3 第一个 FastAPI 应用

```python
from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### 1.4 启动服务

```bash
# 使用 Poetry 运行
poetry run uvicorn main:app --reload

# 默认启动（localhost:8000）
uvicorn main:app --reload

# 指定主机和端口
uvicorn main:app --host 0.0.0.0 --port 8000

# 使用 HTTPS
uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### 1.5 自动文档

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### 1.6 FastAPI 应用配置

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My API",
    description="API Documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=True,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 2. 路由与请求处理

### 2.1 HTTP 方法装饰器

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_items():
    return {"method": "GET"}

@app.post("/items")
def create_item():
    return {"method": "POST"}

@app.put("/items/{item_id}")
def update_item(item_id: int):
    return {"method": "PUT", "item_id": item_id}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"method": "DELETE", "item_id": item_id}

@app.patch("/items/{item_id}")
def patch_item(item_id: int):
    return {"method": "PATCH", "item_id": item_id}

@app.options("/items")
def options_items():
    return {"method": "OPTIONS"}
```

### 2.2 路径参数

```python
from fastapi import FastAPI

app = FastAPI()

# 基础路径参数
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# 带类型的路径参数
@app.get("/products/{product_id}")
def get_product(product_id: str):
    return {"product_id": product_id}

# 路径参数验证
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="ID must be positive")
    return {"item_id": item_id}
```

### 2.3 预定义路径参数

```python
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

### 2.4 查询参数

```python
from fastapi import FastAPI, Query
from typing import Union

app = FastAPI()

# 基础查询参数
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# 可选查询参数
@app.get("/items")
def read_items(q: Union[str, None] = None):
    if q:
        return {"q": q}
    return {"q": None}

# 带验证的查询参数
@app.get("/items")
def read_items(
    q: str = Query(default=None, min_length=3, max_length=50),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100)
):
    return {"q": q, "page": page, "size": size}

# 必需查询参数
@app.get("/items")
def read_items(q: str = Query(...)):
    return {"q": q}

# 多个值的查询参数
@app.get("/items")
def read_items(q: Union[list[str], None] = Query(default=None)):
    return {"q": q}

# 带别名的查询参数
@app.get("/items")
def read_items(q: str = Query(default=None, alias="item-query")):
    return {"q": q}

# 已弃用的查询参数
@app.get("/items")
def read_items(
    q: str = Query(default=None, deprecated=True)
):
    return {"q": q}
```

### 2.5 请求体

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# 基础请求体
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items")
def create_item(item: Item):
    return item

# 带字段验证的请求体
class ItemValidated(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    tax: float | None = Field(default=None, ge=0)

# 嵌套模型
class Image(BaseModel):
    url: str
    name: str

class ItemWithImage(BaseModel):
    name: str
    description: str | None = None
    price: float
    tags: list[str] = []
    images: list[Image] | None = None
```

### 2.6 多个请求体参数

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    full_name: str | None = None

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# 多个 Pydantic 模型
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, user: User):
    return {"item_id": item_id, "item": item, "user": user}

# 混合参数
@app.patch("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    q: str | None = None,
    importance: int = Body(...)
):
    return {"item_id": item_id, "item": item, "q": q, "importance": importance}
```

### 2.7 表单数据

```python
from fastapi import FastAPI, Form
from typing import Annotated

app = FastAPI()

# 基础表单
@app.post("/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

# 可选表单字段
@app.post("/login-optional")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str | None] = Form(default=None)
):
    return {"username": username, "password": password}

# 多个值的表单
@app.post("/items")
def create_item(
    name: Annotated[str, Form(min_length=3)],
    description: Annotated[str | None] = Form(default=None),
    price: Annotated[float, Form(gt=0)],
    tags: Annotated[list[str] | None] = Form(default=None)
):
    return {"name": name, "description": description, "price": price, "tags": tags}
```

### 2.8 文件上传

```python
from fastapi import FastAPI, UploadFile, File, Form
from typing import Annotated

app = FastAPI()

# 基础文件上传
@app.post("/upload")
async def upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "content_size": len(contents)}

# 指定文件类型
@app.post("/upload-image")
async def upload_image(
    file: Annotated[UploadFile, File(content_type="image/png")]
):
    return {"filename": file.filename, "content_type": file.content_type}

# 多个文件上传
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile]):
    return {"file_count": len(files), "filenames": [f.filename for f in files]}

# 带进度追踪的文件上传
@app.post("/upload-with-form")
async def upload_with_form(
    description: Annotated[str, Form()],
    file: Annotated[UploadFile, File()]
):
    contents = await file.read()
    return {
        "description": description,
        "filename": file.filename,
        "size": len(contents)
    }

# 保存上传的文件
@app.post("/upload/save")
async def upload_and_save(file: UploadFile):
    save_path = f"uploads/{file.filename}"
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"path": save_path}
```

### 2.9 请求对象

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/request-info")
async def get_request_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": request.path_params,
        "client": request.client.host if request.client else None,
    }
```

---

## 3. Pydantic 数据模型

### 3.1 基础模型

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# 基础模型
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

# 带默认值的模型
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0

# 模型配置
class UserConfig(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"  # 禁止额外字段
    )
    
    id: int
    name: str
```

### 3.2 字段验证

```python
from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional
import re

class UserValidated(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(default=18, ge=0, le=150)
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @field_validator('phone')
    @classmethod
    def phone_format(cls, v):
        if v is not None:
            if not re.match(r'^\d{10,11}$', v.replace('-', '').replace(' ', '')):
                raise ValueError('Invalid phone number format')
        return v
```

### 3.3 嵌套模型

```python
from pydantic import BaseModel
from typing import Optional, List

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "China"

class Person(BaseModel):
    name: str
    age: int
    email: Optional[str] = None
    address: Address
    friends: List["Person"] = []  # 自引用

# 前向引用（需要 Python 3.9+ 或使用 from __future__ import annotations）
class Company(BaseModel):
    name: str
    CEO: Optional["Person"] = None
    employees: List["Person"] = []
```

### 3.4 组合类型

```python
from pydantic import BaseModel, Field
from typing import Union, Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class Status(str, Enum):
    pending = "pending"
    active = "active"
    completed = "completed"

class FlexibleModel(BaseModel):
    # 联合类型
    status: Union[str, int, Status]
    
    # 可选类型
    description: Optional[str] = None
    
    # 列表类型
    tags: List[str] = []
    
    # 复杂类型
    metadata: dict[str, any] = {}
    
    # 日期时间
    created_at: datetime = Field(default_factory=datetime.now)
    
    # UUID
    id: UUID
    
    # 嵌套联合类型
    data: Union[str, int, List[int], dict[str, str]] = None
```

### 3.5 继承与组合

```python
from pydantic import BaseModel
from typing import Optional

class BaseSchema(BaseModel):
    id: int
    created_at: str

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase, BaseSchema):
    is_active: bool = True
    
    class Config:
        from_attributes = True
```

### 3.6 数据转换

```python
from pydantic import BaseModel, SecretStr
from datetime import datetime
from typing import Optional
import json

class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime = datetime.now()

# 从字典创建
user_data = {"id": 1, "name": "John", "email": "john@example.com"}
user = User(**user_data)

# 转换为字典
user_dict = user.model_dump()
user_dict_json = user.model_dump_json()

# 从 JSON 创建
json_data = '{"id": 1, "name": "John", "email": "john@example.com"}'
user = User.model_validate_json(json_data)

# 复制和更新
user_updated = user.model_copy(update={"name": "Jane"})
```

---

## 4. 响应处理

### 4.1 响应模型

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None

# 定义响应模型
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    return {
        "name": "Widget",
        "description": "A high-quality widget",
        "price": 9.99,
    }

# 返回列表
@app.get("/users", response_model=List[User])
def get_users():
    return [
        {"id": 1, "username": "john", "email": "john@example.com"},
        {"id": 2, "username": "jane", "email": "jane@example.com"},
    ]

# 响应模型配置
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = {"name": "Widget", "price": 9.99}
    if item_id % 2 == 0:
        item["description"] = "Even item description"
    return item
```

### 4.2 状态码

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item():
    return {"message": "Item created"}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id == 0:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return {"item_id": item_id}
```

### 4.3 JSON 响应

```python
from fastapi import FastAPI, JSONResponse
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from datetime import datetime

app = FastAPI()

# 返回 JSON 响应
@app.get("/json")
def json_response():
    return {"message": "Hello", "timestamp": datetime.now()}

# 手动创建 JSONResponse
@app.get("/custom-json")
def custom_json():
    return JSONResponse(
        content={"message": "Custom response"},
        status_code=200,
        headers={"X-Custom-Header": "value"}
    )

# 纯文本响应
@app.get("/text", response_class=PlainTextResponse)
def text_response():
    return "Hello World"

# HTML 响应
@app.get("/html", response_class=HTMLResponse)
def html_response():
    return """
    <html>
        <head><title>Hello</title></head>
        <body><h1>Hello World</h1></body>
    </html>
    """

# 文件响应
@app.get("/file")
def file_response():
    return FileResponse(
        path="example.txt",
        filename="downloaded.txt",
        media_type="text/plain"
    )
```

### 4.4 流式响应

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

# SSE (Server-Sent Events) 流式响应
async def event_stream():
    for i in range(10):
        yield f"data: {i}\n\n"
        await asyncio.sleep(1)

@app.get("/stream")
async def main():
    return StreamingResponse(event_stream(), media_type="text/event-stream")

# 文件流式响应
async def file_iterator():
    with open("large_file.txt", "r") as f:
        for line in f:
            yield line

@app.get("/download")
async def download_file():
    return StreamingResponse(
        file_iterator(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=large_file.txt"}
    )
```

### 4.5 响应头

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/headers")
def custom_headers():
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "X-Custom-Header": "value",
            "X-Another-Header": "another value",
            "Cache-Control": "no-cache"
        }
    )

# 使用 Response 参数
from fastapi import Response

@app.get("/response-headers")
async def response_headers(response: Response):
    response.headers["X-Custom"] = "value"
    return {"message": "Done"}
```

---

## 5. 依赖注入系统

### 5.1 基础依赖注入

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 简单的依赖函数
def get_database():
    db = "database_connection"
    try:
        yield db
    finally:
        print("Closing database connection")

# 使用依赖
@app.get("/users")
def get_users(db: str = Depends(get_database)):
    return {"db": db, "users": []}

# 依赖函数带参数
def get_query_param(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}

@app.get("/items")
def get_items(params: dict = Depends(get_query_param)):
    return params
```

### 5.2 类作为依赖

```python
from fastapi import FastAPI, Depends

app = FastAPI()

class DatabaseConnection:
    def __init__(self):
        self.connection = "connected"
    
    def query(self, sql: str):
        return [f"Result for: {sql}"]

def get_db():
    db = DatabaseConnection()
    try:
        yield db
    finally:
        print("Connection closed")

@app.get("/items")
def get_items(db: DatabaseConnection = Depends(get_db)):
    results = db.query("SELECT * FROM items")
    return results
```

### 5.3 子依赖和依赖链

```python
from fastapi import FastAPI, Depends, Header

app = FastAPI()

# 子依赖
def query_params(q: str | None = None, page: int = 1):
    return {"q": q, "page": page}

def pagination(params: dict = Depends(query_params), limit: int = 10):
    params["limit"] = limit
    return params

@app.get("/search")
def search(p: dict = Depends(pagination)):
    return p

# Header 依赖
def get_user_agent(user_agent: str = Header(default=None)):
    return user_agent

@app.get("/info")
def info(user_agent: str = Depends(get_user_agent)):
    return {"user_agent": user_agent}

# 认证依赖
def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    return authorization.replace("Bearer ", "")

@app.get("/protected")
def protected(token: str = Depends(verify_token)):
    return {"token": token}
```

### 5.4 可缓存的依赖

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 默认情况下，依赖在每个请求中都会被调用
def get_settings():
    print("Loading settings...")  # 每次请求都会打印
    return {"debug": True}

# 使用缓存 - 在同一个请求中只调用一次
@app.get("/cached")
async def cached(settings: dict = Depends(get_settings)):
    return settings
```

### 5.5 依赖的多种用法

```python
from fastapi import Fastapi, Depends, HTTPException
from typing import Annotated

app = FastAPI()

# 可选依赖
def get_optional_dependency(q: str | None = None):
    return q

@app.get("/optional")
def optional_dep(q: str | None = Depends(get_optional_dependency)):
    return {"q": q}

# 多个依赖
def dependency_a():
    return "A"

def dependency_b():
    return "B"

@app.get("/multiple")
def multiple_deps(a: str = Depends(dependency_a), b: str = Depends(dependency_b)):
    return {"a": a, "b": b}

# 使用 Annotated (推荐方式)
@app.get("/annotated")
def annotated_dep(limit: Annotated[int, Depends(get_optional_dependency)] = 10):
    return {"limit": limit}
```

### 5.6 全局依赖

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 全局依赖 - 应用于所有路由
def common_parameters():
    return {"skip": 0, "limit": 10}

@app.get("/items")
def get_items(params: dict = Depends(common_parameters)):
    return params

# 可以为特定路由覆盖
@app.get("/special", dependencies=[])  # 不使用全局依赖
def get_special():
    return {"special": True}
```

---

## 6. 中间件

### 6.1 基础中间件

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI()

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Process time: {process_time:.4f}s")
    return response

# 响应时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 认证检查中间件
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/protected"):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized"}
            )
    return await call_next(request)
```

### 6.2 CORS 中间件

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 基础 CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 详细 CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_origin_regex="https://.*\.example\.com",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Request-ID",
    ],
    expose_headers=["X-Custom-Header"],
    max_age=600,
)
```

### 6.3 内置中间件

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# GZip 压缩
app.add_middleware(GZipMiddleware, minimum_size=1000)

# HTTPS 重定向 (仅在生产环境使用)
# app.add_middleware(HTTPSRedirectMiddleware)

# 受信任主机
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)

# 会话中间件
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key",
    max_age=3600,
)
```

---

## 7. 错误处理

### 7.1 HTTP 异常

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=400, detail="Item ID cannot be 0")
    if item_id < 0:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Item not found",
                "item_id": item_id,
                "suggestion": "Try a positive ID"
            }
        )
    return {"item_id": item_id}

# 使用状态码常量
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item name is required"
        )
    return {"name": name}
```

### 7.2 自定义异常处理器

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

app = FastAPI()

# 自定义异常处理器
class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Custom error: {exc.name}"}
    )

@app.get("/custom-error")
def trigger_custom_error():
    raise CustomException("Something went wrong")

# 验证错误处理器
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        }
    )

# Pydantic 验证错误
@app.exception_handler(ValidationError)
async def pydantic_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# 通用异常处理器
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

---

## 8. 安全与认证

### 8.1 API Key 认证

```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, APIKeyQuery

app = FastAPI()

# Header 中的 API Key
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != "secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/secure")
async def secure_endpoint(api_key: str = Depends(get_api_key)):
    return {"message": "Access granted", "api_key": api_key}

# Query 参数中的 API Key
api_key_query = APIKeyQuery(name="api-key")

@app.get("/secure-query")
async def secure_query_endpoint(api_key: str = Security(api_key_query)):
    return {"message": "Access granted"}
```

### 8.2 OAuth2 密码 Bearer

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 这里应该验证 token 并返回用户
    # 简化示例
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "john", "id": 1}

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}"}

# 登录端点
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 这里应该验证用户名和密码
    if form_data.username != "john" or form_data.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": "valid-token", "token_type": "bearer"}
```

### 8.3 JWT 认证

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    return User(username=token_data.username)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 验证用户凭据
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 8.4 依赖注入认证

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

app = FastAPI()

security = HTTPBearer()

async def verify_credentials(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=403, detail="Invalid authentication scheme")
    if credentials.credentials != "valid-token":
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials.credentials

@app.get("/protected")
async def protected_route(token: str = Depends(verify_credentials)):
    return {"token": token}
```

---

## 9. 数据库集成

### 9.1 SQLModel 基础

```python
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List

app = FastAPI()

# 创建数据库引擎
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

# 定义模型
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

# 创建表
SQLModel.metadata.create_all(engine)

# 路由示例
@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.get("/heroes/", response_model=List[Hero])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}
```

### 9.2 异步数据库操作

```python
from fastapi import FastAPI
from sqlmodel import SQLModel, Field
from typing import Optional, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

app = FastAPI()

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/items/")
async def create_item(item: Item):
    async with async_session_maker() as session:
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    async with async_session_maker() as session:
        result = await session.exec(select(Item))
        return result.all()
```

---

## 10. 异步编程

### 10.1 async/await 基础

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# 同步函数
@app.get("/sync")
def sync_endpoint():
    return {"message": "Sync response"}

# 异步函数
@app.get("/async")
async def async_endpoint():
    return {"message": "Async response"}

# 模拟异步操作
async def simulate_long_task():
    await asyncio.sleep(2)
    return "Task completed"

@app.get("/long-task")
async def long_task():
    result = await simulate_long_task()
    return {"result": result}

# 并发请求
async def fetch_data_from_api_1():
    await asyncio.sleep(1)
    return "Data from API 1"

async def fetch_data_from_api_2():
    await asyncio.sleep(1)
    return "Data from API 2"

@app.get("/concurrent")
async def concurrent_endpoints():
    results = await asyncio.gather(
        fetch_data_from_api_1(),
        fetch_data_from_api_2()
    )
    return {"api_1": results[0], "api_2": results[1]}
```

### 10.2 后台任务

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification will be sent"}

# 带延迟的后台任务
async def process_data(data: str):
    await asyncio.sleep(5)
    with open("processed.txt", "w") as f:
        f.write(f"Processed: {data}")

@app.post("/process")
async def process_item(item: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_data, item)
    return {"message": "Processing started"}
```

---

## 11. WebSocket

### 11.1 基础 WebSocket

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You said: {data}", websocket)
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left the chat")
```

---

## 12. 配置管理

### 12.1 Settings 配置

```python
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "default-secret-key"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

app = FastAPI()

@app.get("/")
def read_root():
    return {"app_name": settings.app_name}
```

### 12.2 多环境配置

```python
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

# 开发环境
class DevSettings(Settings):
    database_url: str = "sqlite:///./dev.db"
    debug: bool = True

# 生产环境  
class ProdSettings(Settings):
    database_url: str
    debug: bool = False

# 根据环境选择配置
import os

env = os.getenv("ENV", "dev")
if env == "prod":
    settings = ProdSettings()
else:
    settings = DevSettings()
```

---

## 13. 测试

### 13.1 基础单元测试

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "name": "Foo", "price": 50.2}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data
```

### 13.2 异步测试

```python
# test_async.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/async")
        assert response.status_code == 200
        assert response.json() == {"message": "Async response"}
```

### 13.3 测试数据库

```python
# test_database.py
import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from main import app, get_session
from typing import Generator

TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_create_item(client: TestClient):
    response = client.post("/items/", json={"name": "Test"})
    assert response.status_code == 200
```

### 13.4 测试覆盖

```bash
# 使用 Poetry 运行测试
poetry run pytest --cov=app --cov-report=html

# 只运行特定文件
poetry run pytest tests/test_api.py -v

# 只运行特定标记的测试
@pytest.mark.integration
def test_integration():
    pass

poetry run pytest -m integration
```

---

## 14. 部署与性能优化

### 14.1 Uvicorn 配置

```bash
# 使用 Poetry 运行
poetry run uvicorn main:app --host 0.0.0.0 --port 8000

# 基础启动
uvicorn main:app

# 生产环境配置
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --limit-concurrency 100 \
    --limit-max-requests 1000 \
    --timeout-keep-alive 5

# 使用配置文件
uvicorn main:app --factory \
    --loop uvloop \
    --http h11 \
    --log-config log_config.py
```

### 14.2 Gunicorn 配置

```bash
# 使用 Gunicorn 运行
gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

### 14.3 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装 Poetry
RUN pip install poetry

# 复制 poetry 相关文件
COPY pyproject.toml poetry.lock ./

# 安装依赖（不使用虚拟环境）
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
    restart: always

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 14.4 性能优化技巧

```python
# 1. 使用缓存
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(x):
    return x ** 2

# 2. 数据库连接池
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
)

# 3. 响应压缩
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 4. 分页处理
@app.get("/items")
async def get_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000)
):
    # 实现分页逻辑
    pass

# 5. 异步数据库查询
async def fetch_items():
    async with async_session_maker() as session:
        result = await session.execute(select(Item).limit(100))
        return result.scalars().all()
```

---

## 15. 最佳实践

### 15.1 项目结构

```
my_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── routers/             # 路由
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── utils/               # 工具函数
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── dependencies/       # 依赖注入
│       ├── __init__.py
│       └── auth.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   └── test_items.py
├── .env                     # 环境变量
├── pyproject.toml          # Poetry 配置
├── Dockerfile
└── docker-compose.yml
```

### 15.2 代码规范

```python
# 1. 使用类型注解
from typing import Optional

def get_user(user_id: int) -> Optional[dict]:
    pass

# 2. 使用 Pydantic 模型进行数据验证
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)

# 3. 使用枚举类型
from enum import Enum

class ItemStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

# 4. 统一的错误响应
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None

# 5. 文档字符串
def create_user(user: UserCreate) -> UserResponse:
    """
    创建新用户
    
    Args:
        user: 用户创建请求体
        
    Returns:
        创建的用户信息
        
    Raises:
        HTTPException: 当用户名已存在时
    """
    pass
```

### 15.3 安全性最佳实践

```python
# 1. 使用环境变量存储敏感信息
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    
    class Config:
        env_file = ".env"

# 2. 密码哈希
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 3. 速率限制
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
async def login(request: Request):
    pass

# 4. 输入验证和清理
from pydantic import field_validator

class UserInput(BaseModel):
    email: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        v = v.strip().lower()
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v
```

---

## 附录

### 常用命令

```bash
# ========== Poetry 命令（推荐）==========
# 初始化项目
poetry new fastapi-project
cd fastapi-project

# 安装 FastAPI 和 uvicorn
poetry add fastapi uvicorn

# 安装开发依赖
poetry add --group dev pytest pytest-asyncio httpx black ruff mypy

# 运行开发服务器
poetry run uvicorn main:app --reload

# 运行测试
poetry run pytest

# 类型检查
poetry run mypy app

# 代码格式化
poetry run black .
poetry run ruff check --fix .

# 构建项目
poetry build

# 发布到 PyPI
poetry publish

# 导出 requirements.txt
poetry export -f requirements.txt --output requirements.txt

# 激活虚拟环境
poetry shell

# 查看依赖树
poetry show --tree

# 检查过时的依赖
poetry show --outdated

# 更新依赖
poetry update
```

### 常用依赖

| 依赖 | 用途 |
|------|------|
| `fastapi` | Web 框架 |
| `uvicorn` | ASGI 服务器 |
| `pydantic` | 数据验证 |
| `pydantic-settings` | 配置管理 |
| `sqlmodel` | ORM |
| `python-jose` | JWT 编码 |
| `passlib` | 密码哈希 |
| `python-multipart` | 表单数据解析 |
| `aiofiles` | 异步文件操作 |
| `httpx` | HTTP 客户端 |
| `pytest` | 测试框架 |
| `pytest-asyncio` | 异步测试 |

### Poetry 项目配置模板 (pyproject.toml)

```toml
[tool.poetry]
name = "my-fastapi-project"
version = "0.1.0"
description = "FastAPI 项目描述"
authors = ["Your Name <your@email.com>"]
readme = "README.md"
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.100.0"
uvicorn = {version = "^0.23.0", extras = ["standard"]}
pydantic = "^2.0.0"
pydantic-settings = "^2.0.0"
sqlmodel = "^0.0.14"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
httpx = "^0.24.0"
black = "^23.7.0"
ruff = "^0.0.282"
mypy = "^1.5.0"

[tool.poetry.scripts]
app = "app.main:app"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

*文档更新时间：2026-03-18*
