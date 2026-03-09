"""
LangChain 链示例
包含：LLMChain、SequentialChain、RouterChain
"""
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from demos.a01_basic_concepts import get_llm

def chains_demo(model_name):
    """链示例"""
    llm = get_llm(model_name)
    
    # 1. 翻译链
    translation_prompt = ChatPromptTemplate.from_template("将 '{text}' 翻译成英文")
    translation_chain = translation_prompt | llm | StrOutputParser()
    
    # 2. 总结链
    summary_prompt = ChatPromptTemplate.from_template("总结以下英文文本: {text}")
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    # 3. 顺序链
    def sequential_chain(text):
        english_text = translation_chain.invoke({"text": text})
        summary = summary_chain.invoke({"text": english_text})
        return {"english_text": english_text, "summary": summary}
    
    return sequential_chain

def router_chain_demo(model_name):
    """路由链示例"""
    llm = get_llm(model_name)
    
    # 创建不同的链
    translation_prompt = ChatPromptTemplate.from_template("将 '{text}' 翻译成英文")
    translation_chain = translation_prompt | llm | StrOutputParser()
    
    summary_prompt = ChatPromptTemplate.from_template("总结以下文本: {text}")
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    # 创建路由链
    def router_chain(input_text):
        # 简单的路由逻辑
        if "翻译" in input_text or "translate" in input_text.lower():
            return {"result": translation_chain.invoke({"text": input_text})}
        else:
            return {"result": summary_chain.invoke({"text": input_text})}
    
    return router_chain

def run_sequential_chain(text, model_name="deepseek"):
    """运行顺序链"""
    chain = chains_demo(model_name)
    return chain(text)

def run_router_chain(input_text, model_name="deepseek"):
    """运行路由链"""
    chain = router_chain_demo(model_name)
    return chain(input_text)

if __name__ == "__main__":
    # 测试顺序链
    result = run_sequential_chain("LangChain 是一个强大的框架，用于构建基于大语言模型的应用。")
    print("英文翻译:", result["english_text"])
    print("总结:", result["summary"])
    
    # 测试路由链
    result = run_router_chain("请总结以下内容：LangChain 是一个用于构建 LLM 应用的框架")
    print("路由链结果:", result["result"])
