from langchain_community.embeddings import HuggingFaceEmbeddings
from app.utils.logger import logger

def get_embedding_model():
    """
    Returns embedding model.
    Free local model using SentenceTransformers.
    """
    try:
        logger.info("[RAG] Loading embedding model: all-MiniLM-L6-v2")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        logger.info("[RAG] Embedding model loaded successfully")

        return embeddings
    
    except Exception:
        logger.exception("[RAG ERROR] Failed to load embedding model")
        raise