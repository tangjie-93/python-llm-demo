"""
`LangChain` 记忆示例
包含：`ConversationBufferMemory`、`ConversationSummaryMemory`、`ConversationBufferWindowMemory`、`VectorStoreMemory`
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from demos.a01_basic_concepts import get_llm

def memory_demo(model_name):
    """记忆示例"""
    llm = get_llm(model_name)
    
    # 聊天提示
    chat_prompt = ChatPromptTemplate.from_template("""
    你是一个友好的助手，根据对话历史回答用户的问题。
    
    对话历史：
    {history}
    
    用户：{input}
    助手：
    """)
    
    # 输出解析器
    output_parser = StrOutputParser()
    
    # 聊天链
    chat_chain = chat_prompt | llm | output_parser
    
    def chat_with_memory(input_text, memory_instances):
        """带记忆的聊天"""
        # 获取当前会话的记忆
        session_id = "default"
        if session_id not in memory_instances:
            memory_instances[session_id] = []
        
        # 构建历史记录
        history = "\n".join([f"用户：{msg['user']}\n助手：{msg['assistant']}" for msg in memory_instances[session_id]])
        
        # 生成回复
        response = chat_chain.invoke({"history": history, "input": input_text})
        
        # 更新记忆
        memory_instances[session_id].append({"user": input_text, "assistant": response})
        
        # 限制记忆长度（模拟 `ConversationBufferWindowMemory`）
        if len(memory_instances[session_id]) > 5:
            memory_instances[session_id] = memory_instances[session_id][-5:]
        
        # 构建完整的对话历史
        full_history = "\n".join([f"用户：{msg['user']}\n助手：{msg['assistant']}" for msg in memory_instances[session_id]])
        
        return response, full_history, memory_instances
    
    return chat_with_memory

def run_memory_demo(input_text, model_name="deepseek", memory_instances=None):
    """运行记忆示例"""
    if memory_instances is None:
        memory_instances = {}
    
    chat_func = memory_demo(model_name)
    return chat_func(input_text, memory_instances)

if __name__ == "__main__":
    # 测试记忆功能
    memory_instances = {}
    
    # 第一轮对话
    response1, history1, memory_instances = run_memory_demo("你好，我是小明", "deepseek", memory_instances)
    print("回复1:", response1)
    print("历史1:", history1)
    
    # 第二轮对话
    response2, history2, memory_instances = run_memory_demo("我叫什么名字？", "deepseek", memory_instances)
    print("回复2:", response2)
    print("历史2:", history2)
