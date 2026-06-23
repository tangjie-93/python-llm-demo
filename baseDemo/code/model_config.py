# -*- coding: utf-8 -*-
"""Shared model provider configuration for OpenAI-compatible chat APIs."""

import os
from dataclasses import dataclass
from typing import List, Optional

from openai import OpenAI


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str
    api_key: Optional[str]
    base_url: Optional[str] = None


def get_model_config(provider: Optional[str] = None) -> ModelConfig:
    """Return config for the selected model provider."""
    selected = (provider or os.getenv("MODEL_PROVIDER") or "deepseek").strip().lower()

    if selected == "deepseek":
        return ModelConfig(
            provider="deepseek",
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        )

    if selected == "openai":
        return ModelConfig(
            provider="openai",
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL") or None,
        )

    raise ValueError(f"不支持的模型提供商: {selected}")


def get_client(provider: Optional[str] = None) -> OpenAI:
    """Create an OpenAI SDK client for the selected provider."""
    config = get_model_config(provider)
    client_kwargs = {"api_key": config.api_key}
    if config.base_url:
        client_kwargs["base_url"] = config.base_url
    return OpenAI(**client_kwargs)


def get_model_choices() -> List[str]:
    return ["deepseek", "openai"]
