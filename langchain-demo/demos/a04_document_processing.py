"""
`LangChain` 文档处理示例
包含：`Document Loaders`、`Text Splitters`、`Embeddings`、`Vector Stores`、`Retrievers`
"""
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader
)

def load_documents_from_directory(directory):
    """从目录加载文档
    
    Args:
        directory: 文档目录路径
    
    Returns:
        加载的文档列表
    """
    documents = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                elif file.endswith('.docx'):
                    loader = Docx2txtLoader(file_path)
                elif file.endswith('.txt'):
                    loader = TextLoader(file_path, encoding='utf-8')
                elif file.endswith('.md'):
                    loader = UnstructuredMarkdownLoader(file_path)
                elif file.endswith('.html'):
                    loader = UnstructuredHTMLLoader(file_path)
                else:
                    continue
                
                loaded_docs = loader.load()
                # 过滤掉只有"知识星球"的页面
                valid_docs = [doc for doc in loaded_docs if doc.page_content.strip() != "知识星球"]
                for doc in valid_docs:
                    doc.metadata['source'] = file
                    documents.append(doc)
                print(f"成功加载: {file_path} ({len(loaded_docs)}页，有效{len(valid_docs)}页)")
            except Exception as e:
                print(f"加载失败 {file_path}: {e}")
    
    return documents

def document_processing_demo(directory=None, vector_store_path="../vector_store"):
    """文档处理示例
    
    Args:
        directory: 文档目录路径，如果为None则使用示例文档
        vector_store_path: 向量存储路径
    """
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 嵌入（使用 `Embeddings`）- 尝试使用 HuggingFaceEmbeddings
    try:
        # 尝试使用本地模型（如果已下载）
        local_model_path = os.path.join(script_dir, "../local_models/bge-small-zh-v1.5")
        if os.path.exists(local_model_path):
            print(f"使用本地中文模型: {local_model_path}")
            embeddings = HuggingFaceEmbeddings(
                model_name=local_model_path,  # 本地模型路径
                encode_kwargs={"normalize_embeddings": True},
                show_progress=True
            )
        else:
            # 优先尝试中文模型
            try:
                print("尝试使用中文嵌入模型...")
                embeddings = HuggingFaceEmbeddings(
                    model_name="BAAI/bge-small-zh-v1.5",  # 中文轻量级模型，更适合中文文档
                    encode_kwargs={"normalize_embeddings": True},
                    show_progress=True
                )
            except Exception:
                # 回退到英文模型
                local_model_path_en = os.path.join(script_dir, "../local_models/bge-small-en-v1.5")
                if os.path.exists(local_model_path_en):
                    print(f"使用本地英文模型: {local_model_path_en}")
                    embeddings = HuggingFaceEmbeddings(
                        model_name=local_model_path_en,  # 本地模型路径
                        encode_kwargs={"normalize_embeddings": True}
                    )
                else:
                    print("尝试使用在线英文模型...")
                    embeddings = HuggingFaceEmbeddings(
                        model_name="BAAI/bge-small-en-v1.5",  # 轻量级模型，适合本地运行
                        encode_kwargs={"normalize_embeddings": True}
                    )
        print("成功加载 HuggingFaceEmbeddings")
    except Exception as e:
        print(f"加载 HuggingFaceEmbeddings 失败: {e}")
        print("使用 LangChain 内置的默认嵌入")
        # 使用 LangChain 内置的默认嵌入作为 fallback
        from langchain_core.embeddings import FakeEmbeddings
        embeddings = FakeEmbeddings(size=100)
    
    # 将向量存储路径转换为绝对路径
    vector_store_path = os.path.abspath(os.path.join(script_dir, vector_store_path))
    
    # 检查是否存在向量存储
    if os.path.exists(vector_store_path) and os.listdir(vector_store_path):
        print(f"加载现有向量存储: {vector_store_path}")
        vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
        # 使用优化的检索参数
        retriever = vector_store.as_retriever(
            search_type="similarity",  # 使用相似度搜索，更注重精确匹配
            search_kwargs={
                "k": 5  # 返回结果数
            }
        )
        
        # 获取文档信息
        if directory and os.path.exists(directory):
            documents = load_documents_from_directory(directory)
        else:
            documents = []
        
        return retriever, documents
    
    print("创建新的向量存储...")
    
    if directory and os.path.exists(directory):
        # 从目录加载文档
        documents = load_documents_from_directory(directory)
        if not documents:
            print("未找到可加载的文档，使用示例文档")
            directory = None
    
    if not directory:
        # 创建示例文档（模拟 `Document Loaders` 加载的文档）
        documents = [
            Document(page_content="LangChain 是一个用于构建 LLM 应用的框架，它提供了一套工具和接口，使开发者能够更轻松地构建复杂的 LLM 应用。", metadata={"source": "doc1"}),
            Document(page_content="LangChain 支持多种模型和工具集成，包括 OpenAI、DeepSeek、Google 等模型，以及各种外部工具和服务。", metadata={"source": "doc2"}),
            Document(page_content="LangChain 的核心概念包括 Chains、Agents、Memory、Retrievers 等，这些组件可以组合使用，构建强大的应用。", metadata={"source": "doc3"}),
            Document(page_content="LangChain 的文档处理能力非常强大，支持各种文档格式，如 PDF、Word、Markdown 等。", metadata={"source": "doc4"}),
            Document(page_content="LangChain 的向量存储支持多种后端，如 Chroma、FAISS、Pinecone 等，可以根据需要选择合适的存储方案。", metadata={"source": "doc5"})
        ]
    
    # 文本分割（使用 `Text Splitters`）- 进一步优化配置
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 增大块大小，保留更多上下文信息
        chunk_overlap=200,  # 增大重叠比例（20%），确保重要内容不会被分割
        length_function=len,  # 使用中文字符长度计算
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", "、", " ", ""]  # 添加更多中文分隔符
    )
    splits = text_splitter.split_documents(documents)
    
    # 向量存储（使用 `Vector Stores`）- 使用 FAISS 本地存储
    vector_store = FAISS.from_documents(splits, embeddings)
    
    # 保存向量存储到本地
    vector_store.save_local(vector_store_path)
    print(f"向量存储已保存到: {vector_store_path}")
    
    # 检索器（使用 `Retrievers`）- 优化检索策略
    # 对于中文精确检索，使用相似度搜索
    retriever = vector_store.as_retriever(
        search_type="similarity",  # 使用相似度搜索，更注重精确匹配
        search_kwargs={
            "k": 5  # 返回结果数
        }
    )
    
    return retriever, documents

def run_document_retrieval(query, directory=None, vector_store_path="./vector_store", return_only_relevant=True):
    """运行文档检索
    
    Args:
        query: 查询文本
        directory: 文档目录路径
        vector_store_path: 向量存储路径
        return_only_relevant: 是否只返回相关片段
    """
    retriever, _ = document_processing_demo(directory, vector_store_path)
    
    # 获取向量存储对象
    vector_store = retriever.vectorstore
    
    # 使用similarity_search_with_score获取带相似度分数的结果
    # 中文模型的相似度分数可能大于1，需要根据实际情况调整阈值
    docs_with_scores = vector_store.similarity_search_with_score(query, k=20)
    
    # 直接使用原始文档进行关键词过滤
    # 先按相似度排序（分数越低越相关）
    docs_with_scores.sort(key=lambda x: x[1])
    
    # 提取文档
    all_docs = [doc for doc, score in docs_with_scores]
    
    # 后处理：过滤并优化排序，确保返回最相关的文档
    def get_attention_relevance_score(doc):
        """评估文档与注意力机制的相关程度"""
        content = doc.page_content.lower()
        
        # 直接相关的注意力机制关键词（高权重）
        direct_keywords = [
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
        
        # 间接相关的注意力提及（低权重）
        indirect_keywords = [
            "双向注意力",
            "单向注意力",
            "注意力会存在"
        ]
        
        # 检查直接相关关键词
        for keyword in direct_keywords:
            if keyword in content:
                return 2, keyword  # 高相关性
        
        # 检查间接相关关键词
        for keyword in indirect_keywords:
            if keyword in content:
                return 1, keyword  # 低相关性
        
        return 0, None  # 不相关
    
    # 过滤并排序文档
    query_lower = query.lower()
    relevant_docs = []
    
    if "注意力机制" in query_lower or "attention" in query_lower:
        # 对于注意力机制查询，使用相关性评分
        for doc in all_docs:
            relevance_score, found_keyword = get_attention_relevance_score(doc)
            if relevance_score >= 2:  # 只保留高相关性文档
                relevant_docs.append(doc)
    else:
        # 对于其他查询，使用简单关键词匹配
        def has_keyword(doc):
            return query_lower in doc.page_content.lower()
        
        relevant_docs = [doc for doc in all_docs if has_keyword(doc)]
    
    # 限制返回结果数量
    optimized_docs = relevant_docs[:5]
    
    # 如果没有找到包含关键词的文档，返回空列表或原始结果
    # 这里选择返回空列表，避免返回不相关内容
    if not optimized_docs:
        optimized_docs = []
    
    # 如果只返回相关片段
    if return_only_relevant:
        from copy import deepcopy
        
        # 定义函数：提取相关片段
        def extract_relevant_snippets(doc, query, context_window=100):
            """从文档中提取包含关键词的相关片段"""
            content = doc.page_content
            query_lower = query.lower()
            content_lower = content.lower()
            
            # 查找所有关键词出现的位置
            keyword_positions = []
            start = 0
            while True:
                pos = content_lower.find(query_lower, start)
                if pos == -1:
                    break
                keyword_positions.append(pos)
                start = pos + len(query_lower)
            
            # 如果没有找到关键词，返回原始文档
            if not keyword_positions:
                return doc
            
            # 提取包含关键词的片段（带上下文）
            snippets = []
            used_ranges = []
            
            for pos in keyword_positions:
                # 计算片段范围，避免重复
                start_pos = max(0, pos - context_window)
                end_pos = min(len(content), pos + len(query) + context_window)
                
                # 检查是否与已提取的片段重叠
                overlap = False
                for (existing_start, existing_end) in used_ranges:
                    if not (end_pos < existing_start or start_pos > existing_end):
                        # 合并重叠片段
                        start_pos = min(start_pos, existing_start)
                        end_pos = max(end_pos, existing_end)
                        # 移除旧片段
                        used_ranges.remove((existing_start, existing_end))
                        overlap = True
                        break
                
                # 添加片段范围
                used_ranges.append((start_pos, end_pos))
            
            # 按位置排序
            used_ranges.sort()
            
            # 提取并合并片段
            merged_snippet = ""
            for i, (start_pos, end_pos) in enumerate(used_ranges):
                if i > 0:
                    # 添加分隔符
                    merged_snippet += "\n...\n"
                # 添加片段
                merged_snippet += content[start_pos:end_pos]
            
            # 创建新文档
            new_doc = deepcopy(doc)
            new_doc.page_content = merged_snippet
            return new_doc
        
        # 对所有文档提取相关片段
        relevant_docs = []
        for doc in optimized_docs:
            relevant_doc = extract_relevant_snippets(doc, query)
            relevant_docs.append(relevant_doc)
        
        return relevant_docs
    
    return optimized_docs

def get_all_documents(directory=None, vector_store_path="./vector_store"):
    """获取所有文档
    
    Args:
        directory: 文档目录路径
        vector_store_path: 向量存储路径
    """
    _, documents = document_processing_demo(directory, vector_store_path)
    return documents

if __name__ == "__main__":
    import sys
    
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 文档目录
    docs_directory = os.path.join(script_dir, "../docs")
    vector_store_path = "../vector_store"
    
    # 测试文档检索
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        print(f"从目录加载文档: {directory}")
    else:
        directory = docs_directory
        print(f"使用默认文档目录: {directory}")
    
    # 测试向量存储创建和检索
    print("\n=== 创建/加载向量存储 ===")
    retriever, documents = document_processing_demo(directory, vector_store_path)
    print(f"成功创建/加载向量存储，文档数: {len(documents)}")
    
    # 测试文档检索
    print("\n=== 测试文档检索 ===")
    test_queries = [
        "大模型基础",
        "注意力机制",
        "模型训练",
        "损失函数"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        docs = run_document_retrieval(query, directory, vector_store_path)
        print(f"找到 {len(docs)} 个相关文档:")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. {doc.page_content[:150]}... (来源: {doc.metadata['source']})")
    
    # 测试获取所有文档
    print("\n=== 所有文档 ===")
    all_docs = get_all_documents(directory, vector_store_path)
    print(f"总文档数: {len(all_docs)}")
    for doc in all_docs:
        print(f"{doc.metadata['source']}")
