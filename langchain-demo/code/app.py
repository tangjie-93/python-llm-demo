"""
`LangChain` 完整教程主文件
整合所有示例，使用 `Gradio` 作为前端界面
"""
import gradio as gr
import markdown
# 从 demos 包导入各个模块
from demos.a01_basic_concepts import run_demo as basic_concepts_run
from demos.a02_chains import run_sequential_chain, run_router_chain
from demos.a03_memory import run_memory_demo
from demos.a04_document_processing import run_document_retrieval, get_all_documents
from demos.a05_tools_agents import run_agent
from demos.a06_evaluation import run_evaluation
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 文档目录
DOCS_DIRECTORY = os.path.join(current_dir, "docs")
# 向量存储路径
VECTOR_STORE_PATH = os.path.join(current_dir, "vector_store")

def create_gradio_interface():
    """创建 `Gradio` 界面"""
    # 预加载文档
    documents = get_all_documents(DOCS_DIRECTORY, VECTOR_STORE_PATH)
    initial_documents = "\n\n".join([f"{doc.page_content} (来源: {doc.metadata['source']})" for doc in documents])
    
    with gr.Blocks(title="LangChain 完整教程") as demo:
        gr.Markdown("# LangChain 循序渐进教程")
        
        # 模型选择
        model_choice = gr.Radio(
            choices=["deepseek", "openai"],
            value="deepseek",
            label="选择模型"
        )
        
        # 1. 基础概念
        with gr.Tab("1. 基础概念"):
            gr.Markdown("## 基础概念示例")
            topic = gr.Textbox(label="输入主题", value="LangChain")
            basic_output = gr.HTML(label="解释")
            basic_button = gr.Button("生成解释")
            
            def basic_concepts_handler(topic, model):
                result = basic_concepts_run(topic, model)
                # 将 `Markdown` 转换为 `HTML`
                html = f"<div class='output-container'>{markdown.markdown(result)}</div>"
                return html
            
            basic_button.click(basic_concepts_handler, inputs=[topic, model_choice], outputs=basic_output)
        
        # 2. 链示例
        with gr.Tab("2. 链示例"):
            gr.Markdown("## 链示例")
            
            # 顺序链
            gr.Markdown("### 顺序链 (`SequentialChain`)")
            text = gr.Textbox(label="输入文本", value="LangChain 是一个强大的框架，用于构建基于大语言模型的应用。")
            english_output = gr.HTML(label="英文翻译")
            summary_output = gr.HTML(label="总结")
            chain_button = gr.Button("执行顺序链")
            
            def chains_handler(text, model):
                result = run_sequential_chain(text, model)
                # 将 `Markdown` 转换为 `HTML`
                english_html = f"<div class='output-container'>{markdown.markdown(result['english_text'])}</div>"
                summary_html = f"<div class='output-container'>{markdown.markdown(result['summary'])}</div>"
                return english_html, summary_html
            
            chain_button.click(chains_handler, inputs=[text, model_choice], outputs=[english_output, summary_output])
            
            # 路由链
            gr.Markdown("### 路由链 (`RouterChain`)")
            router_input = gr.Textbox(label="输入请求", value="请总结以下内容：LangChain 是一个用于构建 LLM 应用的框架")
            router_output = gr.HTML(label="路由链结果")
            router_button = gr.Button("执行路由链")
            
            def router_handler(input_text, model):
                result = run_router_chain(input_text, model)
                # 将 `Markdown` 转换为 `HTML`
                html = f"<div class='output-container'>{markdown.markdown(result['result'])}</div>"
                return html
            
            router_button.click(router_handler, inputs=[router_input, model_choice], outputs=router_output)
        
        # 3. 记忆示例
        with gr.Tab("3. 记忆示例"):
            gr.Markdown("## 记忆示例")
            chat_input = gr.Textbox(label="输入消息")
            chat_output = gr.HTML(label="回复")
            chat_history = gr.Textbox(label="对话历史", lines=5)
            chat_button = gr.Button("发送")
            
            # 存储记忆实例
            memory_instances = {}
            
            def memory_handler(input_text, model):
                nonlocal memory_instances
                response, history, memory_instances = run_memory_demo(input_text, model, memory_instances)
                # 将 `Markdown` 转换为 `HTML`
                html = f"<div class='output-container'>{markdown.markdown(response)}</div>"
                return html, history
            
            chat_button.click(memory_handler, inputs=[chat_input, model_choice], outputs=[chat_output, chat_history])
        
        # 4. 文档处理
        with gr.Tab("4. 文档处理"):
            gr.Markdown("## 文档处理示例")
            
            # 显示原始文档
            gr.Markdown("### 原始文档")
            docs_display = gr.Textbox(label="原始文档", lines=6, interactive=False, value=initial_documents)
            
            # 检索功能
            gr.Markdown("### 文档检索")
            query = gr.Textbox(label="输入查询", value="LangChain的核心概念")
            docs_output = gr.HTML(label="检索结果")
            doc_button = gr.Button("检索")
            
            def document_handler(query):
                docs = run_document_retrieval(query, DOCS_DIRECTORY, VECTOR_STORE_PATH, return_only_relevant=True)
                # 格式化结果，添加更好的样式
                formatted_results = []
                for i, doc in enumerate(docs, 1):
                    formatted_result = f"### 文档 {i} (来源: {doc.metadata['source']})\n{doc.page_content}"
                    formatted_results.append(formatted_result)
                
                result = "\n\n---\n\n".join(formatted_results)
                # 将 `Markdown` 转换为 `HTML`
                html = f"<div class='output-container'>{markdown.markdown(result)}</div>"
                return html
            
            doc_button.click(document_handler, inputs=query, outputs=docs_output)
        
        # 5. 工具和代理
        with gr.Tab("5. 工具和代理"):
            gr.Markdown("## 工具和代理示例")
            agent_input = gr.Textbox(label="输入问题", value="今天北京的天气如何？")
            agent_output = gr.HTML(label="代理回复")
            agent_button = gr.Button("执行代理")
            
            def agent_handler(input_text, model):
                result = run_agent(input_text, model)
                # 将 `Markdown` 转换为 `HTML`
                html = f"<div class='output-container'>{markdown.markdown(result)}</div>"
                return html
            
            agent_button.click(agent_handler, inputs=[agent_input, model_choice], outputs=agent_output)
        
        # 6. 评估
        with gr.Tab("6. 评估"):
            gr.Markdown("## 评估示例")
            question = gr.Textbox(label="问题", value="LangChain 是什么？")
            answer = gr.Textbox(label="模型回答", value="LangChain 是一个用于构建 LLM 应用的框架")
            reference = gr.Textbox(label="参考回答", value="LangChain 是一个框架，用于开发由语言模型驱动的应用程序。它提供了一套工具、组件和接口，使开发者能够更轻松地构建复杂的 LLM 应用。")
            eval_output = gr.HTML(label="评估结果")
            eval_button = gr.Button("评估")
            
            def eval_handler(question, answer, reference):
                result = run_evaluation(question, answer, reference)
                # 将结果转换为 `HTML`
                html = f"<div class='output-container'><p>{result}</p></div>"
                return html
            
            eval_button.click(eval_handler, inputs=[question, answer, reference], outputs=eval_output)
        
        # 7. 总结
        with gr.Tab("7. 总结"):
            gr.Markdown("""
            ## `LangChain` 核心知识点总结
            
            1. **基础概念**
               - `Models`: 语言模型接口，支持多种 `LLM` 提供商的模型，如 `OpenAI`、`Anthropic`、`Google`、`DeepSeek` 等
               - `Prompts`: 提示模板，可重用的提示结构
               - `Output Parsers`: 输出解析器，处理模型输出
            
            2. **链 (`Chains`)**
               - `LLMChain`: 基础链，连接提示和模型
               - `SequentialChain`: 顺序执行多个链
               - `RouterChain`: 根据输入路由到不同的链
               - `RetrievalQAChain`: 结合文档检索和问答
            
            3. **记忆 (`Memory`)**
               - `ConversationBufferMemory`: 简单的对话历史存储
               - `ConversationSummaryMemory`: 存储对话摘要，节省上下文空间
               - `ConversationBufferWindowMemory`: 只保留最近的对话
               - `VectorStoreMemory`: 使用向量存储来检索相关对话历史
            
            4. **文档处理**
               - `Document Loaders`: 支持多种文档格式（`PDF`、`Word`、`Markdown` 等）
               - `Text Splitters`: 将长文本分割成可管理的 `chunks`
               - `Embeddings`: 将文本转换为向量表示
               - `Vector Stores`: 存储和检索向量嵌入
               - `Retrievers`: 从向量存储中检索相关文档
            
            5. **工具和代理**
               - `Tools`: 可被代理调用的函数，如搜索、计算等
               - `Agents`: 使用 `LLM` 来决定如何使用工具完成任务
               - `Toolkits`: 相关工具的集合
            
            6. **评估**
               - 问答评估：评估模型回答问题的质量
               - 摘要评估：评估模型生成摘要的质量
               - 文本生成评估：评估模型生成文本的质量
            
            7. **`LangGraph` 集成**
               - 持久执行：即使在系统重启后也能继续执行
               - 流式传输：实时返回部分结果
               - 人在环中：支持人类干预和反馈
               - 持久化：保存状态和历史记录
            
            ## 学习路径
            1. 从基础概念开始
            2. 学习构建简单的链
            3. 添加记忆功能
            4. 处理文档和向量存储
            5. 使用工具和代理
            6. 评估模型性能
            7. 部署和监控
            
            ## 应用场景
            - **对话式应用**：聊天机器人、客户支持、个人助手
            - **文档处理**：文档问答、信息提取、摘要生成
            - **数据分析**：数据分析、报告生成、可视化辅助
            - **自动化工作流**：任务自动化、决策支持、流程优化
            - **教育和培训**：个性化学习、辅导系统、评估工具
            """)
    
    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    # 定义 `CSS` 样式
    custom_css = """
    .output-container {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin-top: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        min-height: 100px;
    }
    
    .output-container h1, .output-container h2, .output-container h3 {
        color: #333;
        margin-bottom: 10px;
    }
    
    .output-container p {
        color: #555;
        line-height: 1.6;
        margin-bottom: 10px;
    }
    
    .output-container ul, .output-container ol {
        margin-left: 20px;
        margin-bottom: 10px;
    }
    
    .output-container li {
        margin-bottom: 5px;
    }
    
    .output-container code {
        background-color: #f0f0f0;
        padding: 2px 4px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    
    .output-container pre {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 4px;
        overflow-x: auto;
        margin-bottom: 10px;
    }
    """
    demo.launch(share=False, css=custom_css)
