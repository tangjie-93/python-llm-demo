from langchain.agents import create_agent
from langchain_core.tools import Tool
from demos.a01_basic_concepts import get_llm

# 获取LLM实例
llm = get_llm("deepseek")

# 创建一个简单的工具
def test_tool(query):
    """测试工具"""
    return f"测试工具结果: {query}"

tools = [
    Tool(
        name="TestTool",
        func=test_tool,
        description="用于测试的工具"
    )
]

# 查看create_agent函数的文档
print("create_agent函数文档:")
print(create_agent.__doc__)

# 查看create_agent函数的签名
print("\ncreate_agent函数签名:")
import inspect
print(inspect.signature(create_agent))

# 查看create_agent函数的完整帮助
print("\ncreate_agent函数完整帮助:")
help(create_agent)