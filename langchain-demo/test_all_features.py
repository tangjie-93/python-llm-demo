"""
测试 LangChain demo 的所有功能
"""
import time
from demos.a01_basic_concepts import run_demo as basic_concepts_run
from demos.a02_chains import run_sequential_chain, run_router_chain
from demos.a03_memory import run_memory_demo
from demos.a04_document_processing import run_document_retrieval, get_all_documents
from demos.a05_tools_agents import run_agent
from demos.a06_evaluation import run_evaluation

def test_basic_concepts():
    """测试基础概念"""
    print("=== 测试基础概念 ===")
    try:
        result = basic_concepts_run("LangChain")
        print("✓ 基础概念测试成功")
        print(f"  结果长度: {len(result)} 字符")
        return True
    except Exception as e:
        print(f"✗ 基础概念测试失败: {e}")
        return False

def test_chains():
    """测试链示例"""
    print("\n=== 测试链示例 ===")
    
    # 测试顺序链
    try:
        sequential_result = run_sequential_chain("LangChain 是一个强大的框架，用于构建基于大语言模型的应用。")
        print("✓ 顺序链测试成功")
        print(f"  英文翻译: {sequential_result['english_text'][:50]}...")
        print(f"  总结: {sequential_result['summary'][:50]}...")
    except Exception as e:
        print(f"✗ 顺序链测试失败: {e}")
        return False
    
    # 测试路由链
    try:
        router_result = run_router_chain("请总结以下内容：LangChain 是一个用于构建 LLM 应用的框架")
        print("✓ 路由链测试成功")
        print(f"  结果: {router_result['result'][:50]}...")
        return True
    except Exception as e:
        print(f"✗ 路由链测试失败: {e}")
        return False

def test_memory():
    """测试记忆示例"""
    print("\n=== 测试记忆示例 ===")
    try:
        # 初始化记忆实例
        memory_instances = {}
        
        # 测试第一轮对话
        response1, history1, memory_instances = run_memory_demo("你好，我是小明", "deepseek", memory_instances)
        print("✓ 第一轮对话测试成功")
        print(f"  回复: {response1[:50]}...")
        
        # 测试第二轮对话（带上下文）
        response2, history2, memory_instances = run_memory_demo("我叫什么名字？", "deepseek", memory_instances)
        print("✓ 第二轮对话测试成功")
        print(f"  回复: {response2[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ 记忆示例测试失败: {e}")
        return False

def test_document_processing():
    """测试文档处理"""
    print("\n=== 测试文档处理 ===")
    try:
        # 测试获取所有文档
        documents = get_all_documents()
        print(f"✓ 获取文档成功，共 {len(documents)} 个文档")
        
        # 测试文档检索
        docs = run_document_retrieval("LangChain 的核心概念")
        print(f"✓ 文档检索成功，找到 {len(docs)} 个相关文档")
        if docs:
            print(f"  第一个文档: {docs[0].page_content[:50]}...")
        return True
    except Exception as e:
        print(f"✗ 文档处理测试失败: {e}")
        return False

def test_tools_agents():
    """测试工具和代理"""
    print("\n=== 测试工具和代理 ===")
    try:
        # 测试简单问题
        response = run_agent("今天北京的天气如何？")
        print("✓ 工具和代理测试成功")
        print(f"  回复: {response[:50]}...")
        return True
    except Exception as e:
        print(f"✗ 工具和代理测试失败: {e}")
        return False

def test_evaluation():
    """测试评估"""
    print("\n=== 测试评估 ===")
    try:
        # 测试评估功能
        result = run_evaluation(
            "LangChain 是什么？",
            "LangChain 是一个用于构建 LLM 应用的框架",
            "LangChain 是一个框架，用于开发由语言模型驱动的应用程序。它提供了一套工具、组件和接口，使开发者能够更轻松地构建复杂的 LLM 应用。"
        )
        print("✓ 评估测试成功")
        print(f"  评估结果: {result}")
        return True
    except Exception as e:
        print(f"✗ 评估测试失败: {e}")
        return False

def test_all_features():
    """测试所有功能"""
    print("开始测试 LangChain demo 的所有功能...\n")
    
    tests = [
        test_basic_concepts,
        test_chains,
        test_memory,
        test_document_processing,
        test_tools_agents,
        test_evaluation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
        time.sleep(1)  # 避免请求过快
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"总测试数: {len(tests)}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查错误信息。")

if __name__ == "__main__":
    test_all_features()
