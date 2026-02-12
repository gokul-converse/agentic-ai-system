import os
from langchain_community.vectorstores import Chroma
from app.rag.embeddings import get_embedding_model
from app.utils.logger import logger

PERSIST_DIR = "data/vectorstore"

def build_vectorstore(chunks):
    """
    Build and persit Chroma vector store from chunks.
    """

    try:
        logger.info("[RAG] Building Chroma vector store")

        embeddings = get_embedding_model()

        vectorstore = Chroma.from_documents(
            documents= chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )

        vectorstore.persist()

        logger.info("[RAG] Vector store created and persisted")

        return vectorstore
    
    except Exception:
        logger.exception("[RAG ERROR] Failed to build vector store")
        raise

def load_vectorstore():
    """
    Load existing persisted vector store.
    """

    try:
        logger.info("[RAG] Loading existing vector store")

        embeddings = get_embedding_model()

        vector_store = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings
        )

        logger.info("[RAG] Vector store loaded successfully")

        return vector_store
    
    except Exception:
        logger.exception("[RAG ERROR] Failed to load vector store")
        raise