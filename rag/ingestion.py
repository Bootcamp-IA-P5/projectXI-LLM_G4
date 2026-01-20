"""
Ingestion module: loads documents (PDF, TXT) and splits them into chunks using LangChain.
"""
from pathlib import Path
from typing import List, Optional
import glob

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(source_path: str) -> List[Document]:
    """Load PDF and TXT documents from a file, directory, or glob pattern.
    
    Args:
        source_path: Path to a file, directory, or pattern (e.g., 'data/raw/*.pdf')
    
    Returns:
        List of LangChain Documents with content and metadata.
    """
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    
    p = Path(source_path)
    documents: List[Document] = []
    
    # Case 1: Directory - load all PDF and TXT files
    if p.is_dir():
        pdf_files = list(p.glob("*.pdf"))
        txt_files = list(p.glob("*.txt"))
        all_files = pdf_files + txt_files
        
        if not all_files:
            raise FileNotFoundError(f"No PDF or TXT files found in: {source_path}")
        
        for file_path in all_files:
            docs = _load_single_file(str(file_path))
            documents.extend(docs)
        return documents
    
    # Case 2: Glob pattern (e.g., data/raw/*.pdf)
    if "*" in source_path:
        matched_files = glob.glob(source_path)
        if not matched_files:
            raise FileNotFoundError(f"No files found matching pattern: {source_path}")
        
        for file_path in matched_files:
            docs = _load_single_file(file_path)
            documents.extend(docs)
        return documents
    
    # Case 3: Single file
    if not p.exists():
        raise FileNotFoundError(f"File not found: {source_path}")
    
    return _load_single_file(source_path)


def _load_single_file(file_path: str) -> List[Document]:
    """Load a single file (PDF or TXT) and return a list of Documents."""
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    
    p = Path(file_path)
    suffix = p.suffix.lower()
    
    if suffix == ".pdf":
        loader = PyPDFLoader(str(p))
    elif suffix == ".txt":
        loader = TextLoader(str(p), encoding="utf-8")
    else:
        raise ValueError(f"Unsupported format: {suffix}. Use PDF or TXT.")
    
    docs = loader.load()
    
    # Add additional metadata
    for doc in docs:
        doc.metadata["filename"] = p.name
        doc.metadata["source"] = str(p)
    
    return docs


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: Optional[List[str]] = None,
) -> List[Document]:
    """Split documents into chunks using LangChain's RecursiveCharacterTextSplitter.
    
    Args:
        documents: List of LangChain Documents.
        chunk_size: Maximum size of each chunk (characters).
        chunk_overlap: Overlap between chunks (characters).
        separators: List of separators for splitting (default: paragraphs, lines, spaces).
    
    Returns:
        List of Documents split into chunks with preserved metadata.
    """
    if separators is None:
        separators = ["\n\n", "\n", ". ", " ", ""]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add chunk index to metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
    
    return chunks


def ingest_documents(
    source_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """Complete pipeline: load documents and split them into chunks.
    
    Args:
        source_path: Path to file, directory, or glob pattern.
        chunk_size: Chunk size.
        chunk_overlap: Overlap between chunks.
    
    Returns:
        Lista de Documents listos para vectorizar.
    """
    documents = load_documents(source_path)
    chunks = split_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunks
