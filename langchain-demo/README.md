# `LangChain` 完整教程

这是一个循序渐进的 `LangChain` 教程，包含了 `LangChain` 的所有核心知识点，并使用 `Gradio` 构建了交互式前端界面。

## 一、`LangChain` 简介

`LangChain` 是一个强大的框架，用于构建基于大语言模型（`LLM`）的自定义代理和应用程序。它提供了一套工具、组件和接口，使开发者能够更轻松地构建复杂的 `LLM` 应用。

### 1.1 核心价值

- **简化开发流程**：通过提供预构建的组件和接口，减少了开发时间和复杂度
- **模型集成**：支持多种 `LLM` 模型，包括 `OpenAI`、`Anthropic`、`Google`、`DeepSeek` 等
- **代理架构**：提供预构建的代理架构，支持复杂的任务处理
- **灵活扩展**：易于集成自定义工具和功能

### 1.2 架构设计

`LangChain` 的核心架构围绕着链（`Chains`）和代理（`Agents`）展开。链是将多个组件连接在一起的方式，而代理则是使用 `LLM` 来决定如何使用工具完成任务。

## 二、环境要求

1. Python 3.8+
2. pip 20.0+

## 三、安装依赖

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

## 四、环境变量配置

创建 `.env` 文件，添加以下内容：

```
# DeepSeek API Key
DEEPSEEK_API_KEY=your_deepseek_api_key

# OpenAI API Key (可选)
OPENAI_API_KEY=your_openai_api_key
```

## 五、运行应用

```bash
python app.py
```

应用将在 `http://localhost:7860` 启动。

## 六、核心组件

`LangChain` 采用模块化设计，包含以下核心组件：

### 6.1 模型（`Models`）

#### 6.1.1 语言模型（Language Models`）
- 支持多种 `LLM` 提供商的模型
- 包括聊天模型（`ChatModels`）和纯文本模型（`LLMs`）
- 支持 `OpenAI`、`Anthropic`、`Google`、`DeepSeek` 等

#### 6.1.2 嵌入模型（Embeddings`）
- 用于将文本转换为向量表示
- 支持各种嵌入模型，如 `OpenAIEmbeddings`、`DeepSeekEmbeddings` 等

#### 6.1.3 聊天模型（Chat Models`）
- 专门用于对话式应用的模型接口
- 接受消息列表作为输入，返回消息作为输出

### 6.2 提示（`Prompts`）

#### 6.2.1 提示模板（Prompt Templates`）
- 可重用的提示结构
- 支持动态参数填充
- `ChatPromptTemplate`：聊天提示模板
- `PromptTemplate`：纯文本提示模板
- `FewShotPromptTemplate`：少样本提示模板，包含示例引导
- `FewShotChatMessagePromptTemplate`：少样本聊天消息提示模板
- `SystemMessagePromptTemplate`：系统消息提示模板
- `HumanMessagePromptTemplate`：人类消息提示模板
- `AIMessagePromptTemplate`：AI消息提示模板
- `ChatMessagePromptTemplate`：聊天消息提示模板
- `StringPromptTemplate`：字符串提示模板

#### 6.2.2 提示组合（Prompt Composition`）
- 将多个提示组合成更复杂的结构
- `RunnableParallel`：并行组合
- `RunnableSequence`：序列组合
- `MessagesPlaceholder`：消息占位符，用于插入动态消息列表（如对话历史）
- `LangChain Expression Language (LCEL)`：使用 `|` 运算符组合提示和其他组件

#### 6.2.3 示例选择器（Example Selectors`）
- 根据输入动态选择相关示例
- 支持各种选择策略：基于长度、相似度等

### 6.3 输出解析器（`Output Parsers`）

#### 6.3.1 常用解析器
- **`StrOutputParser`**：将输出解析为字符串
- **`JsonOutputParser`**：将输出解析为 JSON
- **`PydanticOutputParser`**：将输出解析为 Pydantic 模型
- **`CommaSeparatedListOutputParser`**：将输出解析为逗号分隔的列表

#### 6.3.2 自定义解析器
- 可以创建自定义解析器来处理特定格式的输出

### 6.4 链（`Chains`）

#### 6.4.1 基础链
- **`LLMChain`**：基础链，连接提示模板和语言模型
- **`TransformationChain`**：转换链，对数据进行预处理和后处理

#### 6.4.2 通用链
- **`SequentialChain`**：顺序执行多个链
- **`RouterChain`**：根据输入路由到不同的链
- **`ConversationChain`**：对话链，带有记忆功能

#### 6.4.3 问答链
- **`RetrievalQAChain`**：结合文档检索和问答
- **`StuffDocumentsChain`**：将文档内容填充到提示中
- **`MapReduceDocumentsChain`**：MapReduce 方式的文档处理

#### 6.4.4 `LangChain` Expression Language (`LCEL`)
- 声明式的方式来组合链
- 使用 `|` 运算符连接组件
- 支持流式输出、并发执行、批处理等

### 6.5 记忆（`Memory`）

#### 6.5.1 短期记忆（Short-term Memory`）
- **概念**：短期记忆让应用程序记住单个线程或对话中的先前交互
- **对话历史**：最常见的短期记忆形式
- **上下文限制**：由于上下文窗口有限，需要使用技术来删除过时信息
- **消息修整**：通过计算标记数量来截断消息

#### 6.5.2 长期记忆（Long-term Memory`）
- **概念**：长期记忆允许代理跨线程记住信息
- **向量存储**：使用向量存储来检索相关的历史信息
- **持久化**：通过检查点（Checkpoint）实现跨会话的持久化

#### 6.5.3 常用记忆组件
1. **`InMemorySaver`**：内存检查点，用于短期记忆
2. **`PostgresSaver`**：数据库检查点，用于生产环境
3. **`Trim Messages`**：消息修整工具
4. **`ConversationBufferMemory`**：对话缓冲区
5. **`ConversationSummaryMemory`**：对话摘要
6. **`ConversationBufferWindowMemory`**：窗口对话记忆
7. **`VectorStoreMemory`**：向量存储记忆

### 6.6 索引（`Indexing`）

#### 6.6.1 文档加载器（Document Loaders`）
- 支持多种文档格式：`PDF`、`Word`、`Markdown`、`HTML`、`JSON`、`CSV` 等
- 从各种来源加载文档：本地文件、URL、数据库等

#### 6.6.2 文本分割器（Text Splitters`）
- 将长文本分割成可管理的 `chunks`
- 常用方法：`RecursiveCharacterTextSplitter`、`CharacterTextSplitter`
- 支持自定义分割规则和元数据保留

#### 6.6.3 嵌入（Embeddings`）
- 将文本转换为向量表示
- 支持各种嵌入模型

#### 6.6.4 向量存储（Vector Stores`）
- 存储和检索向量嵌入
- 支持多种后端：`Chroma`、`FAISS`、`Pinecone`、`Weaviate`、`Milvus` 等

#### 6.6.5 检索器（Retrievers`）
- 从向量存储中检索相关文档
- 常用类型：相似度检索、最大边际相关性（MMR）、自查询检索器等

### 6.7 工具和代理（`Tools` and `Agents`）

#### 6.7.1 工具（Tools`）
- 可被代理调用的函数
- 常用工具：搜索、计算、数据库查询、API 调用等
- 支持自定义工具创建

#### 6.7.2 代理（Agents`）
- 使用 `LLM` 来决定如何使用工具完成任务
- 支持多种代理类型：`ReAct`、`Self-Ask`、`Plan-and-Execute` 等

#### 6.7.3 工具包（Toolkits`）
- 相关工具的集合
- 提供常用工具的便捷访问

### 6.8 评估（`Evaluation`）

#### 6.8.1 评估类型
- **问答评估**：评估模型回答问题的质量
- **摘要评估**：评估模型生成摘要的质量
- **文本生成评估**：评估模型生成文本的质量

#### 6.8.2 评估方法
- 基于规则的评估
- 基于 `LLM` 的评估
- 人工评估

### 6.9 回调（`Callbacks`）

#### 6.9.1 回调功能
- 跟踪和监控链的执行
- 记录日志、收集指标、处理错误
- 支持异步回调

#### 6.9.2 常用回调处理器
- **`StdOutCallbackHandler`**：标准输出
- **`LangChainTracer`**：LangChain 追踪
- 自定义回调处理器

### 6.10 `LangGraph` 集成

`LangChain` 代理基于 `LangGraph` 构建，提供以下功能：

1. **持久执行**：即使在系统重启后也能继续执行
2. **流式传输**：实时返回部分结果
3. **人在环中**：支持人类干预和反馈
4. **持久化**：保存状态和历史记录

## 七、应用场景

1. **对话式应用**：聊天机器人、客户支持、个人助手
2. **文档处理**：文档问答，信息提取、摘要生成
3. **数据分析**：数据分析、报告生成、可视化辅助
4. **自动化工作流**：任务自动化、决策支持、流程优化
5. **教育和培训**：个性化学习、辅导系统、评估工具

## 八、学习路径

1. 从基础概念开始（模型、提示、输出解析器）
2. 学习构建简单的链（`LLMChain`、`SequentialChain`）
3. 添加记忆功能（短期记忆、长期记忆）
4. 处理文档和向量存储（索引、检索）
5. 使用工具和代理（工具定义、代理决策）
6. 评估模型性能（问答评估、摘要评估）
7. 部署和监控（回调、日志）

## 九、注意事项

1. 本教程使用了 `deepseek-chat` 模型作为默认模型
2. 部分功能需要 `API Key` 才能正常工作
3. 文档处理示例使用了模拟数据，实际应用中需要加载真实文档

## 十、扩展建议

1. 添加更多文档加载器支持
2. 集成更多向量存储
3. 实现更复杂的代理逻辑
4. 添加实时监控和日志
5. 探索 `LangGraph` 的高级功能

## 十一、相关资源

1. [LangChain 官方文档](https://docs.langchain.com/oss/python/langchain/overview)
2. [LangChain GitHub 仓库](https://github.com/langchain-ai/langchain)
3. [LangGraph 官方文档](https://docs.langchain.com/oss/python/langgraph/overview)
4. [Gradio 官方文档](https://www.gradio.app/docs/)
5. [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
6. [DeepSeek API 文档](https://platform.deepseek.com/docs)
