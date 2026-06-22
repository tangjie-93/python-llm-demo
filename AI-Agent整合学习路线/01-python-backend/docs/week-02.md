# Level 1-2 | 第 2 周：Python 工程化 — 包管理与异步基础

> 📦 **关卡名**：包管理器大师 · 工程化入门
> 📅 **时间**：第 2 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 能用 `uv` 管理项目依赖和虚拟环境
- [ ] 理解 Python 的 `asyncio` 异步模型
- [ ] 能编写异步 HTTP 请求和并发处理代码

## 每日学习安排

### 周一（3h）· 包管理工具链

- [ ] 学习：`pip` vs `uv` vs `poetry` 对比
- [ ] 学习：虚拟环境原理（`venv`、`.venv`）
- [ ] 实践：用 `uv init` 创建项目，`uv add` 添加依赖，`uv sync` 同步
- [ ] 理解：`pyproject.toml` 项目配置（类比 `package.json`）
- [ ] 前端衔接：`uv` = pnpm/yarn；`pyproject.toml` = `package.json`

### 周二（3h）· async/await 核心

- [ ] 学习：`async def` 协程定义、`await` 等待
- [ ] 学习：事件循环概念（`asyncio.run()`）
- [ ] 对比：JS `Promise` 链 vs Python `await` 链
- [ ] 练习：写异步函数，用 `asyncio.run()` 运行

### 周三（4h）· asyncio 并发模式

- [ ] 学习：`asyncio.gather()` — 类比 `Promise.all()`
- [ ] 学习：`asyncio.create_task()` — 类比 `Promise` 不 await
- [ ] 学习：`asyncio.wait_for()` 超时控制
- [ ] 学习：`asyncio.as_completed()` 按完成顺序处理
- [ ] 练习：并发请求多个 URL，汇总结果

### 周四（4h）· HTTP 客户端 + 实战

- [ ] 学习：`httpx` 异步 HTTP 客户端（类比 `fetch`/`axios`）
- [ ] 学习：`aiofiles` 异步文件读写
- [ ] 实践：写一个异步网络爬虫（并发抓取多个页面）

### 周五（4h）· 综合实战 + 复习

- [ ] 综合练习：异步批量 API 调用 + 结果缓存
- [ ] 了解：Python 的 GIL 概念与多线程/多进程区别
- [ ] 成果检验：对比 JS 和 Python 的异步执行，写一篇对比笔记

## 知识点清单

- [ ] `uv` 包管理器（init / add / sync / run）
- [ ] `pyproject.toml` 项目配置
- [ ] 虚拟环境（`.venv`）原理与使用
- [ ] `pip` 基本使用（传统方式理解）
- [ ] `async def` / `await` 协程机制
- [ ] `asyncio.run()` 事件循环启动
- [ ] `asyncio.gather()` 并发等待
- [ ] `asyncio.create_task()` 后台任务
- [ ] `asyncio.wait_for()` 超时机制
- [ ] `httpx.AsyncClient` 异步 HTTP 请求
- [ ] `aiofiles` 异步文件 I/O
- [ ] GIL 概念了解（非必须深入）

## 练习 / 作业

```python
# 作业 1：批量 API 调用
# 用 asyncio + httpx 并发请求 10 个 API 端点
# 要求：超时 5 秒、错误重试 3 次、汇总结果到 JSON

# 作业 2：项目初始化
# 用 uv 创建一个新项目结构：
# my-project/
#   pyproject.toml
#   src/my_project/main.py
#   tests/test_main.py
# 添加 fastapi、httpx、pytest 依赖

# 作业 3：前端概念映射笔记
# 写一篇短笔记（自己做知识库用）：
# - npm install → uv add
# - node_modules → .venv
# - package.json → pyproject.toml
# - async function → async def
# - Promise.all → asyncio.gather
```

## 本周产出

- ✅ 一个用 `uv` 管理的标准化 Python 项目
- ✅ 1 个异步网络爬虫脚本
- ✅ 1 篇前端→Python 异步概念映射笔记

## 通关标志

- [ ] 能独立用 `uv` 创建和管理 Python 项目
- [ ] 能解释 `asyncio.gather` 与 `Promise.all` 的异同
- [ ] 能用 `httpx` 编写异步 HTTP 客户端
- [ ] 能理解 Python 事件循环的基本模型

## 资源链接

| 资源 | 链接 |
|------|------|
| uv 官方文档 | https://docs.astral.sh/uv/ |
| Python asyncio 官方文档 | https://docs.python.org/3/library/asyncio.html |
| httpx 文档 | https://www.python-httpx.org/ |
| Real Python: Async IO | https://realpython.com/async-io-python/ |

## 前端技能衔接提示

- `Promise.all([a, b])` = `await asyncio.gather(a(), b())`，几乎一字对译
- `Promise.race` ≈ `asyncio.wait(tasks, return_when=FIRST_COMPLETED)`
- `setTimeout(fn, 0)` ≈ `asyncio.sleep(0)` — 让出控制权
- JS 单线程事件循环 ≈ Python 单线程事件循环（但 Python 有 GIL）
