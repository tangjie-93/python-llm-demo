# Level 6-1 | 第 20 周：Agent 可观测性与成本控制

> 📊 **关卡名**：全视之眼 · 可观测性系统
> 📅 **时间**：第 20 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 能用 LangSmith / LangFuse 追踪 Agent 调用链路
- [ ] 能分析 Token 用量和成本
- [ ] 能设计成本控制策略

## 每日学习安排

### 周一（3h）· 可观测性概念

- [ ] 学习：为什么 Agent 需要可观测性（调用链路复杂、成本不透明、难以调试）
- [ ] 学习：核心指标——Token 用量、延迟、LLM 调用次数、成功率、成本
- [ ] 学习：Trace / Span 概念
- [ ] 前端衔接：可观测性 = 前端 Lighthouse / Web Vitals / Sentry

### 周二（4h）· LangSmith 集成

- [ ] 学习：LangSmith 平台功能（Trace、Feedback、Dataset）
- [ ] 实践：配置环境变量，自动追踪 LangChain/LangGraph 调用
- [ ] 实践：在 Dashboard 中查看 Trace 调用链
- [ ] 实践：添加用户反馈收集

### 周三（4h）· LangFuse 集成

- [ ] 学习：LangFuse 开源方案
- [ ] 学习：自托管 vs 云服务
- [ ] 实践：集成 LangFuse 到 Agent 项目
- [ ] 对比：LangSmith vs LangFuse 的选型考量

### 周四（4h）· 成本控制

- [ ] 学习：Token 计数——用 `tiktoken` 精确计算
- [ ] 学习：多模型成本对比（GPT-4o vs DeepSeek vs GPT-4o-mini）
- [ ] 理解：Input vs Output Token 的价格差异
- [ ] 实践：实现 CostController（预算管理、每日限额、成本预估）
- [ ] 实现：简单任务用小模型、复杂任务用大模型的 ModelRouter

### 周五（3h）· 成本优化策略

- [ ] 学习：Prompt 缓存策略—相同输入直接返回缓存
- [ ] 学习：语义缓存—相似问题命中缓存
- [ ] 学习：模型降级策略—大模型不可用时自动降级
- [ ] 实践：在项目中实现缓存和降级

## 知识点清单

- [ ] Agent 可观测性四大指标
- [ ] LangSmith Trace 追踪
- [ ] LangFuse 开源方案
- [ ] Token 计数与成本估算
- [ ] 多模型成本对比
- [ ] CostController 预算管理
- [ ] ModelRouter 模型选择
- [ ] Prompt 缓存与语义缓存
- [ ] 模型降级策略

## 本周产出

- ✅ LangSmith/LangFuse 可观测性集成
- ✅ CostController + ModelRouter 实现
- ✅ Prompt 缓存机制

## 通关标志

- [ ] 能在可观测性平台查看 Agent 调用链路
- [ ] 能计算每次请求的 Token 用量和成本
- [ ] 能实现日预算控制和模型降级
- [ ] 能实现 Prompt 缓存减少重复调用

## 资源链接

| 资源 | 链接 |
|------|------|
| LangSmith 文档 | https://docs.smith.langchain.com/ |
| LangFuse 文档 | https://langfuse.com/docs |
| tiktoken | https://github.com/openai/tiktoken |
| OpenAI Pricing | https://openai.com/api/pricing/ |

## 前端技能衔接提示

- Agent Trace = Redux DevTools 的 Action 时间线
- 成本监控 Dashboard = 前端数据看板（ECharts/Chart.js）
- 性能指标 = Web Vitals（FCP/LCP/CLS）
- 缓存策略 = 前端 HTTP 缓存 / Service Worker 缓存
