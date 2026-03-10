"""
`LangChain` 链示例
包含：`LLMChain`、`SequentialChain`、`RouterChain`、`RetrievalQAChain`
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from demos.a01_basic_concepts import get_llm

def sequential_chain_demo(model_name):
    """顺序链示例"""
    llm = get_llm(model_name)
    
    # 翻译提示
    translate_prompt = ChatPromptTemplate.from_template("将以下文本翻译成英文：{text}")
    
    # 总结提示
    summary_prompt = ChatPromptTemplate.from_template("总结以下英文文本：{english_text}")
    
    # 输出解析器
    output_parser = StrOutputParser()
    
    # 翻译链
    translate_chain = translate_prompt | llm | output_parser
    
    # 总结链
    summary_chain = summary_prompt | llm | output_parser
    
    def sequential_chain(text):
        """顺序执行翻译和总结"""
        english_text = translate_chain.invoke({"text": text})
        summary = summary_chain.invoke({"english_text": english_text})
        return {
            "english_text": english_text,
            "summary": summary
        }
    
    return sequential_chain

def router_chain_demo(model_name):
    """路由链示例"""
    llm = get_llm(model_name)
    
    # 翻译提示
    translate_prompt = ChatPromptTemplate.from_template("将以下文本翻译成英文：{text}")
    
    # 总结提示
    summary_prompt = ChatPromptTemplate.from_template("总结以下文本：{text}")
    
    # 输出解析器
    output_parser = StrOutputParser()
    
    # 翻译链
    translate_chain = translate_prompt | llm | output_parser
    
    # 总结链
    summary_chain = summary_prompt | llm | output_parser
    
    def router_chain(input_text):
        """根据输入内容路由到不同的链"""
        # 简单的路由逻辑
        if "翻译" in input_text or "translate" in input_text.lower():
            # 提取需要翻译的文本
            text_to_translate = input_text.replace("翻译", "").replace("translate", "").strip()
            result = translate_chain.invoke({"text": text_to_translate})
            return {"result": f"翻译结果：\n{result}"}
        elif "总结" in input_text or "summary" in input_text.lower():
            # 提取需要总结的文本
            text_to_summary = input_text.replace("总结", "").replace("summary", "").strip()
            result = summary_chain.invoke({"text": text_to_summary})
            return {"result": f"总结结果：\n{result}"}
        else:
            # 默认使用总结链
            result = summary_chain.invoke({"text": input_text})
            return {"result": f"总结结果：\n{result}"}
    
    return router_chain

def run_sequential_chain(text, model_name="deepseek"):
    """运行顺序链"""
    chain = sequential_chain_demo(model_name)
    return chain(text)

def run_router_chain(input_text, model_name="deepseek"):
    """运行路由链"""
    chain = router_chain_demo(model_name)
    return chain(input_text)

if __name__ == "__main__":
    # 测试顺序链
    text = "`LangChain` 是一个强大的框架，用于构建基于大语言模型的应用。"
    result = run_sequential_chain(text)
    print("英文翻译:", result["english_text"])
    print("总结:", result["summary"])
    
    # 测试路由链
    input_text = "请总结以下内容：`LangChain` 是一个用于构建 `LLM` 应用的框架"
    result = run_router_chain(input_text)
    print("路由链结果:", result["result"])
