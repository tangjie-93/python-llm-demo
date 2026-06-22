# Level 2-2 | 第 6 周：LLM API 调用 — OpenAI SDK 实战

> 🔌 **关卡名**：API 召唤师 · 调用大模型
> 📅 **时间**：第 6 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 能熟练使用 OpenAI SDK 调用对话 API
- [ ] 理解 System Prompt、Temperature 等关键参数
- [ ] 能实现流式输出和错误处理

## 每日学习安排

### 周一（3h）· OpenAI SDK 基础

- [ ] 学习：OpenAI 客户端初始化（API Key、Base URL）
- [ ] 学习：`chat.completions.create()` 基础对话调用
- [ ] 学习：Message 三种角色（`system` / `user` / `assistant`）
- [ ] 实践：用 DeepSeek API（兼容 OpenAI 格式）完成第一次调用
- [ ] 前端衔接：API 调用模式 = 前端 `fetch`/`axios`，完全一样

### 周二（3h）· 参数调优实验

- [ ] 学习：`temperature` 实验（0 → 0.5 → 1.0 → 1.5）
- [ ] 学习：`max_tokens` 参数和输出截断
- [ ] 学习：`top_p` 核采样
- [ ] 练习：同一问题在不同 temperature 下的输出对比实验
- [ ] 前端衔接：Temperature 调参 = 前端动画中的贝塞尔曲线调参

### 周三（4h）· 流式输出 + 多轮对话

- [ ] 学习：`stream=True` 流式输出
- [ ] 学习：SSE-like 的 chunk 处理
- [ ] 学习：多轮对话的消息历史管理
- [ ] 实践：实现一个命令行对话机器人（ChatGPT-like CLI）
- [ ] 前端衔接：流式输出 = SSE (Server-Sent Events) + `EventSource`

### 周四（4h）· 错误处理 + 进阶调用

- [ ] 学习：API 错误码处理（Rate Limit、Token Limit、Content Filter）
- [ ] 学习：重试策略（指数退避）
- [ ] 学习：Vision API（图片理解）调用
- [ ] 实践：为 API 调用添加完整的异常处理
- [ ] 前端衔接：错误处理 = `try/catch` + axios interceptor，套路一样

### 周五（4h）· 多模型适配 + CLI 起步

- [ ] 学习：配置多模型（通过环境变量切换 OpenAI / DeepSeek / 其他）
- [ ] 学习：结构化配置管理（类比前端的 `.env` + config 中心）
- [ ] 实践：CLI 工具骨架搭建（`click` 或 `typer`）

## 知识点清单

- [ ] OpenAI `chat.completions.create()` API 调用
- [ ] Message 角色（system / user / assistant）
- [ ] `temperature` / `max_tokens` / `top_p` 参数
- [ ] `stream=True` 流式输出处理
- [ ] 多轮对话的消息历史管理
- [ ] 常见 API 错误码与重试策略
- [ ] Vision API（图片理解）
- [ ] 多模型配置与环境变量管理
- [ ] `click` / `typer` CLI 框架入门

## 练习 / 作业

```python
# 作业 1：Temperature 实验报告
# 用同一问题分别在 temperature = 0, 0.3, 0.7, 1.0, 1.5 下运行 3 次
# 对比输出的一致性和创造性，记录观察

# 作业 2：CLI 对话机器人
# 实现一个终端 ChatGPT：
# $ python chatbot.py
# You: 介绍一下 Python
# AI: Python 是一门...
# 支持多轮对话（记住上下文）、流式输出

# 作业 3：API 配置切换
# 实现通过环境变量 .env 切换模型提供商
```

## 本周产出

- ✅ Temperature 调参实验报告
- ✅ CLI 多轮对话机器人
- ✅ 多模型环境变量配置模板

## 通关标志

- [ ] 能独立调用 OpenAI 兼容 API 进行对话
- [ ] 能根据任务选择适当的 temperature 值
- [ ] 能实现流式输出交互
- [ ] 能处理常见 API 错误（Rate Limit / Token Limit）
- [ ] 能配置和切换不同模型提供商

## 资源链接

| 资源 | 链接 |
|------|------|
| OpenAI API 文档 | https://platform.openai.com/docs/api-reference/chat |
| DeepSeek API 文档 | https://platform.deepseek.com/api-docs/ |
| Anthropic API 文档 | https://docs.anthropic.com/en/api/ |
| click 文档 | https://click.palletsprojects.com/ |
| typer 文档 | https://typer.tiangolo.com/ |

## 前端技能衔接提示

- API Key 管理 = 前端环境变量管理（`.env` → `NEXT_PUBLIC_*`）
- 流式输出处理 = EventSource / SSE 的处理模式
- 多轮对话状态管理 = Redux/Vuex 消息列表状态
- retry 策略 = axios retry interceptor 的同款逻辑
