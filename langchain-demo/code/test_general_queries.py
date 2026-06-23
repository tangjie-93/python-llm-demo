#!/usr/bin/env python3
"""
测试通用查询功能
"""
from demos.a04_document_processing import run_document_retrieval
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 测试多个查询
queries = [
    "涌现能力",
    "损失函数",
    "微调",
    "LangChain",  # 应该没有结果，因为文档库中没有LangChain内容
    "transformer"
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"查询: {query}")
    print('='*60)
    
    # 执行检索
    docs = run_document_retrieval(query, docs_directory, vector_store_path, return_only_relevant=True)
    
    if not docs:
        print(f"\n没有找到包含 '{query}' 的相关文档")
        continue
    
    print(f"\n找到 {len(docs)} 个相关文档:")
    for i, doc in enumerate(docs, 1):
        print(f"\n{i}. 文档来源: {doc.metadata['source']}")
        print(f"   内容长度: {len(doc.page_content)} 字符")
        print(f"   内容预览:")
        print(f"{doc.page_content[:300]}...")
        print("-" * 40)
