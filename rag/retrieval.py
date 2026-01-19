"""
Retrieval module: vectorstore search and LLM synthesis using LangChain.
"""
from typing import List, Dict, Optional


def get_retriever(vectorstore, k: int = 4, search_type: str = "similarity"):
    """Create a retriever from the vectorstore.
    
    Args:
        vectorstore: Chroma vectorstore instance.
        k: Number of documents to retrieve.
        search_type: Type of search ('similarity' or 'mmr').
    Returns:
        LangChain retriever.
    """
    return vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k}
    )


def retrieve_documents(retriever, query: str) -> List[Dict]:
    """Retrieve relevant documents for a query.
    
    Args:
        retriever: LangChain retriever.
        query: Question or query.
    
    Returns:
        List of dicts with 'content' and 'metadata'.
    """
    docs = retriever.invoke(query)
    
    results = []
    for doc in docs:
        results.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
        })
    
    return results


def create_rag_chain(retriever, llm, system_prompt: Optional[str] = None):
    """Create a complete RAG chain with LangChain.
    
    Args:
        retriever: Configured retriever.
        llm: Language model (ChatGroq, ChatOpenAI, etc.).
        system_prompt: Custom system prompt.
    
    Returns:
        RAG chain ready to invoke.
    """
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
    
    if system_prompt is None:
        system_prompt = """You are an expert assistant in science communication. 
Use the provided context to answer questions clearly and accessibly.
If you don't find relevant information in the context, say so honestly.
Cite sources when possible."""
    
    template = f"""{system_prompt}

Context:
{{context}}

Question: {{question}}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join([
            f"[Source: {doc.metadata.get('filename', 'unknown')}]\n{doc.page_content}"
            for doc in docs
        ])
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


def query_rag(
    query: str,
    vectorstore=None,
    retriever=None,
    llm=None,
    k: int = 4,
    system_prompt: Optional[str] = None,
) -> Dict:
    """Query the RAG system and return response + evidence.
    
    Args:
        query: User question.
        vectorstore: Chroma vectorstore (optional if retriever is provided).
        retriever: Already configured retriever (optional if vectorstore is provided).
        llm: Language model for synthesis (optional).
        k: Number of documents to retrieve.
        system_prompt: Custom system prompt.
    
    Returns:
        Dict with keys: 'answer' (if LLM provided), 'sources' (retrieved documents).
    """
    # Configure retriever
    if retriever is None:
        if vectorstore is None:
            raise ValueError("You must provide vectorstore or retriever")
        retriever = get_retriever(vectorstore, k=k)
    
    # Retrieve documents
    sources = retrieve_documents(retriever, query)
    
    result = {"sources": sources}
    
    # Si hay LLM, generar respuesta
    if llm is not None:
        chain = create_rag_chain(retriever, llm, system_prompt)
        answer = chain.invoke(query)
        result["answer"] = answer
    
    return result
