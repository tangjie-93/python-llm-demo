#!/usr/bin/env python3
"""
专门测试注意力机制的查询结果
"""
from demos.a04_document_processing import run_document_retrieval
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 测试查询
query = "注意力机制"

print(f"查询: {query}")
print("=" * 60)

# 执行检索
print("\n执行检索...")
docs = run_document_retrieval(query, docs_directory, vector_store_path, return_only_relevant=True)

print(f"\n找到 {len(docs)} 个相关文档:")
for i, doc in enumerate(docs, 1):
    print(f"\n{i}. 文档来源: {doc.metadata['source']}")
    print(f"   内容长度: {len(doc.page_content)} 字符")
    print(f"   内容:")
    print(f"{doc.page_content}")
    print("-" * 50)
    
    # 检查是否包含注意力相关关键词
    content_lower = doc.page_content.lower()
    has_attention = "attention" in content_lower or "注意力" in content_lower
    print(f"   是否包含注意力相关内容: {'✅' if has_attention else '❌'}")
    print("-" * 50)
