import langchain
print("LangChain version:", langchain.__version__)

# 检查langchain.agents模块
try:
    import langchain.agents
    print("\nAvailable in langchain.agents:")
    for item in dir(langchain.agents):
        if not item.startswith('_'):
            print(f"  - {item}")
except Exception as e:
    print(f"Error accessing langchain.agents: {e}")

# 搜索AgentExecutor
try:
    from langchain.agents import AgentExecutor
    print("\nFound AgentExecutor in langchain.agents")
except ImportError:
    print("\nAgentExecutor not in langchain.agents")
    # 尝试在其他地方查找
    try:
        from langchain_core.agents import AgentExecutor
        print("Found AgentExecutor in langchain_core.agents")
    except ImportError:
        print("AgentExecutor not in langchain_core.agents")
        # 尝试在langgraph中查找
        try:
            from langgraph.prebuilt import AgentExecutor
            print("Found AgentExecutor in langgraph.prebuilt")
        except ImportError:
            print("AgentExecutor not found in any known location")