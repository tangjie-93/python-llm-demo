#!/usr/bin/env python3
"""
检查向量存储中的内容
"""
from demos.a04_document_processing import document_processing_demo
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录
docs_directory = os.path.join(current_dir, "docs")

# 向量存储路径
vector_store_path = os.path.join(current_dir, "vector_store")

print(f"检查向量存储内容...")
print(f"文档目录: {docs_directory}")
print(f"向量存储路径: {vector_store_path}")

# 加载向量存储
retriever, documents = document_processing_demo(docs_directory, vector_store_path)

print(f"\n总文档数: {len(documents)}")
print("文档来源:")
for doc in documents:
    print(f"  - {doc.metadata['source']}")

# 测试搜索几个关键词
print("\n测试搜索:")
queries = ["损失函数", "注意力机制", "微调", "RAG"]

for query in queries:
    print(f"\n查询: {query}")
    docs = retriever.invoke(query)
    print(f"找到 {len(docs)} 个相关文档:")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.page_content[:150]}... (来源: {doc.metadata['source']})")

# 检查是否有示例文档（来源为doc1, doc2等）
print("\n检查是否有示例文档:")
has_example_docs = any(doc.metadata['source'].startswith('doc') for doc in documents)
if has_example_docs:
    print("❌ 向量存储中仍然包含示例文档!")
    # 找出示例文档
    example_docs = [doc for doc in documents if doc.metadata['source'].startswith('doc')]
    for doc in example_docs:
        print(f"  - 示例文档: {doc.metadata['source']}")
else:
    print("✅ 向量存储中没有示例文档，所有文档都来自PDF文件")
