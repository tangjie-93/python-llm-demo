"""
LangChain 文档处理示例
包含：Document、Text Splitters、Embeddings、Vector Stores、Retrievers
"""
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def document_processing_demo():
    """文档处理示例"""
    # 创建示例文档
    documents = [
        Document(page_content="LangChain 是一个用于构建 LLM 应用的框架，它提供了一套工具和接口，使开发者能够更轻松地构建复杂的 LLM 应用。", metadata={"source": "doc1"}),
        Document(page_content="LangChain 支持多种模型和工具集成，包括 OpenAI、DeepSeek、Google 等模型，以及各种外部工具和服务。", metadata={"source": "doc2"}),
        Document(page_content="LangChain 的核心概念包括 Chains、Agents、Memory、Retrievers 等，这些组件可以组合使用，构建强大的应用。", metadata={"source": "doc3"}),
        Document(page_content="LangChain 的文档处理能力非常强大，支持各种文档格式，如 PDF、Word、Markdown 等。", metadata={"source": "doc4"}),
        Document(page_content="LangChain 的向量存储支持多种后端，如 Chroma、FAISS、Pinecone 等，可以根据需要选择合适的存储方案。", metadata={"source": "doc5"})
    ]
    
    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    splits = text_splitter.split_documents(documents)
    
    # 嵌入
    embeddings = FakeEmbeddings(size=100)
    
    # 向量存储
    vector_store = InMemoryVectorStore.from_documents(splits, embeddings)
    
    # 检索器
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    return retriever, documents

def run_document_retrieval(query):
    """运行文档检索"""
    retriever, _ = document_processing_demo()
    docs = retriever.invoke(query)
    return docs

def get_all_documents():
    """获取所有文档"""
    _, documents = document_processing_demo()
    return documents

if __name__ == "__main__":
    # 测试文档检索
    docs = run_document_retrieval("LangChain 的核心概念")
    print("检索结果:")
    for doc in docs:
        print(f"{doc.page_content} (来源: {doc.metadata['source']})")
    
    # 测试获取所有文档
    all_docs = get_all_documents()
    print("\n所有文档:")
    for doc in all_docs:
        print(f"{doc.page_content} (来源: {doc.metadata['source']})")
