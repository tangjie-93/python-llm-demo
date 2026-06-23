import gradio as gr


def greet(name, intensity):
    return f"Hello, {name}!" + "!" * int(intensity)

def calculator(num1, num2, operation):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2 if num2 != 0 else "Error: Division by zero"


def text_analyzer(text):
    word_count = len(text.split())
    char_count = len(text)
    return f"字数: {word_count} 词, 字符数: {char_count} 个"


with gr.Blocks(title="Gradio Demo") as demo:
    gr.Markdown("# 🚀 Gradio Demo 示例")
    gr.Markdown("这是一个使用 Gradio 创建的交互式 Web 应用演示")

    with gr.Tab("问候"):
        gr.Markdown("### 简单的问候功能")
        name_input = gr.Textbox(label="你的名字", placeholder="请输入名字...")
        intensity_slider = gr.Slider(
            minimum=1, maximum=10, value=1, step=1, label="热情程度"
        )
        greet_output = gr.Textbox(label="问候语")
        greet_btn = gr.Button("打招呼")
        greet_btn.click(fn=greet, inputs=[name_input, intensity_slider], outputs=greet_output)

    with gr.Tab("计算器"):
        gr.Markdown("### 简单计算器")
        with gr.Row():
            num1 = gr.Number(label="数字 1", value=0)
            num2 = gr.Number(label="数字 2", value=0)
        operation = gr.Radio(choices=["+", "-", "*", "/"], label="运算", value="+")
        calc_result = gr.Number(label="结果")
        calc_btn = gr.Button("计算")
        calc_btn.click(fn=calculator, inputs=[num1, num2, operation], outputs=calc_result)

    with gr.Tab("文本分析"):
        gr.Markdown("### 文本统计工具")
        text_input = gr.Textbox(
            label="输入文本", placeholder="在这里输入文字...", lines=5
        )
        text_output = gr.Textbox(label="分析结果")
        analyze_btn = gr.Button("分析")
        analyze_btn.click(fn=text_analyzer, inputs=text_input, outputs=text_output)

    gr.Markdown("---")
    gr.Markdown("Made with ❤️ using Gradio")


if __name__ == "__main__":
    demo.launch()
