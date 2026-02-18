import os

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader

from app.utils.logger import logger

DOCUMENTS_PATH = "data/documents"


def _get_loader(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return PyPDFLoader(file_path)

    elif ext == ".txt":
        try:
            return TextLoader(file_path, encoding="utf-8")
        except Exception:
            logger.warning(f"[RAG] UTF-8 failed, retrying with latin-1: {file_path}")
            return TextLoader(file_path, encoding="latin-1")

    elif ext == ".docx":
        return Docx2txtLoader(file_path)

    else:
        return None


def load_documents():
    """
    Load all the PDF, TXT, DOCX from the folder, returns a list of langchain document object
    """

    if not os.path.exists(DOCUMENTS_PATH):
        logger.error(f"[RAG] Documents folder not found: {DOCUMENTS_PATH}")
        raise FileNotFoundError(f"Document folder not found:{DOCUMENTS_PATH}")

    documents = []

    files = os.listdir(DOCUMENTS_PATH)

    logger.info(f"[Rag] found {len(files)} for ingestion")

    for i in files:
        file_path = os.path.join(DOCUMENTS_PATH, i)

        loader = _get_loader(file_path)

        if loader is None:
            logger.warning(f"[RAG] Skipping unsupported file type: {i}")
            continue

        try:
            logger.info(f"[RAG] Loading document: {i}")

            docs = loader.load()

            documents.extend(docs)

        except Exception:
            logger.exception(f"[RAG ERROR] Failed loading document: {i}")
            raise

    logger.info(f"[RAG] Total pages loaded: {len(documents)}")

    return documents
