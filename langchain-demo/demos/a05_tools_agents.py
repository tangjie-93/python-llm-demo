"""
`LangChain` 工具和代理示例
包含：`Tools`、`Agents`、`Toolkits`
"""
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from demos.a01_basic_concepts import get_llm

def get_tools():
    """获取工具列表"""
    # 模拟搜索工具（`Tools` 示例）
    def search(query):
        """模拟搜索工具"""
        return f"[模拟搜索结果] 关于 '{query}' 的搜索结果"
    
    # 自定义计算工具（`Tools` 示例）
    def calculate(expression):
        """计算数学表达式"""
        try:
            return str(eval(expression))
        except:
            return "计算错误"
    
    # 工具列表
    tools = [
        Tool(
            name="Search",
            func=search,
            description="用于搜索最新信息"
        ),
        Tool(
            name="Calculator",
            func=calculate,
            description="用于计算数学表达式"
        )
    ]
    
    return tools

def create_tool_agent(model_name):
    """创建真实的代理（使用 LangChain 1.2.10 新 API）"""
    llm = get_llm(model_name)
    tools = get_tools()
    
    # 代理系统提示
    system_prompt = "你是一个助手，需要根据用户的请求决定使用哪些工具。请分析用户的问题，然后选择合适的工具来回答。如果需要搜索信息，使用 Search 工具。如果需要计算数学表达式，使用 Calculator 工具。如果不需要工具，直接回答用户的问题。"
    
    # 创建代理图
    agent_graph = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        debug=True
    )
    
    return agent_graph

def run_agent(input_text, model_name="deepseek"):
    """运行代理示例"""
    try:
        # 使用真实的代理
        agent_graph = create_tool_agent(model_name)
        
        # 准备输入
        inputs = {"messages": [{"role": "user", "content": input_text}]}
        
        # 执行代理
        final_response = ""
        for chunk in agent_graph.stream(inputs, stream_mode="updates"):
            # 检查是否有消息更新
            if "messages" in chunk:
                messages = chunk["messages"]
                if messages and messages[-1].get("role") == "assistant":
                    final_response = messages[-1].get("content", "")
                    break
        
        if not final_response:
            # 如果没有获取到助手回复，尝试获取最后一条消息
            for chunk in agent_graph.stream(inputs, stream_mode="values"):
                if "messages" in chunk:
                    messages = chunk["messages"]
                    if messages:
                        final_response = messages[-1].get("content", "")
                        break
        
        return final_response if final_response else "未获取到有效回复"
    except Exception as e:
        print(f"代理执行出错: {e}")
        # 错误处理，使用简单逻辑作为 fallback
        tools = get_tools()
        
        # 简单的代理逻辑（模拟 `Agents` 功能）
        if "天气" in input_text or "搜索" in input_text:
            # 使用搜索工具
            search_tool = tools[0]
            return search_tool.run(input_text)
        elif "计算" in input_text or "+" in input_text or "-" in input_text or "*" in input_text or "/" in input_text:
            # 提取表达式
            import re
            expr = re.search(r'[\d\+\-\*/]+', input_text)
            if expr:
                calc_tool = tools[1]
                return calc_tool.run(expr.group())
        
        # 默认使用 `LLM`
        llm = get_llm(model_name)
        prompt = ChatPromptTemplate.from_template("{input}")
        chain = prompt | llm
        return chain.invoke({"input": input_text}).content

if __name__ == "__main__":
    # 测试搜索工具
    result = run_agent("今天北京的天气如何？")
    print("搜索结果:", result)
    
    # 测试计算工具
    result = run_agent("计算 123 + 456")
    print("计算结果:", result)
    
    # 测试直接回答
    result = run_agent("什么是 LangChain？")
    print("直接回答:", result)
