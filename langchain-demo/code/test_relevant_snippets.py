#!/usr/bin/env python3
"""
测试返回相关片段功能
"""
from demos.a04_document_processing import run_document_retrieval
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 测试查询
queries = ["注意力机制", "损失函数", "涌现能力"]

for query in queries:
    print(f"\n{'='*60}")
    print(f"查询: {query}")
    print('='*60)
    
    # 测试返回相关片段
    print("\n1. 返回相关片段:")
    print("-" * 40)
    
    docs = run_document_retrieval(query, docs_directory, vector_store_path, return_only_relevant=True)
    
    print(f"找到 {len(docs)} 个相关文档:")
    for i, doc in enumerate(docs, 1):
        print(f"\n{i}. 文档来源: {doc.metadata['source']}")
        print(f"   内容长度: {len(doc.page_content)} 字符")
        print(f"   内容:")
        print(f"{doc.page_content}")
        print("-" * 30)
    
    # 测试返回完整文档（对比）
    print("\n2. 返回完整文档 (对比):")
    print("-" * 40)
    
    full_docs = run_document_retrieval(query, docs_directory, vector_store_path, return_only_relevant=False)
    
    if full_docs:
        print(f"第一个文档完整内容长度: {len(full_docs[0].page_content)} 字符")
        print(f"完整内容开头: {full_docs[0].page_content[:200]}...")
        print("-" * 30)
