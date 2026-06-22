# 04. Agent 工作流与多步骤任务

## 学习目标

这一阶段要解决的问题是：Agent 如何稳定完成长任务。

短任务可以一次模型调用完成，长任务通常需要：

- 多个步骤
- 多个工具
- 中间状态
- 用户确认
- 失败重试
- 暂停和恢复

## 1. Workflow 与 Agent 的区别

Workflow 是确定性流程，Agent 是动态决策。

Workflow 适合：

- 步骤固定
- 规则明确
- 合规要求高
- 失败处理明确

Agent 适合：

- 用户目标开放
- 需要动态选择工具
- 需要理解自然语言
- 需要综合多个信息源

生产系统里通常是二者结合：

> Workflow 控制主流程，Agent 负责理解、生成、选择和总结。

## 2. 状态机

状态机用于描述任务当前在哪一步。

示例状态：

- `created`
- `planning`
- `waiting_for_user`
- `running_tool`
- `reviewing`
- `completed`
- `failed`
- `cancelled`

为什么重要：

- 前端可以展示进度
- 后端可以恢复任务
- 失败时知道从哪里继续
- 审计日志更清晰

## 3. Checkpoint

Checkpoint 是任务执行过程中的保存点。

需要保存：

- 当前步骤
- 用户输入
- 模型输出
- 工具调用参数
- 工具结果
- 用户确认记录
- 错误信息

适用场景：

- 长任务中断后恢复
- 用户刷新页面
- 后端进程重启
- 工具调用失败后重试

## 4. Human-in-the-loop

长任务里，人类确认不是额外功能，而是核心控制点。

常见确认点：

- 执行计划确认
- 写操作确认
- 权限升级确认
- 最终结果确认
- 异常分支选择

Vue 交互建议：

- 用步骤条展示任务位置
- 用 Drawer 展示待确认内容
- 用户可以通过“批准、修改、拒绝”三种方式处理
- 所有确认写入审计日志

## 5. Planner / Executor / Reviewer

这是常见 Agent 分工模式。

Planner：

- 理解目标
- 拆分步骤
- 选择策略

Executor：

- 调用工具
- 执行步骤
- 记录结果

Reviewer：

- 检查结果是否满足目标
- 发现遗漏
- 给出修正建议

注意：这不一定需要三个模型实例，也可以是同一个模型在不同 prompt 和状态下扮演不同职责。

## 6. LangGraph

LangGraph 适合构建有状态、多步骤、可恢复的 Agent 工作流。

重点学习：

- graph
- node
- edge
- state
- checkpoint
- conditional routing
- human-in-the-loop

学习方式：

1. 先画出任务状态图
2. 再把每个状态实现成 node
3. 给状态定义 schema
4. 加入 checkpoint
5. 最后再接入真实工具

## 7. OpenAI Agents SDK

OpenAI Agents SDK 适合学习 Agent 原语：

- Agent
- Tool
- Handoff
- Guardrail
- Session
- Tracing

学习重点：

- 如何定义工具
- 如何让 Agent handoff 给另一个 Agent
- 如何加输入 / 输出 guardrail
- 如何查看 tracing
- 如何管理 session

## 8. AI 项目经理 Agent 项目

输入：

```text
帮我把这个需求拆成开发任务，分析影响范围，生成技术方案，创建 GitHub issue，最后输出排期建议。
```

流程：

1. 理解需求
2. 读取项目文档
3. 分析影响范围
4. 生成任务拆分
5. 用户确认
6. 创建 issues
7. 生成排期和风险
8. 输出总结

Vue 页面：

- 需求输入区
- 任务步骤 Timeline
- 文档引用面板
- Issue 草稿列表
- 用户确认 Drawer
- 最终报告预览

## 9. 学习路线

1. 用普通代码写固定 workflow
2. 给每一步加状态
3. 加入中断和恢复
4. 引入模型做任务拆解
5. 引入工具调用
6. 加入用户确认
7. 用 LangGraph 或 Agents SDK 重构

## 10. 本阶段学习资源

- LangGraph 文档：https://langchain-ai.github.io/langgraph/
- OpenAI Agents SDK：https://openai.github.io/openai-agents-python/
- LangChain Agents：https://docs.langchain.com/
- Vue Flow：https://vueflow.dev/
- Pinia：https://pinia.vuejs.org/

