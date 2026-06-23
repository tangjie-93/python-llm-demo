#!/usr/bin/env python3
"""
重新创建向量存储，确保所有PDF内容都被正确索引
"""
from demos.a04_document_processing import document_processing_demo
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录
docs_directory = os.path.join(current_dir, "docs")

# 向量存储路径
vector_store_path = os.path.join(current_dir, "vector_store")

print(f"重新创建向量存储...")
print(f"文档目录: {docs_directory}")
print(f"向量存储路径: {vector_store_path}")
print("=" * 60)

# 删除旧的向量存储文件（如果存在）
if os.path.exists(vector_store_path):
    for file in os.listdir(vector_store_path):
        file_path = os.path.join(vector_store_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(f"已删除旧的向量存储文件")

# 重新创建向量存储
retriever, documents = document_processing_demo(docs_directory, vector_store_path)

print(f"\n向量存储创建完成！")
print(f"索引的文档数: {len(documents)}")
print("文档来源:")
for i, doc in enumerate(documents[:5], 1):  # 只显示前5个
    print(f"  {i}. {doc.metadata['source']}")
if len(documents) > 5:
    print(f"  ... 还有 {len(documents) - 5} 个文档")

# 测试搜索"涌现能力"
print("\n" + "=" * 60)
print("测试搜索: 涌现能力")
docs = retriever.invoke("涌现能力")
print(f"找到 {len(docs)} 个相关文档:")
for i, doc in enumerate(docs, 1):
    print(f"\n{i}. 文档来源: {doc.metadata['source']}")
    print(f"   内容: {doc.page_content}")
    print("-" * 50)
