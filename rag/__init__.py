"""
RAG Package: modular pipeline for Retrieval-Augmented Generation.

Modules:
- ingestion: load and split documents (PDF, TXT)
- database: create and manage Chroma vectorstore
- retrieval: search and LLM synthesis

Usage:
    from rag.ingestion import load_documents, ingest_documents
    from rag.database import ingest_to_vectorstore, load_vectorstore
    from rag.retrieval import query_rag, get_retriever
"""
