"""
RAG Retrieval Module

Retrieves relevant document chunks from the vector database
for a given user query.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


VECTOR_DB_DIR = "chroma"


def retrieve_context(query: str, k: int = 3) -> str:
    """
    Retrieves top-k relevant document chunks.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )

    results = vectorstore.similarity_search(query, k=k)

    context = "\n\n".join(doc.page_content for doc in results)
    return context