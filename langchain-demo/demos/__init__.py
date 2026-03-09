"""
LangChain 示例模块
"""

# 可以在这里导出常用的函数
from .a01_basic_concepts import get_llm
from .a02_chains import chains_demo
from .a03_memory import memory_demo
from .a04_document_processing import document_processing_demo
from .a05_tools_agents import tools_demo
from .a06_evaluation import evaluation_demo

__all__ = [
    'get_llm',
    'chains_demo',
    'memory_demo',
    'document_processing_demo',
    'tools_demo',
    'evaluation_demo'
]