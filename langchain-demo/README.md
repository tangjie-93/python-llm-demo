# LangChain 完整教程

这是一个循序渐进的 LangChain 教程，包含了 LangChain 的所有核心知识点，并使用 Gradio 构建了交互式前端界面。

## 功能特性

- **基础概念**：了解 LangChain 的核心组件
- **链 (Chains)**：学习不同类型的链及其应用
- **记忆 (Memory)**：实现对话历史和记忆功能
- **文档处理**：文档加载、分割、嵌入和检索
- **工具和代理**：使用外部工具和构建智能代理
- **评估**：评估模型性能

## 环境要求

- Python 3.8+
- pip 20.0+

## 安装依赖

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows
. venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

## 环境变量配置

创建 `.env` 文件，添加以下内容：

```
# DeepSeek API Key
DEEPSEEK_API_KEY=your_deepseek_api_key

# OpenAI API Key (可选)
OPENAI_API_KEY=your_openai_api_key
```

## 运行应用

```bash
python langchain_demo.py
```

应用将在 `http://localhost:7860` 启动。

## 教程内容

### 1. 基础概念
- **Models**：语言模型接口
- **Prompts**：提示模板
- **Output Parsers**：输出解析器

### 2. 链 (Chains)
- **LLMChain**：基础链
- **SequentialChain**：顺序链
- **RouterChain**：路由链

### 3. 记忆 (Memory)
- **ConversationBufferMemory**：对话缓冲区
- **ConversationSummaryMemory**：对话摘要

### 4. 文档处理
- **Document Loaders**：文档加载器
- **Text Splitters**：文本分割器
- **Embeddings**：嵌入
- **Vector Stores**：向量存储
- **Retrievers**：检索器

### 5. 工具和代理
- **Tools**：工具
- **Agents**：代理
- **Toolkits**：工具包

### 6. 评估
- 问答评估
- 摘要评估
- 文本生成评估

### 7. 回调
- 跟踪和监控

## 学习路径

1. 从基础概念开始
2. 学习构建简单的链
3. 添加记忆功能
4. 处理文档和向量存储
5. 使用工具和代理
6. 评估模型性能
7. 部署和监控

## 注意事项

- 本教程使用了 `deepseek-chat` 模型作为默认模型
- 部分功能需要 API Key 才能正常工作
- 文档处理示例使用了模拟数据，实际应用中需要加载真实文档

## 扩展建议

- 添加更多文档加载器支持
- 集成更多向量存储
- 实现更复杂的代理逻辑
- 添加实时监控和日志

## 相关资源

- [LangChain 官方文档](https://python.langchain.com/docs/get_started/introduction)
- [Gradio 官方文档](https://www.gradio.app/docs/)
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
