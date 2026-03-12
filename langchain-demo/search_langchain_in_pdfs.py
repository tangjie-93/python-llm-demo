#!/usr/bin/env python3
"""
在PDF文档中搜索"LangChain"关键词
"""
import os
from langchain_community.document_loaders import PyPDFLoader

def search_langchain_in_pdfs(directory):
    """在指定目录的所有PDF文档中搜索"LangChain"关键词"""
    print(f"搜索目录: {directory}")
    print("=" * 60)
    
    # 获取目录中的所有PDF文件
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("没有找到PDF文件")
        return
    
    found_langchain = False
    
    # 遍历所有PDF文件
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        print(f"\n检查文档: {pdf_file}")
        
        try:
            # 使用PyPDFLoader加载PDF
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            
            # 遍历所有页面
            for page_num, page in enumerate(pages, 1):
                text = page.page_content
                
                if text:
                    # 搜索"LangChain"关键词
                    if "LangChain" in text or "langchain" in text:
                        found_langchain = True
                        print(f"  第 {page_num} 页找到 'LangChain' 相关内容")
                        # 显示上下文
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            if "LangChain" in line or "langchain" in line:
                                start = max(0, i-3)
                                end = min(len(lines), i+4)
                                print("  上下文:")
                                for j in range(start, end):
                                    if j == i:
                                        print(f"    >>> {lines[j].strip()}")
                                    else:
                                        print(f"        {lines[j].strip()}")
                                print()
        
        except Exception as e:
            print(f"  读取文档失败: {e}")
    
    print("\n" + "=" * 60)
    if found_langchain:
        print("成功在PDF文档中找到'LangChain'相关内容")
    else:
        print("没有在任何PDF文档中找到'LangChain'相关内容")

if __name__ == "__main__":
    # 文档目录
    docs_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "docs"))
    search_langchain_in_pdfs(docs_directory)
