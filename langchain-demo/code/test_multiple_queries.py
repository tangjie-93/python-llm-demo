#!/usr/bin/env python3
"""
测试多个查询的检索效果
"""
from demos.a04_document_processing import run_document_retrieval
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 测试多个查询
queries = ["涌现能力", "损失函数", "注意力机制", "微调", "LLM"]

for query in queries:
    print(f"\n{'-' * 60}")
    print(f"查询: {query}")
    print('-' * 60)
    
    # 执行检索
    docs = run_document_retrieval(query, docs_directory, vector_store_path)
    
    print(f"找到 {len(docs)} 个相关文档:")
    for i, doc in enumerate(docs, 1):
        # 检查是否包含关键词
        has_keyword = query.lower() in doc.page_content.lower()
        status = "✅" if has_keyword else "❌"
        
        print(f"\n{i}. {status} 文档: {doc.metadata['source']}")
        print(f"   内容: {doc.page_content[:150]}...")
