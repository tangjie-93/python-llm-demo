#!/usr/bin/env python3
"""
测试搜索"涌现能力"关键词
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
query = "涌现能力"

print(f"测试查询: {query}")
print(f"文档目录: {docs_directory}")
print(f"向量存储路径: {vector_store_path}")
print("=" * 60)

# 执行检索
docs = run_document_retrieval(query, docs_directory, vector_store_path)

print(f"\n找到 {len(docs)} 个相关文档:")
for i, doc in enumerate(docs, 1):
    print(f"\n{i}. 文档来源: {doc.metadata['source']}")
    print(f"   内容: {doc.page_content}")
    print("-" * 50)

# 也测试一下其他相关查询
print("\n" + "=" * 60)
print("测试相关查询:")

related_queries = ["大模型涌现能力", "涌现能力原因", "Emergent Capabilities"]
for q in related_queries:
    print(f"\n查询: {q}")
    docs_related = run_document_retrieval(q, docs_directory, vector_store_path)
    print(f"找到 {len(docs_related)} 个相关文档")
    if docs_related:
        print(f"第一个结果来源: {docs_related[0].metadata['source']}")
        print(f"内容片段: {docs_related[0].page_content[:200]}...")
