"""
LangChain 完整教程主文件
整合所有示例，使用 Gradio 作为前端界面
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

def create_gradio_interface():
    """创建 Gradio 界面"""
    # 预加载文档
    documents = get_all_documents()
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
                # 将 Markdown 转换为 HTML
                html = f"<div class='output-container'>{markdown.markdown(result)}</div>"
                return html
            
            basic_button.click(basic_concepts_handler, inputs=[topic, model_choice], outputs=basic_output)
        
        # 2. 链示例
        with gr.Tab("2. 链示例"):
            gr.Markdown("## 链示例")
            
            # 顺序链
            gr.Markdown("### 顺序链 (SequentialChain)")
            text = gr.Textbox(label="输入文本", value="LangChain 是一个强大的框架，用于构建基于大语言模型的应用。")
            english_output = gr.HTML(label="英文翻译")
            summary_output = gr.HTML(label="总结")
            chain_button = gr.Button("执行顺序链")
            
            def chains_handler(text, model):
                result = run_sequential_chain(text, model)
                # 将 Markdown 转换为 HTML
                english_html = f"<div class='output-container'>{markdown.markdown(result['english_text'])}</div>"
                summary_html = f"<div class='output-container'>{markdown.markdown(result['summary'])}</div>"
                return english_html, summary_html
            
            chain_button.click(chains_handler, inputs=[text, model_choice], outputs=[english_output, summary_output])
            
            # 路由链
            gr.Markdown("### 路由链 (RouterChain)")
            router_input = gr.Textbox(label="输入请求", value="请总结以下内容：LangChain 是一个用于构建 LLM 应用的框架")
            router_output = gr.HTML(label="路由链结果")
            router_button = gr.Button("执行路由链")
            
            def router_handler(input_text, model):
                result = run_router_chain(input_text, model)
                # 将 Markdown 转换为 HTML
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
                # 将 Markdown 转换为 HTML
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
            query = gr.Textbox(label="输入查询", value="LangChain 的核心概念")
            docs_output = gr.HTML(label="检索结果")
            doc_button = gr.Button("检索")
            
            def document_handler(query):
                docs = run_document_retrieval(query)
                result = "\n\n".join([f"{doc.page_content} (来源: {doc.metadata['source']})" for doc in docs])
                # 将 Markdown 转换为 HTML
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
                # 将 Markdown 转换为 HTML
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
                # 将结果转换为 HTML
                html = f"<div class='output-container'><p>{result}</p></div>"
                return html
            
            eval_button.click(eval_handler, inputs=[question, answer, reference], outputs=eval_output)
        
        # 7. 总结
        with gr.Tab("7. 总结"):
            gr.Markdown("""
            ## LangChain 核心知识点总结
            
            1. **基础概念**
               - Models: 语言模型接口
               - Prompts: 提示模板
               - Output Parsers: 输出解析器
            
            2. **链 (Chains)**
               - LLMChain: 基础链
               - SequentialChain: 顺序链
               - RouterChain: 路由链
            
            3. **记忆 (Memory)**
               - ConversationBufferMemory: 对话缓冲区
               - ConversationSummaryMemory: 对话摘要
            
            4. **文档处理**
               - Document Loaders: 文档加载器
               - Text Splitters: 文本分割器
               - Embeddings: 嵌入
               - Vector Stores: 向量存储
               - Retrievers: 检索器
            
            5. **工具和代理**
               - Tools: 工具
               - Agents: 代理
               - Toolkits: 工具包
            
            6. **评估**
               - 问答评估
               - 摘要评估
               - 文本生成评估
            
            7. **回调**
               - 跟踪和监控
            
            ## 学习路径
            1. 从基础概念开始
            2. 学习构建简单的链
            3. 添加记忆功能
            4. 处理文档和向量存储
            5. 使用工具和代理
            6. 评估模型性能
            7. 部署和监控
            """)
    
    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    # 定义 CSS 样式
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
