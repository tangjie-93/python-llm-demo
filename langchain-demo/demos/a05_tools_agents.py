"""
`LangChain` 工具和代理示例
包含：`Tools`、`Agents`、`Toolkits`
"""
from langchain_core.tools import Tool
from demos.a01_basic_concepts import get_llm

def tools_demo(model_name):
    """工具示例"""
    llm = get_llm(model_name)
    
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
    
    return tools, llm

def run_agent(input_text, model_name="deepseek"):
    """运行代理示例"""
    tools, llm = tools_demo(model_name)
    
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
    from langchain_core.prompts import ChatPromptTemplate
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
