"""
RAG Ingestion Script

Loads domain documents, chunks them, generates embeddings,
and stores them in a Chroma vector database.
"""

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DATA_DIR = "data"
VECTOR_DB_DIR = "chroma"


def ingest_documents():
    # 1. Load documents
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8"
        }
    )
    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    # 2. Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    print(f"Split into {len(chunks)} chunks")

    # 3. Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Store in Chroma vector DB
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    print("✅ Vector database created and persisted")


if __name__ == "__main__":
    ingest_documents()
