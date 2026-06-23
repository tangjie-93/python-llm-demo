#!/usr/bin/env python3
"""
测试文档检索功能
"""
from demos.a04_document_processing import run_document_retrieval
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录
docs_directory = os.path.join(current_dir, "docs")

# 向量存储路径
vector_store_path = os.path.join(current_dir, "vector_store")

# 测试查询
query = "RAG"

print(f"测试查询: {query}")
print(f"文档目录: {docs_directory}")
print(f"向量存储路径: {vector_store_path}")

# 执行检索
docs = run_document_retrieval(query, docs_directory, vector_store_path)

print(f"\n找到 {len(docs)} 个相关文档:")
for i, doc in enumerate(docs, 1):
    print(f"{i}. {doc.page_content[:200]}... (来源: {doc.metadata['source']})")
