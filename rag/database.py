"""
Vector database module: creates and manages Chroma vectorstore with LangChain.
"""
from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document


def get_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """Returns the configured embeddings model.
    Args:
        model_name: Name of the sentence-transformers model.
    Returns:
        HuggingFaceEmbeddings instance.
    """
    from langchain_huggingface import HuggingFaceEmbeddings
    
    return HuggingFaceEmbeddings(model_name=model_name)


def create_vectorstore(
    documents: List[Document],
    persist_directory: str = "chroma_db",
    collection_name: str = "papers",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> object:
    """Create a Chroma vectorstore from LangChain Documents.
    
    Args:
        documents: List of Documents (already split into chunks).
        persist_directory: Directory to persist the database.
        collection_name: Name of the collection in Chroma.
        embedding_model: Embedding model to use.
    
    Returns:
        Chroma vectorstore instance.
    """
    from langchain_community.vectorstores import Chroma
    
    embeddings = get_embeddings(embedding_model)
    
    persist_path = Path(persist_directory)
    persist_path.mkdir(parents=True, exist_ok=True)
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(persist_path),
        collection_name=collection_name,
    )
    
    return vectorstore


def load_vectorstore(
    persist_directory: str = "chroma_db",
    collection_name: str = "papers",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> object:
    """Load an existing Chroma vectorstore.
    
    Args:
        persist_directory: Directory where the database is stored.
        collection_name: Name of the collection.
        embedding_model: Embedding model (must match the one used during creation).
    
    Returns:
        Chroma vectorstore instance.
    """
    from langchain_community.vectorstores import Chroma
    
    embeddings = get_embeddings(embedding_model)
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        collection_name=collection_name,
        embedding_function=embeddings,
    )
    return vectorstore


def ingest_to_vectorstore(
    source_path: str,
    persist_directory: str = "chroma_db",
    collection_name: str = "papers",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> object:
    """Complete pipeline: load documents, split into chunks, and save to vectorstore.
    
    Args:
        source_path: Path to file, directory, or glob pattern (e.g., 'data/raw').
        persist_directory: Directory to persist Chroma.
        collection_name: Name of the collection.
        embedding_model: Embedding model.
        chunk_size: Size of each chunk.
        chunk_overlap: Overlap between chunks.
    
    Returns:
        Chroma vectorstore instance with indexed documents.
    """
    from .ingestion import ingest_documents
    
    # 1. Load and split documents
    chunks = ingest_documents(source_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    # 2. Create vectorstore
    vectorstore = create_vectorstore(
        documents=chunks,
        persist_directory=persist_directory,
        collection_name=collection_name,
        embedding_model=embedding_model,
    )
    
    print(f"Indexed {len(chunks)} chunks in '{persist_directory}' (collection: {collection_name})")
    return vectorstore
