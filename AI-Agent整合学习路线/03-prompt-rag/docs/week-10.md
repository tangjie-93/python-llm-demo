# Level 3-3 | 第 10 周：LangChain / LlamaIndex 框架

> 🔗 **关卡名**：框架驾驭者 · LangChain & LlamaIndex
> 📅 **时间**：第 10 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 能用 LangChain 搭建 RAG Chain
- [ ] 能用 LlamaIndex 快速构建索引和查询引擎
- [ ] 理解两个框架的定位差异和选型策略

## 每日学习安排

### 周一（4h）· LangChain 核心抽象

- [ ] 学习：LLM / ChatModel 抽象层
- [ ] 学习：PromptTemplate 提示模板
- [ ] 学习：Chain 链式调用（`|` pipe 操作符，LCEL）
- [ ] 实践：用 LCEL 搭建一个翻译 Chain
- [ ] 前端衔接：LCEL `|` pipe = Unix pipe 或 `|>` pipeline operator

### 周二（4h）· LangChain RAG Chain

- [ ] 学习：VectorStore / Retriever 抽象
- [ ] 学习：`RetrievalQA` Chain
- [ ] 学习：`create_history_aware_retriever`（上下文感知检索）
- [ ] 实践：搭建带多轮对话的 RAG Chain

### 周三（4h）· LlamaIndex 快速上手

- [ ] 学习：`SimpleDirectoryReader` 文档加载
- [ ] 学习：`VectorStoreIndex` 索引构建
- [ ] 学习：`QueryEngine` 查询引擎
- [ ] 实践：用 LlamaIndex 10 行代码搭建 RAG
- [ ] 前端衔接：LlamaIndex 的简洁 API = 前端框架的「快速原型」模式

### 周四（3h）· 框架对比 + 混合使用策略

- [ ] 对比：LangChain vs LlamaIndex 的设计哲学
- [ ] 学习：LangChain 擅长编排，LlamaIndex 擅长数据处理
- [ ] 实践：数据用 LlamaIndex 处理，编排用 LangChain

### 周五（3h）· 本地模型实践（可选）

- [ ] 了解：Ollama 本地模型部署
- [ ] 练习：用本地 Embedding 模型替代 OpenAI Embedding
- [ ] 了解：HuggingFace 模型生态

## 知识点清单

- [ ] LangChain ChatModel / LLM 抽象
- [ ] LCEL（LangChain Expression Language）pipe 语法
- [ ] PromptTemplate 模板
- [ ] VectorStore / Retriever 接口
- [ ] RetrievalQA Chain
- [ ] `create_history_aware_retriever`
- [ ] LlamaIndex `SimpleDirectoryReader`
- [ ] LlamaIndex `VectorStoreIndex`
- [ ] LlamaIndex `QueryEngine`
- [ ] 两个框架的定位差异
- [ ] Ollama 本地模型（了解）

## 练习 / 作业

```python
# 作业 1：LangChain RAG Chain
# 用 LangChain 搭建：技术文档加载 → 递归字符切分 → OpenAI Embeddings → Chroma
# → 带来源引用的 RetrievalQA Chain → 支持多轮对话

# 作业 2：LlamaIndex 快速 RAG
# 用 LlamaIndex 搭建同样的功能，对比代码量和开发体验

# 作业 3：混合方案
# LlamaIndex 做文档索引 + LangChain 做查询编排
# 体验「用对的框架做对的事」
```

## 本周产出

- ✅ LangChain RAG Chain 完整实现
- ✅ LlamaIndex RAG 快速原型
- ✅ 框架对比分析笔记

## 通关标志

- [ ] 能用 LangChain LCEL 搭建链式调用
- [ ] 能用 LlamaIndex 快速构建 RAG 查询引擎
- [ ] 能解释两个框架的定位差异

## 资源链接

| 资源 | 链接 |
|------|------|
| LangChain 官方文档 | https://python.langchain.com/ |
| LlamaIndex 官方文档 | https://docs.llamaindex.ai/ |
| DeepLearning.AI: LangChain for LLM App | https://www.deeplearning.ai/short-courses/ |
| Ollama | https://ollama.com/ |

## 前端技能衔接提示

- LangChain Chain = React 组件组合（`<A><B><C/></B></A>`）
- LCEL pipe = Unix pipe 或 RxJS pipe operator
- LlamaIndex 的快速原型 = 你用 Vite 搭一个 React App 的体验
