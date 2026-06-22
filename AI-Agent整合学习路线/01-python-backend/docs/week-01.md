# Level 1-1 | 第 1 周：Python 语法速成 — 类型与函数

> 🐍 **关卡名**：蛇语觉醒 · Python 基础语法
> 📅 **时间**：第 1 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [x] 能理解 Python 与 TypeScript 的核心语法差异
- [x] 能用 Python 编写函数、类、列表/字典操作的代码
- [x] 能在本地运行和调试 Python 脚本

## 每日学习安排

### 周一（3h）· 环境搭建 + 基础语法

- [ ] 安装 Python 3.12+、配置 VS Code Python 插件（Pylance、Ruff）
- [ ] 学习：变量、类型注解、`int`/`float`/`str`/`bool`/`None`
- [ ] 练习：对照 TS→Python 映射表，把熟悉的 TS 代码翻译成 Python
- [ ] 前端衔接：Python `int` = TS `number` 但有无限精度；Python `None` = TS `null`/`undefined` 合一

### 周二（3h）· 控制流 + 数据结构

- [ ] 学习：`if/elif/else`、`for/while`、`match-case`（Python 3.10+）
- [ ] 学习：`list`/`tuple`/`dict`/`set` 及其推导式
- [ ] 练习：用列表推导式重写 `Array.map()`/`filter()`/`reduce()`
- [ ] 前端衔接：Python 没有 `switch`，用 `match-case`；没有 `for(x of arr)`，只有 `for x in arr`

### 周三（4h）· 函数 + 类 + 模块

- [ ] 学习：`def` 函数、参数（位置/关键字/默认/可变）、`lambda`
- [ ] 学习：`class` 定义、`__init__`、`self`、继承、`@staticmethod`
- [ ] 学习：模块导入 `import`/`from...import` 与 `__name__`
- [ ] 练习：定义一个带类型注解的 class，导入到另一个文件使用
- [ ] 前端衔接：`self` = JS 的 `this` 但显式传入；`lambda` 只有一行

### 周四（4h）· Pythonic 特性 + 综合练习

- [ ] 学习：装饰器 `@`、上下文管理器 `with`、切片 `[::]`、解包 `*args/**kwargs`
- [ ] 学习：`enumerate`/`zip`/`map`/`filter`/`sorted`
- [ ] 练习：写一个计时装饰器；用 `with open()` 读写文件
- [ ] 综合练习：实现一个简单的 CLI 待办事项（TODO list）

### 周五（4h）· 综合实战 + 复习

- [ ] 综合练习：将前端项目中的一段 TS 工具函数库翻译为 Python 模块
- [ ] 练习：编写 `pytest` 测试用例（至少 5 个）
- [ ] 成果检验：完成本周所有练习题

## 知识点清单

- [ ] Python 变量与基本类型（`int`/`float`/`str`/`bool`/`None`）
- [ ] 类型注解（`x: int = 1`）与 `mypy` 类型检查
- [ ] 字符串操作（f-string、切片、常用方法）
- [ ] 控制流（`if/elif/else`、`for/while`、`match-case`）
- [ ] 列表/元组/字典/集合（创建、推导式、常用方法）
- [ ] 函数定义（参数类型、返回值类型、`lambda`）
- [ ] 类与继承（`class`、`__init__`、`self`、`super()`）
- [ ] 模块系统（`import`/`from...import`/包）
- [ ] 装饰器（`@` 语法、闭包原理）
- [ ] 上下文管理器（`with` 语句、`__enter__`/`__exit__`）
- [ ] 异常处理（`try/except/finally/raise`）
- [ ] 切片语法（`a[1:4]`、`a[::-1]`）
- [ ] `*args`/`**kwargs` 解包

## 练习 / 作业

```python
# 作业 1：TS → Python 翻译
# 把以下 TS 代码翻译为 Python：
# function groupBy<T>(arr: T[], key: keyof T): Record<string, T[]> { ... }

# 作业 2：装饰器实现
# 写一个 @retry(n) 装饰器，函数执行失败时自动重试 n 次

# 作业 3：CLI 小工具
# 实现一个命令行 Markdown 字数统计工具：
# - 读取 .md 文件
# - 统计中文字数、英文单词数、代码块行数
# - 输出统计报告
```

## 本周产出

- ✅ 一个本地可运行的 Python 练习仓库（含 10+ 个练习文件）
- ✅ 1 个 TS 工具库 → Python 翻译模块
- ✅ 1 个 CLI 小工具（Markdown 字数统计）

## 通关标志

- [ ] 能独立编写带类型注解的 Python 函数
- [ ] 能使用推导式替代 `map`/`filter`/`reduce`
- [ ] 能解释装饰器的执行原理
- [ ] 能用 `with` 管理文件和资源
- [ ] 能区分 `list`/`tuple`/`dict`/`set` 的适用场景

## 资源链接

| 资源 | 链接 |
|------|------|
| Python 官方教程 | https://docs.python.org/3/tutorial/ |
| freeCodeCamp: Python for Beginners | https://www.youtube.com/@freecodecamp |
| 《Python编程：从入门到实践》 | 快速过基础语法章节（第 1-9 章） |

## 前端技能衔接提示

- TS 的类型注解习惯 = Python type hints，基本零学习曲线
- `array.map(x => x*2)` → `[x*2 for x in arr]`，思维方向一致
- `try/catch/finally` 语法几乎一样，只是关键字不同（`except` vs `catch`）
