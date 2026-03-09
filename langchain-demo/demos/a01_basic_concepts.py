"""
LangChain 基础概念示例
包含：Models、Prompts、Output Parsers
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_llm(model_name="deepseek"):
    """获取语言模型"""
    api_key = os.getenv("DEEPSEEK_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
    if model_name == "deepseek":
        # 使用 DeepSeek API（OpenAI 兼容）
        return ChatOpenAI(
            model="deepseek-chat",
            temperature=0.7,
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
    else:
        # 使用 OpenAI API
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )

def basic_concepts_demo(model_name):
    """基础概念示例"""
    llm = get_llm(model_name)
    
    # Prompt 模板
    prompt = ChatPromptTemplate.from_template("你是一个专家，帮我解释什么是 {topic}")
    
    # 输出解析器
    output_parser = StrOutputParser()
    
    # 链
    chain = prompt | llm | output_parser
    
    return chain

def run_demo(topic, model_name="deepseek"):
    """运行示例"""
    chain = basic_concepts_demo(model_name)
    return chain.invoke({"topic": topic})

if __name__ == "__main__":
    # 测试
    result = run_demo("LangChain")
    print(result)
