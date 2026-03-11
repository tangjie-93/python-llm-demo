"""
`LangChain` 基础概念示例
包含：`Models`、`Prompts`、`Output Parsers`
"""
import os
from langchain_core.prompts import (
    ChatPromptTemplate,          # 聊天提示模板
    PromptTemplate,              # 基础文本提示模板
    FewShotPromptTemplate,       # 少样本提示模板
    FewShotChatMessagePromptTemplate,  # 少样本聊天消息提示模板
    SystemMessagePromptTemplate,  # 系统消息提示模板
    HumanMessagePromptTemplate,   # 人类消息提示模板
    AIMessagePromptTemplate,      # AI消息提示模板
    ChatMessagePromptTemplate,    # 聊天消息提示模板
    MessagesPlaceholder,          # 消息占位符
    BasePromptTemplate,           # 基础提示模板基类
    StringPromptTemplate,         # 字符串提示模板
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_llm(model_name="deepseek", streaming=False):
    """获取语言模型"""
    api_key = os.getenv("DEEPSEEK_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
    if model_name == "deepseek":
        # 使用 `DeepSeek` API（`OpenAI` 兼容）
        return ChatOpenAI(
            model="deepseek-chat",
            temperature=0.7,
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            streaming=streaming
        )
    else:
        # 使用 `OpenAI` API
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key,
            streaming=streaming
        )

def basic_concepts_demo(model_name, streaming=False):
    """基础概念示例"""
    llm = get_llm(model_name, streaming=streaming)
    
    # 1. `Prompt` 模板 - 定义可重用的提示结构
    # 1.1 基础文本提示模板 (`PromptTemplate`)
    # 适用于纯文本模型，不包含消息类型
    text_prompt = PromptTemplate(
        input_variables=["topic"],
        template="你是一个专家，帮我详细解释什么是 {topic}，包括其核心组件和使用场景"
    )
    
    # 1.2 聊天提示模板 (`ChatPromptTemplate`)
    # 1.2.1 基础聊天提示模板（使用 from_template）
    basic_chat_prompt = ChatPromptTemplate.from_template(
        "你是一个专家，帮我详细解释什么是 {topic}，包括其核心组件和使用场景"
    )
    
    # 1.2.2 高级聊天提示模板（使用 from_messages）
    # 包含系统消息和用户消息
    advanced_chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的技术讲解专家，擅长清晰解释复杂概念"),
        ("user", "请详细解释什么是 {topic}，包括：\n1. 核心概念\n2. 关键组件\n3. 使用场景\n4. 优势和局限性")
    ])
    
    # 1.3 少样本提示模板 (`FewShotPromptTemplate`)
    # 包含示例的提示模板，适用于需要示例引导的任务
    examples = [
        {"input": "LangChain", "output": "LangChain 是一个构建 LLM 应用的框架"},
        {"input": "OpenAI", "output": "OpenAI 是一家人工智能研究公司"}
    ]
    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="输入: {input}\n输出: {output}"
    )
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="请按照以下示例的格式回答问题：",
        suffix="输入: {topic}\n输出:",
        input_variables=["topic"]
    )
    
    # 1.4 少样本聊天消息提示模板 (`FewShotChatMessagePromptTemplate`)
    # 包含聊天消息示例的提示模板
    chat_examples = [
        {
            "input": "什么是 LangChain？",
            "output": "LangChain 是一个构建 LLM 应用的框架，提供了丰富的组件和工具。"
        },
        {
            "input": "什么是 OpenAI？",
            "output": "OpenAI 是一家人工智能研究公司，开发了 GPT 系列模型。"
        }
    ]
    few_shot_chat_prompt = FewShotChatMessagePromptTemplate(
        examples=chat_examples,
        example_prompt=ChatPromptTemplate.from_messages([
            ("user", "{input}"),
            ("ai", "{output}")
        ]),
        input_variables=["topic"]
    )
    
    # 1.5 系统/人类/AI消息提示模板
    # 1.5.1 系统消息提示模板 (`SystemMessagePromptTemplate`)
    system_prompt = SystemMessagePromptTemplate.from_template(
        "你是一个专业的 {field} 专家，提供准确详细的信息"
    )
    
    # 1.5.2 人类消息提示模板 (`HumanMessagePromptTemplate`)
    human_prompt = HumanMessagePromptTemplate.from_template(
        "请解释什么是 {topic}？"
    )
    
    # 1.5.3 AI消息提示模板 (`AIMessagePromptTemplate`)
    ai_prompt = AIMessagePromptTemplate.from_template(
        "{topic} 是一个重要的概念，它的核心是..."
    )
    
    # 1.5.4 组合消息提示模板
    combined_chat_prompt = ChatPromptTemplate.from_messages([
        system_prompt,
        human_prompt,
        MessagesPlaceholder(variable_name="chat_history"),
        human_prompt
    ])
    
    # 1.6 消息占位符 (`MessagesPlaceholder`)
    # 用于在提示中插入动态消息列表，如对话历史
    history_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个聊天助手，基于对话历史回答问题"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{question}")
    ])
    
    # 1.7 组合提示模板
    # 使用基础 PromptTemplate 组合多个模板
    full_template = """
    你是一个专业的技术专家
    
    例如：Python 是一种编程语言
    
    请解释什么是 {topic}？
    """
    
    # 直接定义包含所有内容的提示模板
    combined_prompt = PromptTemplate(
        input_variables=["topic"],
        template=full_template
    )
    
    # 1.8 选择使用的提示模板
    prompt = advanced_chat_prompt
    
    # 2. 输出解析器 - 处理模型输出
    # 2.1 基础解析器 - `StrOutputParser`
    # 将模型输出解析为字符串
    basic_parser = StrOutputParser()
    
    # 2.2 其他类型的解析器（示例）
    # - `JsonOutputParser`: 解析为 JSON
    # - `PydanticOutputParser`: 解析为 Pydantic 模型
    # - `CommaSeparatedListOutputParser`: 解析为逗号分隔的列表
    
    # 选择使用的解析器
    output_parser = basic_parser
    
    # 3. 链 - 使用 `LCEL` (LangChain Expression Language) 连接组件
    # 3.1 基础链
    # `|` 运算符表示数据流向：prompt → llm → output_parser
    # 1) prompt: 接收输入并渲染模板
    # 2) llm: 接收渲染后的提示并生成回复
    # 3) output_parser: 接收模型输出并解析为字符串
    basic_chain = prompt | llm | output_parser
    
    # 3.2 链的执行流程
    # - 输入: `{"topic": "LangChain"}`
    # - 步骤1: prompt 渲染 → "你是一个专业的技术讲解专家...请详细解释什么是 LangChain..."
    # - 步骤2: llm 生成 → 模型生成的详细解释
    # - 步骤3: output_parser 解析 → 字符串形式的解释
    
    # 3.3 链的调用方式
    # - `chain.invoke(input)`: 同步调用，返回结果
    # - `chain.stream(input)`: 流式调用，返回生成过程
    # - `chain.batch([input1, input2])`: 批量调用，返回多个结果
    
    return basic_chain

def run_demo(topic, model_name="deepseek", streaming=False):
    """运行示例"""
    chain = basic_concepts_demo(model_name, streaming=streaming)
    if streaming:
        # 使用流式调用，返回生成过程
        print("=== 流式返回结果 ===")
        result = ""
        for chunk in chain.stream({"topic": topic}):
            print(chunk, end="", flush=True)
            result += chunk
        print()
        return result
    else:
        # 使用同步调用，返回完整结果
        return chain.invoke({"topic": topic})

def run_all_prompt_demos(model_name="deepseek"):
    """运行所有提示模板示例"""
    llm = get_llm(model_name)
    output_parser = StrOutputParser()
    
    print("=== 1. 基础文本提示模板 (PromptTemplate) ===")
    text_prompt = PromptTemplate(
        input_variables=["topic"],
        template="你是一个专家，帮我解释什么是 {topic}？"
    )
    text_chain = text_prompt | llm | output_parser
    result = text_chain.invoke({"topic": "LangChain"})
    print(result)
    
    print("\n=== 2. 聊天提示模板 (ChatPromptTemplate) ===")
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的技术专家"),
        ("user", "请解释什么是 {topic}？")
    ])
    chat_chain = chat_prompt | llm | output_parser
    result = chat_chain.invoke({"topic": "LangChain"})
    print(result)
    
    print("\n=== 3. 少样本提示模板 (FewShotPromptTemplate) ===")
    examples = [
        {"input": "Python", "output": "Python 是一种高级编程语言"},
        {"input": "JavaScript", "output": "JavaScript 是一种脚本语言"}
    ]
    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="输入: {input}\n输出: {output}"
    )
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="请按照以下示例的格式回答问题：",
        suffix="输入: {topic}\n输出:",
        input_variables=["topic"]
    )
    few_shot_chain = few_shot_prompt | llm | output_parser
    result = few_shot_chain.invoke({"topic": "LangChain"})
    print(result)
    
    print("\n=== 4. 系统消息提示模板 (SystemMessagePromptTemplate) ===")
    system_prompt = SystemMessagePromptTemplate.from_template(
        "你是一个专业的 {field} 专家"
    )
    human_prompt = HumanMessagePromptTemplate.from_template(
        "请解释什么是 {topic}？"
    )
    system_chain = ChatPromptTemplate.from_messages([
        system_prompt,
        human_prompt
    ]) | llm | output_parser
    result = system_chain.invoke({"field": "AI", "topic": "LangChain"})
    print(result)
    
    print("\n=== 5. 消息占位符 (MessagesPlaceholder) ===")
    history_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个聊天助手，基于对话历史回答问题"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{question}")
    ])
    chat_history = [
        ("user", "什么是 LLM？"),
        ("ai", "LLM 是大型语言模型的缩写")
    ]
    history_chain = history_prompt | llm | output_parser
    result = history_chain.invoke({"chat_history": chat_history, "question": "LangChain 和 LLM 有什么关系？"})
    print(result)
    
    print("\n=== 6. 组合提示模板 ===")
    # 直接定义包含所有内容的提示模板
    combined_template = """
    你是一个专业的技术专家
    
    例如：Python 是一种编程语言
    
    请解释什么是 {topic}？
    """
    
    combined_prompt = PromptTemplate(
        input_variables=["topic"],
        template=combined_template
    )
    
    # 使用组合模板
    pipeline_chain = combined_prompt | llm | output_parser
    result = pipeline_chain.invoke({"topic": "LangChain"})
    print(result)

if __name__ == "__main__":
    # 测试基础示例
    print("=== 基础示例 (同步返回) ===")
    result = run_demo("`LangChain`")
    print(result)
    
    # 测试流式返回
    print("\n=== 基础示例 (流式返回) ===")
    run_demo("`LangChain`", streaming=True)
    
    # 测试所有提示模板示例
    print("\n=== 所有提示模板示例 ===")
    run_all_prompt_demos()
