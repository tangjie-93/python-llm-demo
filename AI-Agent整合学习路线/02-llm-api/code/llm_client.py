import json
import os
from dataclasses import dataclass
from typing import Any

from openai import OpenAI


@dataclass
class LLMConfig:
    model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    temperature: float = 0.2


class LLMClient:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content or ""

    def json_chat(self, system: str, user: str) -> dict[str, Any]:
        content = self.chat(
            system=f"{system}\n只返回 JSON，不要返回 Markdown。",
            user=user,
        )
        return json.loads(content)


if __name__ == "__main__":
    llm = LLMClient()
    print(llm.chat("你是一个简洁的 Python 导师。", "用三句话解释 FastAPI。"))

