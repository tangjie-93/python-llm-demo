# 阶段三：Prompt Engineering & RAG

> 🎯 **阶段总目标**：掌握 Prompt 工程和 RAG 系统构建
> 📦 **阶段产出**：`doc-qa` — 技术文档 RAG 问答系统
> ⏱️ **阶段时长**：4 周 | **关卡数**：4

---

## 前置要求

- 完成阶段二（LLM API 调用）
- 完成阶段一（Python + FastAPI）

## 学习目标

- 掌握高级 Prompt Engineering 技巧
- 理解 RAG 的完整工作流程
- 能搭建基于向量数据库的 RAG 系统
- 能使用 LangChain/LlamaIndex 加速开发

## 关卡列表

| 关卡 | 周次 | 关卡名 | BOSS | EXP |
|------|------|--------|------|-----|
| [Level 3-1](./week-08.md) | 第 8 周 | 💬 低语智者 · Prompt 工程 | 🎭 人格面具 PersonaMask | ⭐⭐⭐ |
| [Level 3-2](./week-09.md) | 第 9 周 | 📚 知识编织者 · RAG 入门 | 🧩 碎片魔像 ChunkGolem | ⭐⭐⭐ |
| [Level 3-3](./week-10.md) | 第 10 周 | 🔗 框架驾驭者 · LangChain & LlamaIndex | ⚙️ 抽象魔偶 AbstractionGolem | ⭐⭐⭐ |
| [Level 3-4](./week-11.md) | 第 11 周 | 🏗️ 文档智者 · RAG 系统交付 | 👻 幻觉幻影领主 HallucinationLord | ⭐⭐⭐⭐ |

### 区域 BOSS

**👻 幻觉幻影领主 HallucinationLord** — 制造虚假信息的幻影领主。用「不知道」护盾方可对抗。

## 阶段验收标准

- [ ] 能根据任务类型选择合适的 Prompt 策略
- [ ] 理解 Embedding 的作用和向量相似度检索原理
- [ ] 能根据文档类型选择 Chunking 策略
- [ ] 能用 LangChain 或 LlamaIndex 搭建完整 RAG 系统
- [ ] 了解至少 3 种向量数据库的特点和适用场景
- [ ] 完成实战项目 `doc-qa` 全部验收标准

## 核心知识点一览

1. **Prompt Engineering**：Zero-shot、Few-shot、CoT、ToT、ReAct、Self-Consistency、Structured Output
2. **RAG 完整流程**：文档加载 → 切分 → Embedding → 向量存储 → 检索 → LLM 生成
3. **文档切分策略**：固定大小、递归字符、语义切分、代码感知、滑动窗口
4. **向量数据库**：Chroma、Qdrant、Milvus、Pinecone、FAISS、Weaviate、pgvector
5. **RAG 框架**：LangChain RAG、LlamaIndex

## 前端技能迁移要点

- Prompt 模板 = 前端组件模板
- RAG = 前端应用的「数据层」——API 拿不到的数据从本地向量库查
- Chunking = 长列表分页/虚拟滚动
- 向量检索 = 前端搜索过滤——用相似度代替关键词匹配

## 实战项目

**`doc-qa`** — 基于 RAG 的技术文档智能问答系统

- 支持上传 Markdown/PDF 技术文档
- 文档自动切分、向量化、存储
- 回答附带来源引用
- 支持多轮对话和流式返回
