#!/usr/bin/env python3
"""
优化的文档检索脚本，提高检索准确性
"""
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs(directory):
    """加载目录中的所有PDF文件"""
    documents = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    loader = PyPDFLoader(file_path)
                    loaded_docs = loader.load()
                    for doc in loaded_docs:
                        # 过滤掉只有"知识星球"的页面
                        if doc.page_content.strip() != "知识星球":
                            doc.metadata['source'] = file
                            documents.append(doc)
                    print(f"成功加载: {file} ({len(loaded_docs)}页，有效{len([d for d in loaded_docs if d.page_content.strip() != '知识星球'])}页)")
                except Exception as e:
                    print(f"加载失败 {file}: {e}")
    return documents

def optimize_retrieval():
    """优化的文档检索"""
    print("=== 优化的文档检索系统 ===")
    
    # 1. 加载嵌入模型
    print("\n1. 加载嵌入模型...")
    # 优先使用中文模型
    local_model_path_zh = "./local_models/bge-small-zh-v1.5"
    if os.path.exists(local_model_path_zh):
        print(f"使用本地中文模型: {local_model_path_zh}")
        embeddings = HuggingFaceEmbeddings(
                model_name=local_model_path_zh,
                encode_kwargs={"normalize_embeddings": True},
                show_progress=True
            )
    else:
        # 回退到英文模型
        local_model_path_en = "./local_models/bge-small-en-v1.5"
        if os.path.exists(local_model_path_en):
            print(f"使用本地英文模型: {local_model_path_en}")
            embeddings = HuggingFaceEmbeddings(
                model_name=local_model_path_en,
                encode_kwargs={"normalize_embeddings": True},
                show_progress=True
            )
        else:
            print("尝试使用在线中文模型...")
            embeddings = HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-zh-v1.5",  # 中文轻量级模型，更适合中文文档
                encode_kwargs={"normalize_embeddings": True},
                show_progress=True
            )
    
    # 2. 加载文档
    print("\n2. 加载文档...")
    docs_directory = "d:/study/LLM/code/python-llm-demo/langchain-demo/docs"
    documents = load_pdfs(docs_directory)
    print(f"共加载 {len(documents)} 个有效文档页")
    
    # 3. 优化的文本分割
    print("\n3. 文本分割...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 增大块大小，保留更多上下文信息
        chunk_overlap=200,  # 增大重叠比例（20%），确保重要内容不会被分割
        length_function=len,  # 使用中文字符长度计算
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", "、", " ", ""]  # 添加更多中文分隔符
    )
    
    splits = text_splitter.split_documents(documents)
    print(f"分割后得到 {len(splits)} 个文本块")
    
    # 4. 创建向量存储
    print("\n4. 创建向量存储...")
    vector_store = FAISS.from_documents(splits, embeddings)
    
    # 5. 测试检索
    print("\n5. === 测试检索准确性 ===")
    test_queries = [
        "大模型基础概念",
        "注意力机制详解",
        "损失函数原理",
        "模型微调方法",
        "Multi-Query Attention",
        "KL散度与交叉熵的区别"
    ]
    
    # 创建两种检索器进行对比
    similarity_retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    mmr_retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,  # 返回更多结果用于筛选
            "fetch_k": 30,  # 先获取更多结果再进行MMR排序
            "lambda_mult": 0.7  # 相关性权重（0.7表示更注重相关性）
        }
    )
    
    # 优化相似度阈值 - 使用中文模型后需要大幅降低阈值
    SIMILARITY_THRESHOLD = 0.35  # 调整阈值以适应中文模型的相似度分布
    
    for query in test_queries:
        print(f"\n查询: {query}")
        
        # 使用similarity_search_with_score获取带相似度的结果
        results_with_scores = vector_store.similarity_search_with_score(query, k=10)
        
        # 过滤掉相似度低于阈值的结果
        filtered_results = [(doc, score) for doc, score in results_with_scores 
                          if (1-score) > SIMILARITY_THRESHOLD]
        
        # 按相似度排序
        filtered_results.sort(key=lambda x: (1-x[1]), reverse=True)
        
        print(f"找到 {len(filtered_results)} 个相关结果:")
        
        for i, (result, score) in enumerate(filtered_results[:3], 1):  # 只显示前3个
            content = result.page_content[:250].strip()  # 显示更多内容以便评估
            if len(result.page_content) > 250:
                content += "..."
            
            print(f"\n{i}. [{result.metadata['source']}] 第{result.metadata['page']+1}页")
            print(f"   内容: {content}")
            print(f"   相似度: {1-score:.4f}")
            
            # 显示元数据中的更多信息
            if 'source' in result.metadata:
                print(f"   来源: {result.metadata['source']}")

if __name__ == "__main__":
    optimize_retrieval()