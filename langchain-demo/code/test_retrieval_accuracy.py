#!/usr/bin/env python3
"""
测试文档检索的准确性
"""
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

def load_single_pdf(file_path):
    """加载单个PDF文件"""
    loader = PyPDFLoader(file_path)
    return loader.load()

def test_retrieval_accuracy():
    """测试检索准确性"""
    # 1. 加载嵌入模型
    print("加载嵌入模型...")
    local_model_path = "./local_models/bge-small-en-v1.5"
    embeddings = HuggingFaceEmbeddings(
        model_name=local_model_path,
        encode_kwargs={"normalize_embeddings": True}
    )
    
    # 2. 加载测试文档
    print("\n加载测试文档...")
    test_docs = [
        "d:/study/LLM/code/python-llm-demo/langchain-demo/docs/1-大模型（LLMs）基础面.pdf",
        "d:/study/LLM/code/python-llm-demo/langchain-demo/docs/4-Attention 升级面.pdf",
        "d:/study/LLM/code/python-llm-demo/langchain-demo/docs/6-LLMs 损失函数篇.pdf",
        "d:/study/LLM/code/python-llm-demo/langchain-demo/docs/9-大模型（LLMs）微调面.pdf"
    ]
    
    all_documents = []
    for doc_path in test_docs:
        print(f"  加载: {os.path.basename(doc_path)}")
        docs = load_single_pdf(doc_path)
        all_documents.extend(docs)
    
    print(f"\n共加载 {len(all_documents)} 个文档页")
    
    # 3. 文本分割
    print("\n文本分割...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    
    splits = text_splitter.split_documents(all_documents)
    print(f"分割后得到 {len(splits)} 个文本块")
    
    # 4. 创建向量存储
    print("\n创建向量存储...")
    vector_store = FAISS.from_documents(splits, embeddings)
    
    # 5. 测试检索
    print("\n=== 测试检索准确性 ===")
    test_queries = [
        "大模型基础概念",
        "注意力机制详解",
        "损失函数原理",
        "模型微调方法"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        results = vector_store.similarity_search(query, k=3)
        print(f"找到 {len(results)} 个相关结果:")
        
        for i, result in enumerate(results, 1):
            # 显示更多内容以便评估
            content = result.page_content[:200].strip()
            if len(result.page_content) > 200:
                content += "..."
            
            print(f"\n{i}. [{result.metadata['source']}] 第{result.metadata['page']+1}页")
            print(f"   内容: {content}")
            
            # 计算相似度分数
            if hasattr(vector_store, 'similarity_search_with_score'):
                results_with_scores = vector_store.similarity_search_with_score(query, k=3)
                for j, (doc, score) in enumerate(results_with_scores):
                    if doc == result:
                        print(f"   相似度: {1-score:.4f}")  # FAISS返回的是距离，转换为相似度
                        break

if __name__ == "__main__":
    test_retrieval_accuracy()