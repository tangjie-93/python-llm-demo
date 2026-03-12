#!/usr/bin/env python3
"""
调试注意力机制查询结果
"""
from demos.a04_document_processing import run_document_retrieval
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 手动检查文档内容
print("手动检查文档内容是否包含注意力相关关键词...")
print("=" * 60)

# 测试文档路径
test_doc_path = os.path.join(docs_directory, "9-大模型（LLMs）微调面.pdf")

# 使用PyPDFLoader加载文档
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(test_doc_path)
docs = loader.load()

print(f"文档 {test_doc_path} 共有 {len(docs)} 页")

# 检查每一页是否包含注意力相关关键词
for page_num, doc in enumerate(docs, 1):
    content = doc.page_content
    content_lower = content.lower()
    
    # 检查注意力相关关键词
    has_attention_keywords = False
    attention_keywords = ["注意力", "attention", "自注意力", "self-attention", "多头注意力", "multi-head"]
    
    for keyword in attention_keywords:
        if keyword in content_lower:
            has_attention_keywords = True
            print(f"第 {page_num} 页包含关键词 '{keyword}'")
            
            # 显示包含关键词的上下文
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if keyword in line.lower():
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    print("上下文:")
                    for j in range(start, end):
                        if j == i:
                            print(f"  >>> {lines[j].strip()}")
                        else:
                            print(f"      {lines[j].strip()}")
                    print()
            break
    
    if not has_attention_keywords:
        print(f"第 {page_num} 页不包含注意力相关关键词")

print("\n" + "=" * 60)
print("调试完成")
