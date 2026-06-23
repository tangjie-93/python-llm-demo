#!/usr/bin/env python3
"""
在PDF文档中搜索"RAG"关键词
"""
import os
from PyPDF2 import PdfReader

def search_rag_in_pdfs(directory):
    """在指定目录的所有PDF文档中搜索"RAG"关键词"""
    print(f"搜索目录: {directory}")
    print("=" * 60)
    
    # 获取目录中的所有PDF文件
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("没有找到PDF文件")
        return
    
    found_rag = False
    
    # 遍历所有PDF文件
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        print(f"\n检查文档: {pdf_file}")
        
        try:
            # 打开PDF文件
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                
                # 遍历所有页面
                for page_num, page in enumerate(reader.pages, 1):
                    # 提取页面内容
                    text = page.extract_text()
                    
                    if text:
                        # 搜索"RAG"关键词
                        if "RAG" in text or "rag" in text:
                            found_rag = True
                            print(f"  第 {page_num} 页找到 'RAG' 关键词")
                            # 显示上下文
                            lines = text.split('\n')
                            for i, line in enumerate(lines):
                                if "RAG" in line or "rag" in line:
                                    start = max(0, i-2)
                                    end = min(len(lines), i+3)
                                    print("  上下文:")
                                    for j in range(start, end):
                                        if j == i:
                                            print(f"    >>> {lines[j].strip()}")
                                        else:
                                            print(f"        {lines[j].strip()}")
        
        except Exception as e:
            print(f"  读取文档失败: {e}")
    
    print("\n" + "=" * 60)
    if found_rag:
        print("成功在PDF文档中找到'RAG'关键词")
    else:
        print("没有在任何PDF文档中找到'RAG'关键词")

if __name__ == "__main__":
    # 文档目录
    docs_directory = "d:\study\LLM\code\python-llm-demo\langchain-demo\docs"
    search_rag_in_pdfs(docs_directory)
