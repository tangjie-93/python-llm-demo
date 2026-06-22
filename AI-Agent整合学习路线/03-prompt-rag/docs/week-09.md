# Level 3-2 | 第 9 周：RAG 核心 — Embedding、向量库与文档处理

> 📚 **关卡名**：知识编织者 · RAG 入门
> 📅 **时间**：第 9 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 理解 RAG 的完整工作流程
- [ ] 能对文档进行切分、向量化、检索
- [ ] 能搭建基础的问答流程

## 每日学习安排

### 周一（3h）· RAG 概念与工作流

- [ ] 学习：RAG 完整流程（文档加载→切分→Embedding→存储→检索→生成）
- [ ] 理解：为什么 LLM 需要 RAG（知识截止日期、幻觉、私有知识）
- [ ] 实践：用 OpenAI Embedding 对一段文本向量化
- [ ] 前端衔接：RAG = 前端应用的「数据层」——API 拿不到的数据从本地向量库查

### 周二（3h）· 文档加载与切分

- [ ] 学习：文档加载器（TXT / Markdown / PDF / HTML）
- [ ] 学习：Chunking 策略对比（固定大小 / 递归字符 / 语义 / 代码感知）
- [ ] 学习：`chunk_size` 与 `chunk_overlap` 的权衡
- [ ] 实践：用 `LangChain Text Splitter` 对不同文档切分

### 周三（4h）· 向量数据库入门

- [ ] 学习：Chroma 向量数据库（嵌入式、零配置）
- [ ] 学习：向量插入、检索、元数据过滤
- [ ] 实践：将切分后的文档存入 Chroma，进行相似度检索
- [ ] 前端衔接：Chroma = `json-server`——快速原型用；Qdrant = Supabase——生产用

### 周四（4h）· 检索策略

- [ ] 学习：相似度检索（Cosine / Euclidean / Dot Product）
- [ ] 学习：MMR（最大边际相关性）检索——提高多样性
- [ ] 学习：元数据过滤——精准缩小检索范围
- [ ] 实践：对比不同检索策略的召回效果

### 周五（4h）· 检索 + 生成流程

- [ ] 学习：将检索到的文档片段注入 Prompt（Context Window 管理）
- [ ] 学习：来源引用——返回检索片段作为来源引证
- [ ] 实践：搭建一个端到端的 RAG 问答流水线

## 知识点清单

- [ ] RAG 完整工作流程
- [ ] Embedding 模型选择（OpenAI / HuggingFace / 本地）
- [ ] 文档切分策略（固定大小 / 递归字符 / 语义 / 代码感知 / 滑动窗口）
- [ ] `chunk_size` / `chunk_overlap` 参数
- [ ] Chroma 向量数据库基本操作
- [ ] 相似度检索（Cosine / Euclidean / Dot Product）
- [ ] MMR 检索策略
- [ ] Prompt 注入检索上下文
- [ ] 来源引用返回

## 练习 / 作业

```python
# 作业 1：Chunking 实验
# 对同一篇技术文档用 4 种策略切分，对比检索效果
# 固定大小 | 递归字符 | 语义切分 | 滑动窗口

# 作业 2：RAG 问答流水线
# 搭建最小 RAG 系统：
# - 加载一篇 FastAPI 官方文档
# - 切分 → Embedding → Chroma 存储
# - 用户提问 → 检索 Top 3 → 注入 Prompt → LLM 回答
# - 返回答案 + 来源引用
```

## 本周产出

- ✅ Chunking 策略对比实验报告
- ✅ 端到端 RAG 问答流水线（最小可用版）
- ✅ 文档处理工具函数库

## 通关标志

- [ ] 能画出 RAG 完整流程图并解释每个环节
- [ ] 能根据文档类型选择合适的 Chunking 策略
- [ ] 能使用 Chroma 进行向量存储和检索
- [ ] 能实现「检索→注入 Prompt→LLM 回答」的完整链路

## 资源链接

| 资源 | 链接 |
|------|------|
| LangChain Text Splitters | https://python.langchain.com/docs/how_to/#text-splitters |
| Chroma 文档 | https://docs.trychroma.com/ |
| LlamaIndex: Building RAG from Scratch | https://www.youtube.com/@LlamaIndex |
| OpenAI Embeddings 指南 | https://platform.openai.com/docs/guides/embeddings |

## 前端技能衔接提示

- Chunking = 长列表分页/虚拟滚动——控制每次处理的数据块大小
- 向量检索 = 前端搜索过滤——用相似度代替关键词匹配
- RAG Pipeline = 数据管道（ETL）——Extract → Transform → Load
- Metadata 过滤 = CSS 选择器——按属性缩小范围
