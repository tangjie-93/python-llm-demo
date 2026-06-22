# 02. RAG 知识库 Agent

## 学习目标

RAG 的目标是让模型基于外部资料回答问题，而不是完全依赖模型参数里的知识。

RAG 全称是 Retrieval-Augmented Generation，即“检索增强生成”。

## 1. RAG 基本流程

一个典型 RAG 流程：

1. 收集文档
2. 解析文档
3. 切分 chunk
4. 生成 embedding
5. 存入向量数据库
6. 用户提问
7. 检索相关 chunk
8. 可选 rerank
9. 把相关内容放入上下文
10. 模型生成答案并引用来源

## 2. 文档解析

文档解析是把 PDF、Markdown、HTML、Word 等内容转成可索引文本。

重点问题：

- 表格如何处理
- 标题层级如何保留
- 图片和 OCR 如何处理
- 代码块如何保留
- 页码和来源如何记录

建议记录 metadata：

```json
{
  "doc_id": "string",
  "title": "string",
  "source": "string",
  "page": 3,
  "section": "安装说明",
  "created_at": "2026-06-16",
  "permission_group": "engineering"
}
```

练习：

- 解析 Markdown 并保留标题层级
- 解析 PDF 并保留页码
- 把每个 chunk 和来源 metadata 绑定

## 3. Chunking

Chunking 是把长文档切成小片段。

常见策略：

- 固定长度切分
- 按标题切分
- 按段落切分
- 语义切分
- 滑动窗口 overlap

经验原则：

- chunk 太小：缺少上下文
- chunk 太大：召回不精准，浪费 token
- overlap 太小：跨段信息丢失
- overlap 太大：重复内容太多

练习：

- 对同一文档分别使用 300、800、1500 字 chunk
- 比较检索结果质量
- 记录不同 chunk 策略的 eval 分数

## 4. Embedding

Embedding 是把文本转换成向量，用于语义相似度搜索。

关键理解：

- embedding 适合找语义相近内容
- 不一定擅长精确匹配编号、代码、公式
- embedding 模型变化后通常需要重新索引
- 查询文本和文档文本最好使用同一 embedding 模型

练习：

- 对 20 个问题做向量检索
- 观察 top 5 是否包含正确答案
- 记录失败问题类型

## 5. Vector Search

Vector search 根据向量相似度查找相关文本。

常见数据库：

- PostgreSQL + pgvector
- Qdrant
- Milvus
- Weaviate
- Pinecone

对于个人项目，建议优先用 PostgreSQL + pgvector，便于同时管理结构化数据和向量。

## 6. BM25 与 Hybrid Search

BM25 是传统关键词检索方法，适合：

- 精确术语
- 产品编号
- API 名称
- 错误码
- 专有名词

Hybrid Search 是结合向量检索和关键词检索，通常比单一向量检索更稳。

练习：

- 用同一批问题比较 vector search、BM25、hybrid search
- 找出哪类问题更适合关键词检索

## 7. Rerank

Rerank 是对初步召回结果重新排序。典型做法：

1. 先召回 top 20
2. 用 reranker 重新评分
3. 取 top 5 放入模型上下文

适用场景：

- 文档量变大
- 召回结果噪声高
- top 结果不稳定

## 8. Citation

Citation 是让答案带来源引用。

好的引用应该包含：

- 文档标题
- 页码或章节
- 原文片段
- 链接
- chunk id

Vue 交互建议：

- 答案正文中显示引用编号
- 右侧引用侧边栏展示来源
- 点击引用滚动到对应片段
- 支持打开原文

## 9. 拒答机制

RAG Agent 必须能承认“不知道”。

拒答条件：

- 检索结果为空
- 检索分数过低
- 资料与问题不相关
- 资料中没有明确答案
- 用户要求超出权限范围

拒答不应该是简单一句“我不知道”，而应该说明：

- 当前资料没有找到依据
- 已搜索了哪些范围
- 用户可以补充什么资料

## 10. Vue 知识库 Agent 项目

功能清单：

- 文档上传
- 文档解析进度
- 索引状态展示
- Chat UI
- 流式回答
- 引用侧边栏
- 历史会话
- 文档过滤器
- 失败反馈按钮

推荐架构：

```text
Vue 3 / Nuxt 3
  -> FastAPI
    -> PostgreSQL + pgvector
    -> Redis
    -> Object Storage
    -> LLM API
```

## 11. 本阶段学习资源

- LlamaIndex 文档：https://docs.llamaindex.ai/
- LangChain RAG 文档：https://docs.langchain.com/
- pgvector：https://github.com/pgvector/pgvector
- PostgreSQL：https://www.postgresql.org/docs/
- Qdrant 文档：https://qdrant.tech/documentation/
- Vue 3 官方文档：https://vuejs.org/
- Nuxt 3 文档：https://nuxt.com/docs

