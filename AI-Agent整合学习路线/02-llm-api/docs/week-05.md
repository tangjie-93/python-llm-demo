# Level 2-1 | 第 5 周：LLM 核心概念 — Token 到 Transformer

> 🧠 **关卡名**：思维觉醒 · 理解大模型
> 📅 **时间**：第 5 周 | ⏱️ **学时**：~18h

## 本周学习目标

- [ ] 理解 Token、Embedding、Attention 的基本概念
- [ ] 能看懂 Transformer 架构的高层流程图
- [ ] 了解主流模型生态和各自定位

## 每日学习安排

### 周一（3h）· Token 与 Tokenizer

- [ ] 学习：Token 概念——文本被切分后的最小单元
- [ ] 学习：Tokenizer 的作用（文本→Token ID→文本）
- [ ] 实践：用 `tiktoken` 库对中英文文本进行 Token 计数
- [ ] 练习：对比 GPT-4 / Claude / DeepSeek 的 Tokenizer 差异
- [ ] 前端衔接：Token 类比 CSS 中的像素点——同样的文本，不同 Tokenizer 切出不同数量

### 周二（3h）· Embedding 与向量空间

- [ ] 学习：Embedding 概念——将文本映射为高维向量
- [ ] 学习：向量空间中的语义相似度（cosine similarity）
- [ ] 实践：用 OpenAI `text-embedding-3-small` 生成 Embedding
- [ ] 练习：计算两段文本的语义相似度
- [ ] 前端衔接：Embedding = 把文本变成颜色值（`#FF0000`），语义相近的文本颜色也相近

### 周三（4h）· Transformer 架构（不含数学）

- [ ] 学习：Transformer 的高层架构（Encoder-Decoder）
- [ ] 学习：Self-Attention 直觉理解——「关注输入中重要部分」
- [ ] 学习：为什么 Transformer 取代了 RNN/LSTM
- [ ] 推荐视频：3Blue1Brown「Neural Networks」系列
- [ ] 前端衔接：Transformer = React Virtual DOM—核心算法引擎；Attention = Web Vitals 中的 FCP—关注关键部分

### 周四（4h）· 模型生态与选型

- [ ] 学习：GPT-4o / GPT-4.1（OpenAI）— 综合最强
- [ ] 学习：Claude 3.5 Sonnet / Opus（Anthropic）— 长上下文、安全
- [ ] 学习：Gemini 2.5 Pro（Google）— 1M+ tokens 超长上下文
- [ ] 学习：DeepSeek-V3 / R1 — 开源、高性价比
- [ ] 学习：Qwen 2.5 / Qwen3（阿里）— 中文优化
- [ ] 学习：Llama 3 / 4（Meta）— 开源社区活跃
- [ ] 练习：制作一张模型选型决策树

### 周五（3h）· 综合复习 + 概念整理

- [ ] 综合：画出 LLM 工作流程图（文本→Tokenizer→Transformer→Sampler→输出）
- [ ] 理解：Context Window（上下文窗口）= 浏览器的 LocalStorage 5MB 限制
- [ ] 理解：Temperature（温度参数）= `Math.random()` 的种子控制
- [ ] 练习：用自己的话写一篇 LLM 概念总结（给前端同行看）

## 知识点清单

- [ ] Token 概念与 Tokenizer 作用
- [ ] tiktoken 库使用
- [ ] Embedding 概念与向量语义空间
- [ ] cosine similarity 语义相似度计算
- [ ] Transformer 高层架构（Encoder-Decoder）
- [ ] Self-Attention 直觉理解
- [ ] Context Window 概念
- [ ] Temperature 参数
- [ ] GPT-4o / Claude / Gemini / DeepSeek / Qwen / Llama 模型对比
- [ ] 模型选型决策树

## 练习 / 作业

```python
# 作业 1：Token 计数实验
# 用 tiktoken 对比同一段中英文文本的 Token 数量
# 理解「中文 Token 效率低」的原因

# 作业 2：Embedding 相似度实验
# 用 OpenAI embedding API 计算以下句对的相似度：
# ("Python 是一门编程语言", "JavaScript 也是一门编程语言")
# ("Python 是一门编程语言", "今天天气真好")
# 打印相似度分数并分析结果

# 作业 3：模型选型决策树
# 用 Markdown 或 Python 实现一个交互式模型选型问答
```

## 本周产出

- ✅ Token 计数实验报告
- ✅ Embedding 相似度实验代码
- ✅ 模型选型决策树文档
- ✅ 1 篇 LLM 核心概念总结笔记

## 通关标志

- [ ] 能用自己的话解释 Token、Embedding、Attention
- [ ] 能说出至少 4 个主流模型的核心特点和适用场景
- [ ] 能画出 LLM 工作流程简图
- [ ] 能解释 Temperature 参数对输出的影响

## 资源链接

| 资源 | 链接 |
|------|------|
| Andrej Karpathy: Intro to LLMs (1h) | https://www.youtube.com/watch?v=zjkBMFhNj_g |
| 3Blue1Brown: Neural Networks | https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi |
| 《Attention Is All You Need》 | https://arxiv.org/abs/1706.03762 |
| tiktoken 仓库 | https://github.com/openai/tiktoken |
| OpenAI Platform | https://platform.openai.com/docs |

## 前端技能衔接提示

- Token 分片 ≈ 字符串 encode/decode
- Embedding 降维可视化 ≈ 前端数据可视化（`echarts`/`d3`）
- Attention 权重分配 ≈ CSS 优先级计算——模型自动决定「看重」哪些输入
- Context Window 限制 ≈ LocalStorage 5MB / Cookie 4KB 限制
