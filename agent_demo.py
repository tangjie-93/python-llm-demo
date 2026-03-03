# -*- coding: utf-8 -*-
"""
DeepSeek Agent Demo
基于 ReAct 模式的智能体实现，支持工具调用和记忆管理
使用 Gradio 作为 UI 框架

ReAct 框架说明：
- Reasoning (思考): 大模型分析用户需求，决定是否需要使用工具
- Acting (行动): 如果需要工具，输出工具名称和参数
- Observation (观察): 执行工具，获取结果
- 最终回答: 基于观察结果，大模型生成最终回复
"""

import gradio as gr
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Callable
from datetime import datetime
import requests
import textwrap
from tavily import TavilyClient

# 加载环境变量
load_dotenv()

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


class Tool:
    """工具基类"""
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
    
    def execute(self, **kwargs) -> str:
        try:
            result = self.func(**kwargs)
            return str(result)
        except Exception as e:
            return f"工具执行错误: {str(e)}"


class Agent:
    """
    DeepSeek Agent 实现
    基于 ReAct 模式（Reasoning + Acting + Observation）
    
    ReAct 完整流程：
    1. Reasoning: 大模型分析用户需求，输出思考过程
    2. Acting: 如果需要工具，输出 "行动: 工具名" 和 "参数: {...}"
    3. Observation: 系统执行工具，获取结果
    4. 最终回答: 大模型基于观察结果生成最终回复（第2次大模型调用）
    """
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.memory: List[Dict[str, str]] = []  # 对话历史
        self.max_memory = 3  # 最大记忆轮数
        self.setup_tools()
    
    def setup_tools(self):
        """初始化可用工具"""
        # 工具 1: 计算器
        self.tools["calculator"] = Tool(
            name="calculator",
            description="执行数学计算，如加减乘除、幂运算等",
            func=self._calculator
        )
        
        # 工具 2: 天气查询（模拟）
        self.tools["weather"] = Tool(
            name="weather",
            description="查询指定城市的当前天气",
            func=self._weather
        )
        
        # 工具 3: 当前时间
        self.tools["time"] = Tool(
            name="time",
            description="获取当前日期和时间",
            func=self._time
        )
        
        # 工具 4: 网页搜索
        self.tools["search"] = Tool(
            name="search",
            description="搜索网络信息，获取最新资讯和知识",
            func=self._search
        )
    
    def _calculator(self, expression: str) -> str:
        """计算器工具"""
        try:
            # 安全计算，只允许基本运算符
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return "错误：表达式包含非法字符"
            result = eval(expression)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    def _weather(self, city: str) -> str:
        """天气查询工具（使用 Open-Meteo API + 模拟数据）"""
        try:
            # 使用 Open-Meteo API（免费、稳定、快速）
            # 1. 获取城市坐标
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=zh&format=json"
            geo_response = requests.get(geo_url, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data.get('results'):
                raise Exception(f"未找到城市: {city}")
            
            location = geo_data['results'][0]
            lat = location['latitude']
            lon = location['longitude']
            name = location.get('name', city)
            country = location.get('country', '')
            
            # 2. 获取天气数据
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            weather_response = requests.get(weather_url, timeout=10)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            current = weather_data['current']
            
            # 天气代码映射
            weather_codes = {
                0: "晴朗", 1: "多云", 2: "阴天", 3: "阴天",
                45: "雾", 48: "雾",
                51: "小雨", 53: "小雨", 55: "小雨",
                61: "小雨", 63: "中雨", 65: "大雨",
                80: "阵雨", 81: "阵雨", 82: "阵雨",
                95: "雷阵雨", 96: "雷阵雨", 99: "雷阵雨"
            }
            
            weather_code = current.get('weather_code', 0)
            weather_desc = weather_codes.get(weather_code, "未知")
            
            # 构建天气信息
            weather_info = f"{name}, {country} 当前天气：\n"
            weather_info += f"🌡️ 温度: {current['temperature_2m']}°C\n"
            weather_info += f"💨 风速: {current['wind_speed_10m']} km/h\n"
            weather_info += f"💧 湿度: {current['relative_humidity_2m']}%\n"
            weather_info += f"☁️ 天气: {weather_desc}"
            
            return weather_info
            
        except Exception as e:
            # API 失败，使用模拟数据
            import random
            weather_types = ["晴天", "多云", "阴天", "小雨", "中雨", "大雨", "雷阵雨", "雾"]
            
            mock_data = {
                'location': city,
                'temp': str(random.randint(15, 35)),
                'wind': str(random.randint(5, 30)),
                'humidity': str(random.randint(40, 90)),
                'weather': random.choice(weather_types)
            }
            
            weather_info = f"{mock_data['location']} 当前天气（模拟数据）：\n"
            weather_info += f"🌡️ 温度: {mock_data['temp']}°C\n"
            weather_info += f"💨 风速: {mock_data['wind']} km/h\n"
            weather_info += f"💧 湿度: {mock_data['humidity']}%\n"
            weather_info += f"☁️ 天气: {mock_data['weather']}"
            
            return weather_info
    
    def _time(self) -> str:
        """获取当前时间"""
        now = datetime.now()
        return f"当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}"
    
    def _search(self, query: str) -> str:
        """网页搜索工具（使用 Tavily API，每月 1000 次免费）"""
        try:
            # 获取 Tavily API Key
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                return "错误：未配置 TAVILY_API_KEY 环境变量\n请访问 https://tavily.com 注册获取免费 API Key（每月 1000 次）"
            
            # 初始化 Tavily 客户端
            tavily_client = TavilyClient(api_key=api_key)
            
            # 执行搜索
            response = tavily_client.search(
                query=query,
                max_results=5,
                search_depth="basic",  # basic 或 advanced
                include_answer=True,     # 包含 AI 总结
                include_raw_content=False
            )
            
            # 格式化搜索结果
            search_result = f"🔍 搜索 '{query}' 的结果：\n\n"
            
            # 添加 AI 总结（如果有）
            if response.get("answer"):
                search_result += f"📝 智能总结：\n{response['answer']}\n\n"
            
            # 添加详细结果
            search_result += "🔗 相关网页：\n"
            for i, result in enumerate(response.get("results", []), 1):
                title = result.get("title", "无标题")
                url = result.get("url", "")
                content = result.get("content", "")
                score = result.get("score", 0)
                
                search_result += f"{i}. **{title}** (相关度: {score:.2f})\n"
                search_result += f"   {content[:200]}...\n"
                search_result += f"   🔗 {url}\n\n"
            
            return search_result.strip()
                
        except Exception as e:
            return f"搜索 '{query}' 时出错：{str(e)}\n\n提示：请检查 TAVILY_API_KEY 是否正确，或访问 https://tavily.com 获取"
    
    def get_tools_description(self) -> str:
        """获取工具描述，用于 Prompt"""
        tools_desc = "可用工具:\n"
        for name, tool in self.tools.items():
            tools_desc += f"- {name}: {tool.description}\n"
        tools_desc += "\n使用工具时，请按以下格式输出:\n"
        tools_desc += "思考: <你的思考过程>\n"
        tools_desc += "行动: <工具名称>\n"
        tools_desc += "参数: <JSON格式的参数>\n"
        return tools_desc
    
    def parse_action(self, text: str) -> tuple:
        """
        解析 Agent 的行动（ReAct 中的 Acting 阶段）
        
        解析大模型输出的思考、行动和参数
        格式示例：
            思考: 用户想查询天气，我需要使用 weather 工具
            行动: weather
            参数: {"city": "北京"}
        """
        lines = text.strip().split('\n')
        thought = ""
        action = None
        params = {}
        
        for line in lines:
            if line.startswith("思考:"):
                thought = line[3:].strip()
            elif line.startswith("行动:"):
                action = line[3:].strip()
            elif line.startswith("参数:"):
                try:
                    params = json.loads(line[3:].strip())
                except:
                    params = {}
        
        return thought, action, params
    
    def run_stream(self, user_input: str, system_prompt: str = ""):
        """
        运行 Agent（流式返回，完整的 ReAct 流程）
        
        ReAct 完整流程：
        ┌─────────────────────────────────────────────────────────────┐
        │  Step 1: Reasoning (思考)                                    │
        │  调用大模型分析用户需求，输出思考过程                          │
        │  → 输出: "思考: 用户想查询天气，我需要使用 weather 工具"       │
        └─────────────────────────────────────────────────────────────┘
                                ↓
        ┌─────────────────────────────────────────────────────────────┐
        │  Step 2: Acting (行动)                                       │
        │  解析大模型输出，识别工具调用请求                              │
        │  → 识别: "行动: weather" + "参数: {"city": "北京"}"            │
        └─────────────────────────────────────────────────────────────┘
                                ↓
        ┌─────────────────────────────────────────────────────────────┐
        │  Step 3: Observation (观察)                                  │
        │  执行工具，获取结果                                           │
        │  → 执行: _weather("北京") → 返回天气数据                       │
        └─────────────────────────────────────────────────────────────┘
                                ↓
        ┌─────────────────────────────────────────────────────────────┐
        │  Step 4: 最终回答 (第2次大模型调用)                           │
        │  将观察结果传给大模型，生成最终回复                            │
        │  → 输入: 用户问题 + 工具结果                                   │
        │  → 输出: "北京今天天气晴朗，温度25°C..."                       │
        └─────────────────────────────────────────────────────────────┘
        
        Args:
            user_input: 用户输入
            system_prompt: 系统提示词
        
        Yields:
            流式返回的回复片段，包含完整的 ReAct 流程
        """
        # =====================================================================
        # Step 0: 准备阶段 - 构建系统提示词和消息列表
        # =====================================================================
        full_system_prompt = system_prompt or textwrap.dedent("""\
            你是一个智能助手，可以使用工具来帮助用户解决问题。
            请按照 ReAct 模式（思考-行动-观察）来工作。
            如果需要使用工具，请按以下格式输出:
            思考: <你的思考过程>
            行动: <工具名称>
            参数: <JSON格式的参数，如 {"expression": "1+1"}>

            重要提示：
            1. 优先使用内置工具解决问题
            2. 每个工具都有固定的参数要求，请严格按照工具描述使用参数
            3. 如果工具调用失败，系统会显示错误信息，请直接告诉用户错误原因
            4. 如果问题不需要使用内置工具，直接回答用户即可
        """)
        
        # 添加工具描述到系统提示词
        full_system_prompt += "\n\n" + self.get_tools_description()
        
        # 构建消息列表（包含系统提示词和历史记忆）
        messages = [{"role": "system", "content": full_system_prompt}]
        
        # 添加记忆（限制长度，避免超出上下文限制）
        recent_memory = self.memory[-self.max_memory:] if len(self.memory) > self.max_memory else self.memory
        for msg in recent_memory:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 添加当前用户输入
        messages.append({"role": "user", "content": user_input})
        
        # =====================================================================
        # Step 1: Reasoning (思考阶段)
        # 调用大模型分析用户需求，输出思考过程
        # =====================================================================
        try:
            # 第 1 次调用大模型：分析需求，决定是否使用工具
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=True
            )
            
            # 收集大模型的思考和行动计划
            assistant_reply = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    assistant_reply += content
                    # 流式输出大模型的思考过程
                    yield assistant_reply
            
            # =====================================================================
            # Step 2: Acting (行动阶段)
            # 解析大模型输出，判断是否需要调用工具
            # =====================================================================
            thought, action, params = self.parse_action(assistant_reply)
            
            # 如果需要调用工具
            if action and action in self.tools:
                # 显示工具调用 loading 效果
                loading_message = f"\n\n🔄 正在调用工具 `{action}`，请稍候...\n"
                yield assistant_reply + loading_message
                
                try:
                    # =====================================================================
                    # Step 3: Observation (观察阶段)
                    # 执行工具，获取结果
                    # =====================================================================
                    tool_result = self.tools[action].execute(**params)
                    
                    # 显示工具执行结果
                    observation_display = f"\n\n---\n\n"
                    observation_display += f"**🛠️ 工具执行结果（Observation）**\n\n"
                    observation_display += f"{tool_result}\n\n"
                    observation_display += f"---\n"
                    yield assistant_reply + observation_display
                    
                    # =====================================================================
                    # Step 4: 最终回答（第2次大模型调用）
                    # 基于观察结果，让大模型生成最终回复
                    # =====================================================================
                    # 构建第2次调用的消息列表
                    # 包含：系统提示词 + 历史记忆 + 用户问题 + 第1次回复 + 工具结果
                    final_messages = [
                        {"role": "system", "content": full_system_prompt}
                    ]
                    
                    # 添加历史记忆
                    for msg in recent_memory:
                        final_messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    # 添加用户问题
                    final_messages.append({"role": "user", "content": user_input})
                    
                    # 添加第1次大模型的回复（作为 assistant 的消息）
                    final_messages.append({"role": "assistant", "content": assistant_reply})
                    
                    # 添加工具执行结果（作为 tool 角色的消息）
                    # 注意：这里使用 user 角色来传递观察结果，因为 DeepSeek 不支持 tool 角色
                    final_messages.append({
                        "role": "user", 
                        "content": f"工具执行结果：\n{tool_result}\n\n请基于以上结果回答用户的问题。"
                    })
                    
                    # 显示第2次大模型调用的提示
                    final_thinking = f"\n🤔 正在基于观察结果生成最终回答...\n"
                    yield assistant_reply + observation_display + final_thinking
                    
                    # 第 2 次调用大模型：基于观察结果生成最终回复
                    final_response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=final_messages,
                        temperature=0.7,
                        max_tokens=2000,
                        stream=True
                    )
                    
                    # 收集最终回复
                    final_reply = ""
                    for chunk in final_response:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            final_reply += content
                            # 流式输出最终回复
                            yield assistant_reply + observation_display + final_thinking + final_reply
                    
                    # 构建完整的回复（包含 ReAct 全流程）
                    full_reply = assistant_reply + observation_display + final_thinking + final_reply
                    
                    # 更新记忆（保存完整的对话）
                    self.memory.append({"role": "user", "content": user_input})
                    self.memory.append({"role": "assistant", "content": full_reply})
                    
                except Exception as tool_error:
                    # 工具执行失败，显示错误信息
                    error_message = f"\n\n---\n\n"
                    error_message += f"**❌ 工具调用失败**\n\n"
                    error_message += f"{str(tool_error)}\n\n"
                    error_message += f"---\n"
                    yield assistant_reply + error_message
                    
                    # 更新记忆
                    self.memory.append({"role": "user", "content": user_input})
                    self.memory.append({"role": "assistant", "content": assistant_reply + error_message})
            else:
                # 不需要调用工具，直接使用第1次大模型的回复
                # 更新记忆
                self.memory.append({"role": "user", "content": user_input})
                self.memory.append({"role": "assistant", "content": assistant_reply})
                
        except Exception as e:
            yield f"错误: {str(e)}"
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []
        return "记忆已清空"


# 创建 Agent 实例
agent = Agent()


def chat_with_agent(message, history, system_prompt):
    """
    与 Agent 对话（流式）
    
    Args:
        message: 用户消息
        history: 对话历史（Gradio 格式）
        system_prompt: 系统提示词
    
    Yields:
        更新后的历史和空字符串
    """
    # 将 Gradio 历史转换为 Agent 记忆格式
    agent.memory = []
    for msg in history:
        # 判断msg是否为字典
        if isinstance(msg, dict):
            # 新格式：字典列表
            if msg.get("role") == "user":
                agent.memory.append({"role": "user", "content": msg.get("content", "")})
            elif msg.get("role") == "assistant":
                agent.memory.append({"role": "assistant", "content": msg.get("content", "")})
        elif isinstance(msg, (list, tuple)) and len(msg) >= 2:
            # 旧格式：[[user_msg, assistant_msg], ...]
            user_msg, assistant_msg = msg[0], msg[1]
            if user_msg:
                agent.memory.append({"role": "user", "content": user_msg})
            if assistant_msg:
                agent.memory.append({"role": "assistant", "content": assistant_msg})
    
    # 添加用户消息到历史
    history.append({"role": "user", "content": message})
    
    # 流式获取 Agent 回复
    partial_response = ""
    for partial_reply in agent.run_stream(message, system_prompt):
        partial_response = partial_reply
        # 更新最后一条助手消息
        if len(history) > 0 and history[-1].get("role") == "assistant":
            history[-1]["content"] = partial_response
        else:
            history.append({"role": "assistant", "content": partial_response})
        yield history, ""


def clear_chat():
    """清空对话"""
    agent.clear_memory()
    return [], "对话已清空"


# 创建 Gradio 界面
with gr.Blocks(title="DeepSeek Agent Demo") as demo:
    gr.Markdown("# 🤖 DeepSeek Agent 智能体演示")
    gr.Markdown("基于完整 ReAct 模式的智能体，支持工具调用（计算器、天气查询、时间、搜索）")
    
    with gr.Row():
        # 左侧：对话区域
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="对话历史",
                height=500
            )
            
            with gr.Row(equal_height=True):
                msg_input = gr.Textbox(
                    placeholder="输入你的问题，例如：北京今天天气怎么样？或者计算 123 * 456",
                    scale=4,
                    lines=1,
                    show_label=False,
                    container=False
                )
                send_btn = gr.Button("发送", variant="primary", scale=1)
                clear_btn = gr.Button("清空", scale=1)
        
        # 右侧：设置区域
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ 设置")
            
            system_prompt = gr.Textbox(
                label="系统提示词",
                value="你是一个智能助手，可以使用工具来帮助用户解决问题。",
                lines=4,
                placeholder="设置 Agent 的行为和角色..."
            )
            
            gr.Markdown("### 🛠️ 可用工具")
            gr.Markdown("""
            - **calculator**: 数学计算
            - **weather**: 天气查询
            - **time**: 当前时间
            - **search**: 网页搜索（Tavily API，每月1000次免费）
            """)
            
            gr.Markdown("### 🧠 ReAct 框架说明")
            gr.Markdown("""
            **完整 ReAct 流程：**
            
            1. **🤔 Reasoning（思考）**
               - 大模型分析需求
               - 决定是否使用工具
            
            2. **🔄 Acting（行动）**
               - 识别工具调用
               - 执行工具函数
            
            3. **👁️ Observation（观察）**
               - 获取工具结果
               - 整理观察数据
            
            4. **💬 最终回答**
               - 第2次大模型调用
               - 基于观察生成回复
            """)
            
            gr.Markdown("### 💡 示例")
            gr.Markdown("""
            1. "计算 123 + 456"
            2. "北京今天天气怎么样？"
            3. "现在几点了？"
            4. "什么是人工智能？"
            """)
    
    # 事件绑定
    send_btn.click(
        chat_with_agent,
        inputs=[msg_input, chatbot, system_prompt],
        outputs=[chatbot, msg_input]
    )
    
    msg_input.submit(
        chat_with_agent,
        inputs=[msg_input, chatbot, system_prompt],
        outputs=[chatbot, msg_input]
    )
    
    clear_btn.click(
        clear_chat,
        outputs=[chatbot, msg_input]
    )


if __name__ == "__main__":
    demo.launch()
