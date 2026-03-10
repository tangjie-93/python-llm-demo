"""
`LangChain` 示例模块
"""

# 可以在这里导出常用的函数
from .a01_basic_concepts import get_llm, run_demo as run_basic_concepts
from .a02_chains import run_sequential_chain, run_router_chain
from .a03_memory import run_memory_demo
from .a04_document_processing import run_document_retrieval, get_all_documents
from .a05_tools_agents import run_agent
from .a06_evaluation import run_evaluation

__all__ = [
    'get_llm',
    'run_basic_concepts',
    'run_sequential_chain',
    'run_router_chain',
    'run_memory_demo',
    'run_document_retrieval',
    'get_all_documents',
    'run_agent',
    'run_evaluation'
]