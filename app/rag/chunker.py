from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.logger import logger


def chunk_documents(documents):
    """
    Split loaded documents into smaller chunks for embeddings
    """
    logger.info(f"[RAG] Starting chunking. Input documents: {len(documents)}")

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)

        chunks = splitter.split_documents(documents)
        logger.info(f"[RAG] Chunking completed. Total chunks created: {len(chunks)}")
        return chunks
    except Exception:
        logger.exception("[RAG ERROR] Document chunking failed")
        raise
