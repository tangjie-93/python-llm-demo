# AI Agent 开发者情报站设计

## 目标

构建一个别人可以直接访问的 AI Agent 开发者/学习者情报站。它每天自动采集 AI 相关内容，生成中文摘要、分类和标签，并把外部内容与本地 Obsidian/Markdown 笔记关联起来，形成可浏览、可搜索、可持续更新的公开网站。

第一版重点不是做一个聊天框，而是跑通“采集 -> 清洗 -> 摘要 -> 分类 -> 网站展示 -> 本地知识关联”的内容闭环。

## 目标读者

主要面向两类人：

1. AI 开发者：关注 LLM API、Agent、RAG、MCP、开源项目、工程实践和部署经验。
2. AI 学习者：需要结构化学习路线、术语解释、每日精选和高质量教程入口。

内容风格应偏技术和学习，不做泛泛的 AI 新闻搬运。

## MVP 范围

第一版包含以下能力：

1. 公开首页
   - 今日 AI 简报
   - 最新内容列表
   - 热门分类入口
   - 推荐专题入口

2. 分类页
   - Agent
   - RAG
   - LLM API
   - 开源项目
   - 论文与研究
   - AI 工具
   - 教程与学习资源
   - 行业动态

3. 内容详情页
   - 标题
   - 原文链接
   - 来源
   - 发布时间
   - 中文摘要
   - 分类与标签
   - 关键要点
   - 相关本地笔记

4. 每日简报
   - 每天定时生成一篇中文简报
   - 按分类汇总重点内容
   - 标出“值得深入阅读”的内容
   - 保留历史简报列表

5. 本地知识整理
   - 扫描本地 Obsidian/Markdown 文件
   - 抽取标题、路径、正文、标签和更新时间
   - 自动分类到同一套主题体系
   - 将本地笔记关联到外部内容和专题页

6. 搜索与 RAG
   - 支持关键词搜索公开内容和本地笔记
   - 支持基于站内内容的问答
   - 回答必须引用来源
   - 检索不到可靠依据时拒答

## 非目标

第一版不做：

- 用户注册、登录和评论
- 订阅付费
- 复杂个性化推荐
- 多作者 CMS 工作流
- 自动发布未经审核的高风险内容
- 面向全行业的泛 AI 新闻站

这些能力会增加复杂度，但不影响第一版验证核心价值。

## 推荐技术架构

```text
外部内容源
  -> 采集任务
  -> 内容清洗与去重
  -> LLM 摘要/分类/标签
  -> 数据库
  -> 向量索引
  -> FastAPI
  -> Vue/Nuxt 公开网站

本地 Obsidian/Markdown
  -> 本地扫描任务
  -> 元数据抽取
  -> LLM 分类/标签
  -> 数据库
  -> 向量索引
  -> 相关笔记/RAG/专题页
```

建议技术选型：

- 前台网站：Vue 3 或 Nuxt 3。若重视 SEO 和公开访问，优先 Nuxt 3。
- 后端 API：FastAPI。
- 数据库：PostgreSQL。个人原型也可先用 SQLite，但公开网站建议尽早切 PostgreSQL。
- 向量检索：PostgreSQL + pgvector 或 Qdrant。第一版推荐 PostgreSQL + pgvector，减少系统数量。
- 定时任务：APScheduler、Celery Beat 或 GitHub Actions。早期可用 APScheduler，部署稳定后再拆到队列。
- LLM：用于摘要、分类、标签、每日简报和 RAG 回答。
- 部署：前端部署到 Vercel/Netlify，后端部署到 Render/Fly.io/云服务器，数据库使用托管 PostgreSQL。

## 核心模块

### 内容采集模块

负责从配置化内容源获取最新 AI 内容。第一版优先支持 RSS 和静态源列表，避免一开始写复杂爬虫。

每条内容至少保存：

- 标题
- URL
- 来源名称
- 发布时间
- 原文摘要或正文片段
- 抓取时间
- 内容哈希

用 URL 和内容哈希做去重。

### 内容理解模块

负责调用 LLM 生成结构化结果：

```json
{
  "summary": "中文摘要",
  "key_points": ["要点 1", "要点 2"],
  "category": "Agent",
  "tags": ["LangGraph", "Tool Calling"],
  "audience": "developer",
  "importance": 4,
  "reason": "为什么值得读"
}
```

分类必须限制在固定枚举中，避免标签无限膨胀。标签可以更灵活，但需要定期合并同义词。

### 本地知识扫描模块

负责读取 Obsidian/Markdown 文件。它不是公开暴露原始本地文件，而是抽取可公开的元数据、摘要和关联关系。

每篇本地笔记至少保存：

- 标题
- 文件路径
- 更新时间
- Markdown frontmatter
- 正文摘要
- 分类
- 标签
- 向量索引状态

如果某些笔记不适合公开，可用目录白名单或 frontmatter 控制：

```yaml
publish: true
category: RAG
tags:
  - embedding
  - retrieval
```

### 网站展示模块

公开网站优先解决浏览效率：

- 首页让读者快速看到今天有什么值得关注。
- 分类页让读者按主题追踪内容。
- 详情页让读者判断是否打开原文。
- 专题页把外部内容和本地笔记串成学习路径。

页面不应以 Chat UI 为核心。Chat/RAG 是辅助检索能力。

### RAG 问答模块

RAG 只回答站内已有内容和允许公开的本地笔记。回答必须包含引用来源。

检索策略：

1. 关键词检索召回标题、标签、来源和正文。
2. 向量检索召回语义相关内容。
3. 合并结果并 rerank。
4. 低分或无依据时拒答。

## 数据模型草案

### content_items

- id
- title
- url
- source_id
- source_type
- published_at
- fetched_at
- raw_excerpt
- summary
- key_points
- category
- tags
- importance
- content_hash
- status

### local_notes

- id
- title
- file_path
- updated_at
- frontmatter
- summary
- category
- tags
- publish_status
- content_hash
- index_status

### daily_briefs

- id
- brief_date
- title
- summary
- sections
- generated_at
- status

### embeddings

- id
- object_type
- object_id
- chunk_text
- metadata
- embedding
- created_at

## 内容分类体系

第一版使用固定一级分类：

- Agent
- RAG
- LLM API
- MCP / Tools
- Open Source
- Papers
- Products
- Tutorials
- Deployment / Eval / Security

标签用于更细粒度主题，例如：

- LangGraph
- LlamaIndex
- OpenAI API
- Claude
- Gemini
- Qdrant
- pgvector
- Prompt Injection
- Evals

分类用于网站导航，标签用于关联内容。

## 每日任务流程

每天定时执行：

1. 拉取外部内容源。
2. 去重并保存原始记录。
3. 调用 LLM 生成摘要、分类、标签和重要性评分。
4. 扫描本地 Markdown 变更。
5. 更新本地笔记分类和向量索引。
6. 生成每日简报。
7. 将简报发布到网站。
8. 输出运行日志和失败记录。

## 错误处理

- 内容源不可用：记录失败，不阻塞其他来源。
- LLM 调用失败：保留待处理状态，下一轮重试。
- 分类结果不合法：回退到 `Uncategorized` 并记录错误。
- 本地文件解析失败：跳过该文件并保留错误原因。
- RAG 检索低置信度：拒答并展示可搜索的相关内容。

## 安全与发布边界

本地笔记默认不公开。只有满足以下条件之一才进入公开页面：

1. 位于配置的公开目录白名单。
2. frontmatter 中显式声明 `publish: true`。

RAG 可以检索非公开笔记用于个人后台，但公开网站不能向访客返回非公开笔记内容。第一版如果不做登录，建议公开站只索引可公开内容。

## 验收标准

第一版完成时应满足：

1. 访问网站首页能看到每日 AI 简报。
2. 至少有 5 个分类页可以浏览内容。
3. 每条内容详情页包含中文摘要、原文链接、分类和标签。
4. 定时任务可以生成当天简报。
5. 本地 Markdown 可以被扫描、分类并关联到内容详情或专题页。
6. 搜索可以同时查到外部内容和可公开本地笔记。
7. RAG 回答带来源引用，并能在无依据时拒答。

## 建议实施顺序

1. 建数据库模型和内容源配置。
2. 实现 RSS/链接采集和去重。
3. 实现 LLM 摘要、分类和标签。
4. 实现每日简报生成。
5. 实现公开网站首页、分类页和详情页。
6. 接入本地 Markdown 扫描。
7. 加搜索与基础 RAG。
8. 部署公开访问版本。

## 开放决策

需要在实施前确认：

1. 是否使用 Nuxt 3 来换取更好的 SEO。
2. 第一批内容源清单。
3. 本地 Obsidian/Markdown 的公开目录白名单。
4. 每日简报的发布时间和推送渠道。
