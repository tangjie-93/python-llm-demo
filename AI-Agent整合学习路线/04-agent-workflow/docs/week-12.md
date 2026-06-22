# Level 4-1 | 第 12 周：Agent 核心概念与 ReAct 模式

> 🤖 **关卡名**：智能体觉醒 · Agent 基础
> 📅 **时间**：第 12 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 理解 Agent 的核心架构（LLM + Tools + Memory + Planning）
- [ ] 深入理解 ReAct 循环机制
- [ ] 能实现基础的 Tool Calling

## 每日学习安排

### 周一（3h）· Agent 核心概念

- [ ] 学习：Agent = LLM + 工具 + 记忆 + 规划 的自主程序
- [ ] 学习：Agent 与传统程序的区别（自主决策 vs 预设流程）
- [ ] 学习：Agent 工作流——感知→思考→行动→观察 循环
- [ ] 前端衔接：Agent = 带有状态机的前端应用；Tool = API 调用

### 周二（3h）· ReAct 模式深度剖析

- [ ] 学习：Thought（思考）→ Action（行动）→ Observation（观察）循环
- [ ] 学习：ReAct 与 CoT 的区别（ReAct 多了行动环节）
- [ ] 实践：用 LangChain 实现一个 ReAct Agent
- [ ] 前端衔接：ReAct = Event Loop 的事件循环；Action = Redux Action dispatch

### 周三（4h）· Function Calling / Tool Calling

- [ ] 学习：OpenAI Function Calling 机制
- [ ] 学习：Tool 定义格式（JSON Schema 描述参数）
- [ ] 学习：LLM 如何决策调用哪个 Tool、传什么参数
- [ ] 实践：定义一个「天气查询」Tool，让 Agent 自主调用
- [ ] 前端衔接：Tool 定义 = API Schema + Zod 验证

### 周四（4h）· 多 Tool 协同

- [ ] 学习：同时注册多个 Tool 给 Agent
- [ ] 学习：LLM 如何选择调用顺序（链式调用 vs 并行调用）
- [ ] 学习：Tool 调用结果的解析和处理
- [ ] 实践：给 Agent 添加「天气查询」「计算器」「搜索」三个 Tool

### 周五（4h）· 综合实战

- [ ] 综合练习：实现一个「旅行规划 Agent」
- [ ] 功能：查询天气 + 计算预算 + 搜索景点 → 生成旅行计划
- [ ] 练习：观察 Agent 的决策链（什么时候调用哪个工具）

## 知识点清单

- [ ] Agent = LLM + Tools + Memory + Planning
- [ ] Agent 与传统程序的区别
- [ ] ReAct 循环（Thought → Action → Observation）
- [ ] OpenAI Function Calling 格式
- [ ] Tool JSON Schema 定义
- [ ] Tool 调用解析与结果处理
- [ ] 多 Tool 协同与调用链
- [ ] LangChain `create_react_agent`

## 练习 / 作业

```python
# 作业 1：天气查询 Agent
# 实现一个带「天气查询」Tool 的 Agent
# 用户：「北京今天天气怎么样？适合跑步吗？」

# 作业 2：多功能 Agent
# 给 Agent 添加以下 Tools：
# - get_weather(city) → 天气信息
# - calculator(expression) → 计算结果
# - web_search(query) → 搜索摘要
# 用户提问：「上海和深圳哪个城市更热？」

# 作业 3：ReAct 循环可视化
# 将 Agent 的思考→行动→观察过程打印到终端，直观看到每一步的决策链
```

## 本周产出

- ✅ ReAct 循环可视化代码
- ✅ 旅行规划 Agent（多 Tool 协同）
- ✅ Agent 决策链日志分析

## 通关标志

- [ ] 能解释 Agent 四大核心组件（LLM/Tools/Memory/Planning）
- [ ] 能画出 ReAct 循环的流程图
- [ ] 能定义 Tool 并注册给 Agent
- [ ] 能观察和理解 Agent 的工具调用决策链

## 资源链接

| 资源 | 链接 |
|------|------|
| LangChain Agents 文档 | https://python.langchain.com/docs/concepts/agents/ |
| OpenAI Function Calling 指南 | https://platform.openai.com/docs/guides/function-calling |
| DeepLearning.AI: Functions, Tools and Agents | https://www.deeplearning.ai/short-courses/ |

## 前端技能衔接提示

- Agent 决策链 = Redux Middleware 日志（action sequence）
- Tool 定义 = API endpoint + Zod schema validation
- ReAct 循环 = React Render Loop （state → render → effect → state）
- Agent Memory = SessionStorage / Redux Persist
