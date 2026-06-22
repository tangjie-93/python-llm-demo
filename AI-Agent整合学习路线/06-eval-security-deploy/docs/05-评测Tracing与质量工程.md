# 05. 评测、Tracing 与质量工程

## 学习目标

这一阶段的目标是建立持续改进 Agent 的能力。没有评测和 Tracing，Agent 出错只能靠猜。

## 1. 为什么需要 Eval

LLM 应用不是只要“能跑”就行。每次改 prompt、换模型、改 chunk 策略、加工具，都可能引入回归。

Eval 用来回答：

- 回答是否正确
- 检索是否命中
- 工具是否选对
- 参数是否正确
- 成本是否升高
- 延迟是否变慢
- 安全规则是否被绕过

## 2. Golden Dataset

Golden dataset 是人工准备的一组标准测试集。

建议包含：

- 用户问题
- 期望答案
- 参考来源
- 期望工具
- 期望参数
- 不应该发生的行为

示例：

```json
{
  "question": "如何申请发票？",
  "expected_answer": "用户需要在订单详情页提交发票申请。",
  "expected_sources": ["invoice_policy.md"],
  "must_not": ["编造客服电话"]
}
```

## 3. Retrieval Eval

评估检索质量。

指标：

- Recall：正确文档是否被召回
- Precision：召回结果里相关内容比例
- MRR：正确结果排在多靠前
- nDCG：排序质量

常见失败：

- chunk 太碎
- metadata 过滤错误
- embedding 不适合领域术语
- query rewrite 改坏了用户问题
- top_k 太小

## 4. Answer Eval

评估最终答案。

维度：

- 是否正确
- 是否完整
- 是否引用来源
- 是否出现幻觉
- 是否遵守格式
- 是否承认不知道

可以结合：

- 规则校验
- 人工标注
- LLM-as-judge

注意：LLM-as-judge 不能完全替代人工评测，尤其是高风险业务。

## 5. Tool Calling Eval

评估工具调用。

维度：

- 是否调用了正确工具
- 是否不该调用工具时保持回答
- 参数是否正确
- 调用顺序是否正确
- 工具失败后是否恢复
- 是否绕过确认

示例 case：

```json
{
  "input": "帮我给客户 123 发一封催款邮件",
  "expected_tools": ["get_customer", "draft_email"],
  "forbidden_tools": ["send_email"],
  "requires_confirmation": true
}
```

## 6. Trajectory Eval

Trajectory 是 Agent 的中间执行轨迹。

需要检查：

- 是否重复调用同一工具
- 是否陷入循环
- 是否忽略工具错误
- 是否越权
- 是否遗漏关键步骤

## 7. Tracing

Tracing 记录一次 Agent 运行的全过程。

建议记录：

- 用户输入
- 模型名称
- prompt 版本
- 输入 / 输出 token
- 工具调用
- 工具参数
- 工具耗时
- 工具结果摘要
- 错误信息
- 总成本
- 总耗时

Vue Dashboard 建议：

- 会话列表
- 单次运行 Timeline
- token 和成本图表
- 工具调用详情
- 失败原因分类
- eval 分数趋势

## 8. Failure Taxonomy

建立失败分类能帮助你系统优化。

建议分类：

- Intent：意图理解错误
- Retrieval：检索失败
- Grounding：没有基于资料回答
- Tool Selection：工具选择错误
- Tool Argument：参数错误
- Permission：权限错误
- UX：用户无法理解状态
- Latency：响应太慢
- Cost：成本过高
- Safety：安全风险

## 9. Eval Dashboard 项目

功能：

- 管理测试集
- 运行评测
- 查看分数趋势
- 对比不同 prompt 版本
- 查看失败样本
- 标注失败原因
- 导出报告

技术建议：

- Vue 3 + ECharts
- FastAPI
- PostgreSQL
- 后台任务队列
- LLM-as-judge 可作为辅助

## 10. 学习路线

1. 先给 RAG 项目准备 30 个问题
2. 手工标注参考答案和来源
3. 写脚本自动运行
4. 加入 retrieval eval
5. 加入 answer eval
6. 加入 tool calling eval
7. 做 Vue dashboard

## 11. 本阶段学习资源

- OpenAI Evals 文档：https://platform.openai.com/docs/guides/evals
- OpenAI Agents SDK Tracing：https://openai.github.io/openai-agents-python/tracing/
- LangSmith：https://docs.smith.langchain.com/
- promptfoo：https://www.promptfoo.dev/docs/
- Ragas：https://docs.ragas.io/
- ECharts：https://echarts.apache.org/

