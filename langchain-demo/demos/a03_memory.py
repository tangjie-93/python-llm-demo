"""
LangChain 记忆示例
使用简单的字典来保存对话历史
"""
from langchain_core.prompts import ChatPromptTemplate
from demos.a01_basic_concepts import get_llm

def memory_demo(model_name):
    """记忆示例"""
    llm = get_llm(model_name)
    
    prompt = ChatPromptTemplate.from_template("{chat_history}\nHuman: {input}\nAI:")
    
    # 使用简单的字典来保存对话历史
    memory = {"chat_history": []}
    
    # 使用 LangChain 1.0+ 语法
    def chat_chain(input_text, memory=memory):
        # 获取历史记录
        chat_history = memory["chat_history"]
        # 构建完整的提示
        history_str = "\n".join(chat_history)
        full_prompt = prompt.format(chat_history=history_str, input=input_text)
        # 调用模型
        response = llm.invoke(full_prompt)
        # 保存对话
        chat_history.append(f"Human: {input_text}")
        chat_history.append(f"AI: {response.content}")
        return response.content
    
    return chat_chain, memory

def run_memory_demo(input_text, model_name="deepseek", memory_instances=None):
    """运行记忆示例"""
    if memory_instances is None:
        memory_instances = {}
    
    if model_name not in memory_instances:
        chain, memory = memory_demo(model_name)
        memory_instances[model_name] = (chain, memory)
    else:
        chain, memory = memory_instances[model_name]
    
    result = chain(input_text)
    history = "\n".join(memory["chat_history"])
    
    return result, history, memory_instances

if __name__ == "__main__":
    # 测试记忆功能
    memory_instances = {}
    
    # 第一次对话
    response, history, memory_instances = run_memory_demo("你好，我叫小明", "deepseek", memory_instances)
    print("第一次回复:", response)
    print("对话历史:", history)
    
    # 第二次对话
    response, history, memory_instances = run_memory_demo("我喜欢编程", "deepseek", memory_instances)
    print("第二次回复:", response)
    print("对话历史:", history)
