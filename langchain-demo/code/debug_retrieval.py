#!/usr/bin/env python3
"""
调试检索逻辑
"""
import os
from demos.a04_document_processing import document_processing_demo

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 文档目录和向量存储路径
docs_directory = os.path.join(current_dir, "docs")
vector_store_path = os.path.join(current_dir, "vector_store")

# 执行检索并打印详细信息
def debug_retrieval(query):
    print(f"调试查询: {query}")
    print("=" * 70)
    
    # 获取检索器和向量存储
    retriever, _ = document_processing_demo(docs_directory, vector_store_path)
    vector_store = retriever.vectorstore
    
    # 获取带分数的结果
    print("\n1. 获取带相似度分数的结果:")
    print("-" * 70)
    docs_with_scores = vector_store.similarity_search_with_score(query, k=20)
    
    for i, (doc, score) in enumerate(docs_with_scores, 1):
        print(f"{i}. 文档来源: {doc.metadata['source']}, 相似度分数: {score:.4f}")
        content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
        print(f"   内容预览: {content_preview}")
    
    # 设置相似度阈值
    SIMILARITY_THRESHOLD = 0.5
    print(f"\n2. 过滤掉相似度分数 > {SIMILARITY_THRESHOLD} 的文档:")
    print("-" * 70)
    
    filtered_docs_with_scores = [(doc, score) for doc, score in docs_with_scores if score < SIMILARITY_THRESHOLD]
    
    for i, (doc, score) in enumerate(filtered_docs_with_scores, 1):
        print(f"{i}. 文档来源: {doc.metadata['source']}, 相似度分数: {score:.4f}")
    
    # 检查关键词
    print(f"\n3. 检查文档是否包含注意力相关关键词:")
    print("-" * 70)
    
    filtered_docs = [doc for doc, score in filtered_docs_with_scores]
    
    def has_keyword(doc, query):
        content = doc.page_content.lower()
        query_lower = query.lower()
        
        if "注意力机制" in query_lower or "attention" in query_lower:
            # 检查注意力相关关键词
            attention_keywords = ["注意力", "attention", "自注意力", "self-attention", "多头注意力", "multi-head"]
            found_keywords = []
            for keyword in attention_keywords:
                if keyword in content:
                    found_keywords.append(keyword)
            
            if found_keywords:
                return True, found_keywords
            else:
                return False, []
        
        return query_lower in content, [query_lower]
    
    docs_with_keyword = []
    docs_without_keyword = []
    
    for doc in filtered_docs:
        has_key, found_keywords = has_keyword(doc, query)
        if has_key:
            docs_with_keyword.append(doc)
            print(f"✅ 文档 {doc.metadata['source']} 包含关键词: {found_keywords}")
        else:
            docs_without_keyword.append(doc)
            print(f"❌ 文档 {doc.metadata['source']} 不包含注意力相关关键词")
    
    print(f"\n4. 最终返回结果:")
    print("-" * 70)
    print(f"包含关键词的文档数量: {len(docs_with_keyword)}")
    print(f"不包含关键词的文档数量: {len(docs_without_keyword)}")
    
    optimized_docs = docs_with_keyword
    if not optimized_docs:
        optimized_docs = [doc for doc, _ in docs_with_scores[:5]]
    else:
        optimized_docs = optimized_docs[:5]
    
    print(f"\n最终返回 {len(optimized_docs)} 个文档:")
    for i, doc in enumerate(optimized_docs, 1):
        print(f"{i}. 文档来源: {doc.metadata['source']}")

# 运行调试
if __name__ == "__main__":
    debug_retrieval("注意力机制")
