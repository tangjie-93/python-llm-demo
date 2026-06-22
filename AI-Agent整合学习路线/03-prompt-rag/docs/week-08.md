# Level 3-1 | 第 8 周：Prompt Engineering 技术体系

> 💬 **关卡名**：低语智者 · Prompt 工程精通
> 📅 **时间**：第 8 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 掌握 7 种核心 Prompt 工程技术的使用场景
- [ ] 能根据任务类型选择合适的 Prompt 策略
- [ ] 能编写结构化的、可复用的 Prompt 模板

## 每日学习安排

### 周一（3h）· Zero-shot / Few-shot Prompting

- [ ] 学习：Zero-shot 直接提问——不放示例
- [ ] 学习：Few-shot 示例引导——2-5 个样例定格式
- [ ] 实验：同一任务 Zero-shot vs Few-shot 效果对比
- [ ] 前端衔接：Few-shot = 前端代码示例文档（给出 few examples 再让 AI 写）

### 周二（3h）· Chain-of-Thought / Tree-of-Thought

- [ ] 学习：CoT 逐步推理——「让我们一步步思考」
- [ ] 学习：ToT 多路径探索——生成 N 个方案再评估
- [ ] 练习：用 CoT 解决复杂逻辑推理问题
- [ ] 前端衔接：CoT = 代码调试中的逐步断点（step by step debugging）

### 周三（4h）· ReAct + Self-Consistency

- [ ] 学习：ReAct 模式——思考→行动→观察→思考 循环
- [ ] 学习：Self-Consistency——多次采样取共识
- [ ] 实践：用 ReAct 模式设计一个「购物助手」Prompt
- [ ] 前端衔接：ReAct = Event Loop 的事件循环处理

### 周四（4h）· Structured Output + 实战

- [ ] 学习：约束输出格式（JSON Schema / Function Calling）
- [ ] 学习：角色扮演 Prompt（Persona-based Prompting）
- [ ] 学习：Prompt 模板管理（Jinja2 模板引擎）
- [ ] 实践：用 Jinja2 组织可复用的 Prompt 模板库

### 周五（4h）· 综合实验 + 最佳实践

- [ ] 综合实验：对比多种 Prompt 策略在同一任务上的表现
- [ ] 学习：Prompt 最佳实践（清晰指令、给出参考文本、分解复杂任务）
- [ ] 制作：个人 Prompt 工具箱（模板集合）

## 知识点清单

- [ ] Zero-shot Prompting
- [ ] Few-shot Prompting
- [ ] Chain-of-Thought（CoT）
- [ ] Tree-of-Thought（ToT）
- [ ] ReAct（推理+行动交替）
- [ ] Self-Consistency（多次采样+投票）
- [ ] Structured Output（约束 JSON 格式）
- [ ] Persona-based Prompting（角色扮演）
- [ ] Jinja2 模板引擎
- [ ] Prompt 最佳实践原则

## 练习 / 作业

```python
# 作业 1：Prompt 策略对比实验
# 选取 3 种不同的任务（翻译、推理、代码生成）
# 用 3 种 Prompt 策略（Zero-shot/Few-shot/CoT）分别测试
# 对比输出质量，输出对比报告

# 作业 2：Prompt 模板库
# 用 Jinja2 搭建一个可复用的 Prompt 模板库
# 包含：代码审查模板、翻译模板、JSON 提取模板

# 作业 3：ReAct 模式实现
# 用纯 Prompt 实现一个 ReAct 循环（不带工具调用）
# 观察模型如何自主「思考→行动→观察」
```

## 本周产出

- ✅ Prompt 策略对比实验报告
- ✅ Jinja2 Prompt 模板库
- ✅ ReAct 实验代码

## 通关标志

- [ ] 能区分 5+ 种 Prompt 策略的适用场景
- [ ] 能写出高质量的 Few-shot 示例
- [ ] 能设计结构化输出的 Prompt
- [ ] 能解释 ReAct 循环的工作原理

## 资源链接

| 资源 | 链接 |
|------|------|
| Prompt Engineering Guide | https://www.promptingguide.ai/ |
| OpenAI Prompt Engineering | https://platform.openai.com/docs/guides/prompt-engineering |
| Anthropic Prompt Library | https://docs.anthropic.com/en/prompt-library |

## 前端技能衔接提示

- Prompt 模板 = 前端组件模板（props → 不同渲染结果）
- Few-shot 示例 = Storybook 中的组件示例（展示不同用法）
- Prompt 版本管理 = 前端的组件版本管理
- 结构化输出约束 = `zod` schema 校验（确保输出格式符合预期）
