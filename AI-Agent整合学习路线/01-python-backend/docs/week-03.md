# Level 1-3 | 第 3 周：FastAPI 框架 — 路由、模型与依赖注入

> 🚀 **关卡名**：疾风 API · FastAPI 精通
> 📅 **时间**：第 3 周 | ⏱️ **学时**：~20h

## 本周学习目标

- [ ] 能用 FastAPI 搭建完整的 RESTful API 服务
- [ ] 能使用 Pydantic 进行数据建模和运行时验证
- [ ] 理解 FastAPI 的依赖注入系统

## 每日学习安排

### 周一（4h）· FastAPI 快速上手

- [ ] 学习：FastAPI 安装与最小应用（`uvicorn` 启动）
- [ ] 学习：路由装饰器（`@app.get/post/put/delete`）
- [ ] 学习：路径参数、查询参数、请求体
- [ ] 体验：自动生成 Swagger UI（`/docs`）和 ReDoc（`/redoc`）
- [ ] 练习：创建 5 个路由端点（CRUD 模拟）
- [ ] 前端衔接：`@app.get("/items")` = `app.get("/items", handler)`（Express 风格）

### 周二（4h）· Pydantic 数据模型

- [ ] 学习：`BaseModel` 定义、字段类型、默认值
- [ ] 学习：`Field()` 验证器（`min_length`、`gt`、`pattern` 等）
- [ ] 学习：嵌套模型、`Optional` 字段、`Literal` 枚举
- [ ] 练习：定义复杂的嵌套数据模型（用户+订单+商品）
- [ ] 前端衔接：`BaseModel` = `interface` + `zod` 合体，声明即验证

### 周三（4h）· 依赖注入系统

- [ ] 学习：`Depends()` 依赖注入机制
- [ ] 学习：路径操作依赖、全局依赖
- [ ] 学习：依赖缓存、依赖嵌套
- [ ] 练习：实现 JWT 认证依赖（`get_current_user`）
- [ ] 前端衔接：`Depends()` = Express 中间件 + Vue `provide/inject`

### 周四（4h）· 中间件与异常处理

- [ ] 学习：FastAPI 中间件（CORS、日志、计时）
- [ ] 学习：`HTTPException` 异常处理
- [ ] 学习：自定义异常处理器
- [ ] 学习：`BackgroundTasks` 后台任务
- [ ] 练习：添加 CORS 中间件、请求日志中间件

### 周五（4h）· 综合实战 + 测试

- [ ] 学习：FastAPI `TestClient` + pytest
- [ ] 综合练习：构建「开发者笔记 API」基础骨架
- [ ] 练习：为 API 端点编写测试用例

## 知识点清单

- [ ] FastAPI 应用创建与 `uvicorn` 启动
- [ ] 路由定义（`@app.get/post/put/delete/patch`）
- [ ] 路径参数 / 查询参数 / 请求体
- [ ] 响应模型（`response_model`）
- [ ] Swagger UI（`/docs`）自动文档
- [ ] Pydantic `BaseModel` 数据模型定义
- [ ] `Field()` 字段验证（`min_length`/`gt`/`pattern`）
- [ ] 嵌套模型与 `Optional` 字段
- [ ] `Depends()` 依赖注入
- [ ] JWT 认证依赖实现
- [ ] CORS 中间件配置
- [ ] `HTTPException` 异常处理
- [ ] `BackgroundTasks` 后台任务
- [ ] `TestClient` + `pytest` 测试

## 练习 / 作业

```python
# 作业 1：笔记 API 骨架
# 实现以下端点（先不连数据库，用内存 dict 存储）：
# POST   /notes         创建笔记
# GET    /notes         笔记列表（支持分页 query params）
# GET    /notes/{id}    单条笔记
# PUT    /notes/{id}    更新笔记
# DELETE /notes/{id}    删除笔记

# 作业 2：用户认证
# 实现注册和登录端点，返回 JWT token
# 用 Depends() 保护笔记 API 端点

# 作业 3：测试覆盖
# 为以上端点编写至少 8 个单元测试
```

## 本周产出

- ✅ 一个功能完整的 FastAPI 笔记 API 骨架（内存版）
- ✅ JWT 认证模块
- ✅ 8+ 个 pytest 单元测试

## 通关标志

- [ ] 能独立创建 FastAPI 应用并定义路由
- [ ] 能用 Pydantic 定义请求/响应数据模型
- [ ] 能实现 Depends() 依赖注入
- [ ] 能在 Swagger UI 中测试 API
- [ ] 能编写 FastAPI 单元测试

## 资源链接

| 资源 | 链接 |
|------|------|
| FastAPI 官方教程 | https://fastapi.tiangolo.com/tutorial/ |
| Pydantic V2 文档 | https://docs.pydantic.dev/latest/ |
| FastAPI + JWT 教程 | https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ |

## 前端技能衔接提示

- RESTful API 设计经验 100% 复用 —— 路由设计、状态码、错误格式都一样
- Express/Koa 中间件模式 = FastAPI `Depends()`，思维模型相同
- Swagger UI 自动生成 = 前端 API 文档工具（Apifox/Postman），无需额外配置
- `BaseModel` 类型校验 = 前端 `zod`/`yup` schema 校验，但更强大（自动文档生成）
