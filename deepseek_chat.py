# -*- coding: utf-8 -*-
"""
DeepSeek 聊天助手
基于 Gradio 和 OpenAI SDK 实现的智能对话界面
支持流式输出，实时显示 AI 回复
"""

import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载环境变量文件
load_dotenv()

# 初始化 OpenAI 客户端（用于调用 DeepSeek API）
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 从环境变量获取 API Key
    base_url="https://api.deepseek.com"    # DeepSeek API 基础 URL
)


# 流式获取 AI 回复
def chat_response(message, history, system_prompt, temperature, max_tokens):
    """
    通过 DeepSeek API 获取流式响应
    
    Args:
        message: 用户输入的消息
        history: 对话历史记录
        system_prompt: 系统提示词
        temperature: 控制回答随机性 (0-2)
        max_tokens: 最大生成令牌数
    
    Yields:
        流式返回 AI 的部分回复内容
    """
    # 构建完整的消息列表，包括系统提示词
    messages = [{"role": "system", "content": system_prompt}]
    
    # 限制历史记录长度，只保留最近 4 轮对话（2 个用户消息 + 2 个助手消息）
    # 这样可以减少 token 消耗，同时保持对话连贯性
    max_history = 4
    limited_history = history[-max_history:] if len(history) > max_history else history
    
    # 将历史记录转换为 API 所需的格式
    for msg in limited_history:
        if msg["role"] == "user":
            messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant":
            messages.append({"role": "assistant", "content": msg["content"]})
    
    # 添加当前用户消息
    messages.append({"role": "user", "content": message})
    
    try:
        # 发送流式请求
        response = client.chat.completions.create(
            model="deepseek-chat",  # 使用 DeepSeek 聊天模型
            messages=messages,      # 完整的消息列表
            temperature=temperature,  # 温度参数
            max_tokens=max_tokens,  # 最大令牌数
            stream=True             # 启用流式输出
        )
        
        # 处理流式响应
        partial_message = ""  # 累积的回复内容
        for chunk in response:
            # 检查是否有内容（排除结束标记）
            if chunk.choices[0].delta.content:
                partial_message += chunk.choices[0].delta.content
                # 实时返回部分内容
                yield partial_message
    except Exception as e:
        # 错误处理
        yield f"Error: {str(e)}"


# 清空对话历史
def clear_history():
    """
    清空对话历史
    
    Returns:
        空列表，用于重置聊天记录
    """
    return []


# 创建 Gradio 应用界面
with gr.Blocks(title="DeepSeek Chat Demo") as demo:
    # 标题和描述
    gr.Markdown("# 🤖 DeepSeek 聊天助手")
    gr.Markdown("基于 DeepSeek 大模型的智能对话演示")
    
    # 主布局：左右两列
    with gr.Row():
        # 左侧：聊天区域（占 3/4 宽度）
        with gr.Column(scale=3):
            # 聊天历史显示
            chatbot = gr.Chatbot(
                label="对话历史",
                height=500
            )
            
            # 输入区域：文本框 + 按钮
            with gr.Row(equal_height=True):  # 垂直居中对齐
                msg_input = gr.Textbox(
                    placeholder="在这里输入你的问题...",
                    scale=4,           # 占 4/6 宽度
                    lines=1,           # 单行输入
                    show_label=False,  # 隐藏标签
                    container=False    # 移除外层容器
                )
                send_btn = gr.Button("发送", variant="primary", scale=1)  # 占 1/6 宽度
                clear_btn = gr.Button("清空对话", scale=1)                # 占 1/6 宽度
        
        # 右侧：参数设置（占 1/4 宽度）
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ 参数设置")
            
            # 系统提示词设置
            system_prompt = gr.Textbox(
                label="系统提示词",
                value="你是一个有用的AI助手，请用中文回答问题。",
                lines=4,
                placeholder="设置 AI 的角色和行为..."
            )
            
            # 温度参数滑块
            temperature = gr.Slider(
                minimum=0,          # 最小值
                maximum=2,          # 最大值
                value=0.7,          # 默认值
                step=0.1,           # 步长
                label="Temperature (温度)",
                info="值越高，回答越随机；值越低，回答越确定"
            )
            
            # 最大令牌数滑块
            max_tokens = gr.Slider(
                minimum=100,         # 最小值
                maximum=4000,        # 最大值
                value=1000,          # 默认值
                step=100,            # 步长
                label="Max Tokens (最大令牌数)",
                info="控制回答的最大长度"
            )
            
            # 使用说明
            model_info = gr.Markdown(
                """
                ### ℹ️ 使用说明
                
                1. 设置环境变量 `DEEPSEEK_API_KEY`
                2. 在左侧输入框输入问题
                3. 点击发送或按 Enter 键
                4. 可调整右侧参数优化回答
                
                ### 🔑 获取 API Key
                
                访问 [DeepSeek 官网](https://platform.deepseek.com/) 注册并获取 API Key
                
                ```bash
                export DEEPSEEK_API_KEY="your-api-key"
                ```
                """
            )
    
    # 事件处理：用户发送消息
    def user_message(user_message, history):
        """
        处理用户发送消息事件
        
        Args:
            user_message: 用户输入的消息
            history: 当前对话历史
        
        Returns:
            清空输入框，更新历史记录（添加用户消息和空的助手消息）
        """
        return "", history + [{"role": "user", "content": user_message}, {"role": "assistant", "content": ""}]
    
    # 事件处理：获取 AI 回复
    def bot_message(history, system_prompt, temperature, max_tokens):
        """
        处理获取 AI 回复事件
        
        Args:
            history: 当前对话历史
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大令牌数
        
        Yields:
            实时更新对话历史（显示流式回复）
        """
        # 从历史记录中提取用户消息
        user_message = history[-2]["content"]
        
        # 调用 chat_response 函数获取流式响应
        for partial_response in chat_response(user_message, history[:-2], system_prompt, temperature, max_tokens):
            # 更新助手消息内容
            history[-1] = {"role": "assistant", "content": partial_response}
            # 实时返回更新后的历史记录
            yield history
    
    # 绑定发送按钮点击事件
    send_btn.click(
        user_message,                   # 处理函数
        inputs=[msg_input, chatbot],    # 输入组件
        outputs=[msg_input, chatbot]    # 输出组件
    ).then(                             # 链式调用：用户消息处理完成后
        bot_message,                    # 处理函数
        inputs=[chatbot, system_prompt, temperature, max_tokens],  # 输入组件
        outputs=[chatbot]               # 输出组件
    )
    
    # 绑定输入框回车事件
    msg_input.submit(
        user_message,                   # 处理函数
        inputs=[msg_input, chatbot],    # 输入组件
        outputs=[msg_input, chatbot]    # 输出组件
    ).then(                             # 链式调用：用户消息处理完成后
        bot_message,                    # 处理函数
        inputs=[chatbot, system_prompt, temperature, max_tokens],  # 输入组件
        outputs=[chatbot]               # 输出组件
    )
    
    # 绑定清空按钮点击事件
    clear_btn.click(
        clear_history,                  # 处理函数
        outputs=[chatbot]               # 输出组件
    )


# 启动应用
if __name__ == "__main__":
    demo.launch()  # 启动 Gradio 应用