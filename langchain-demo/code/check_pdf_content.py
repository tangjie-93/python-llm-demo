#!/usr/bin/env python3
"""
检查PDF文档的内容解析情况
"""
import os
from langchain_community.document_loaders import PyPDFLoader

def check_pdf_content(file_path, max_pages=5):
    """检查PDF文档的内容解析情况"""
    print(f"\n=== 检查文档: {os.path.basename(file_path)} ===")
    
    # 加载PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    print(f"总页数: {len(docs)}")
    
    # 检查前几页内容
    for i, doc in enumerate(docs[:max_pages]):
        print(f"\n第{i+1}页内容:")
        print("-" * 50)
        
        content = doc.page_content.strip()
        if len(content) == 0:
            print("[空内容]")
        elif len(content) > 500:
            print(content[:500] + "...")
            print(f"(内容长度: {len(content)} 字符)")
        else:
            print(content)
            
        # 检查元数据
        print(f"元数据: {doc.metadata}")

def main():
    """检查所有文档"""
    docs_dir = "d:/study/LLM/code/python-llm-demo/langchain-demo/docs"
    
    # 检查几个关键文档
    key_docs = [
        "1-大模型（LLMs）基础面.pdf",
        "4-Attention 升级面.pdf",
        "6-LLMs 损失函数篇.pdf"
    ]
    
    for doc_name in key_docs:
        doc_path = os.path.join(docs_dir, doc_name)
        if os.path.exists(doc_path):
            check_pdf_content(doc_path, max_pages=3)
        else:
            print(f"文档不存在: {doc_name}")

if __name__ == "__main__":
    main()