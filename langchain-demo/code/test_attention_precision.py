#!/usr/bin/env python3
"""
测试注意力机制查询的精确性
"""
import os
from demos.a04_document_processing import document_processing_demo

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 执行检索并分析结果
def test_attention_precision(query):
    print(f"查询: {query}")
    print("=" * 70)
    
    # 获取检索器和向量存储
    retriever, _ = document_processing_demo(docs_directory, vector_store_path)
    vector_store = retriever.vectorstore
    
    # 获取带分数的结果
    docs_with_scores = vector_store.similarity_search_with_score(query, k=20)
    docs_with_scores.sort(key=lambda x: x[1])
    
    # 分析每个文档
    print("\n分析文档内容中的注意力机制相关内容:")
    print("-" * 70)
    
    all_docs = [doc for doc, score in docs_with_scores]
    
    # 定义更精确的注意力机制关键词匹配
    def has_direct_attention_content(doc):
        content = doc.page_content.lower()
        
        # 直接相关的注意力机制关键词
        direct_attention_keywords = [
            "attention",
            "注意力机制",
            "自注意力",
            "self-attention",
            "多头注意力",
            "multi-head attention",
            "注意力头",
            "attention head",
            "注意力层",
            "attention layer",
            "注意力计算",
            "注意力权重",
            "注意力分布",
            "注意力掩码",
            "attention mask"
        ]
        
        # 间接相关的注意力提及
        indirect_attention_keywords = [
            "双向注意力",
            "单向注意力",
            "注意力会存在"
        ]
        
        # 检查直接相关关键词
        for keyword in direct_attention_keywords:
            if keyword in content:
                return True, "direct", keyword
        
        # 检查间接相关关键词
        for keyword in indirect_attention_keywords:
            if keyword in content:
                return True, "indirect", keyword
        
        return False, "none", None
    
    # 分析每个文档
    for i, doc in enumerate(all_docs[:10], 1):
        has_attention, attention_type, found_keyword = has_direct_attention_content(doc)
        
        print(f"\n{i}. 文档来源: {doc.metadata['source']}")
        print(f"   注意力相关: {'✅' if has_attention else '❌'}")
        if has_attention:
            print(f"   相关类型: {attention_type} ({found_keyword})")
            
            # 显示包含关键词的上下文
            content = doc.page_content
            content_lower = content.lower()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines):
                if found_keyword in line.lower():
                    start = max(0, line_num - 2)
                    end = min(len(lines), line_num + 3)
                    print(f"   上下文 (行 {line_num + 1}):")
                    for j in range(start, end):
                        if j == line_num:
                            print(f"     >>> {lines[j].strip()}")
                        else:
                            print(f"         {lines[j].strip()}")
                    break

# 运行测试
test_attention_precision("注意力机制")
