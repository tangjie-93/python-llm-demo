#!/usr/bin/env python3
"""
简单测试搜索"涌现能力"的结果
"""
from demos.a04_document_processing import run_document_retrieval
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 测试查询
query = "涌现能力"

print(f"查询: {query}")
print("=" * 50)

# 执行检索
docs = run_document_retrieval(query, docs_directory, vector_store_path)

print(f"找到 {len(docs)} 个相关文档:")
for i, doc in enumerate(docs, 1):
    print(f"\n{i}. 文档: {doc.metadata['source']}")
    # 检查是否包含关键词
    if "涌现能力" in doc.page_content:
        print(f"   ✅ 包含关键词 '涌现能力'")
    if "Emergent Capabilities" in doc.page_content:
        print(f"   ✅ 包含关键词 'Emergent Capabilities'")
    # 显示前200个字符
    print(f"   内容: {doc.page_content[:200]}...")
