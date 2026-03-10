"""
`LangChain` 评估示例
包含：问答评估、摘要评估、文本生成评估
"""
from demos.a01_basic_concepts import get_llm

def evaluation_demo():
    """评估示例"""
    llm = get_llm("deepseek")
    return llm

def run_evaluation(question, answer, reference):
    """运行评估"""
    # 简单的评估逻辑：比较回答和参考答案的相似度
    # 实际应用中可以使用更复杂的评估方法
    
    # 计算简单的相似度（基于词汇重叠）
    answer_words = set(answer.lower().split())
    reference_words = set(reference.lower().split())
    
    if not answer_words or not reference_words:
        similarity = 0
    else:
        intersection = answer_words.intersection(reference_words)
        union = answer_words.union(reference_words)
        similarity = len(intersection) / len(union) * 100
    
    # 生成评估结果
    evaluation_result = f"评估结果:\n" \
                      f"问题: {question}\n" \
                      f"模型回答: {answer}\n" \
                      f"参考回答: {reference}\n" \
                      f"相似度: {similarity:.2f}%\n" \
                      f"评估类型: 问答评估 (基于词汇相似度)"
    
    return evaluation_result

if __name__ == "__main__":
    # 测试评估
    result = run_evaluation(
        question="`LangChain` 是什么？",
        answer="`LangChain` 是一个用于构建 `LLM` 应用的框架",
        reference="`LangChain` 是一个框架，用于开发由语言模型驱动的应用程序。它提供了一套工具、组件和接口，使开发者能够更轻松地构建复杂的 `LLM` 应用。"
    )
    print("评估结果:", result)
