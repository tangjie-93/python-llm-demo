from collections.abc import Callable
from dataclasses import dataclass


Tool = Callable[[str], str]


@dataclass
class Step:
    thought: str
    tool: str
    argument: str
    observation: str = ""


def search_docs(query: str) -> str:
    return f"找到与“{query}”相关的 3 条内部知识。"


def create_ticket(summary: str) -> str:
    return f"已创建工单：{summary}"


TOOLS: dict[str, Tool] = {
    "search_docs": search_docs,
    "create_ticket": create_ticket,
}


def plan(user_input: str) -> list[Step]:
    if "故障" in user_input or "报错" in user_input:
        return [
            Step("先查知识库定位问题", "search_docs", user_input),
            Step("如果需要跟进，创建工单", "create_ticket", user_input),
        ]
    return [Step("普通问题先查知识库", "search_docs", user_input)]


def run_agent(user_input: str) -> str:
    steps = plan(user_input)
    observations: list[str] = []
    for step in steps:
        tool = TOOLS[step.tool]
        step.observation = tool(step.argument)
        observations.append(f"{step.tool}: {step.observation}")
    return "任务完成。\n" + "\n".join(observations)


if __name__ == "__main__":
    print(run_agent("登录后台时报错 500，帮我处理"))

