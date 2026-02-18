# Loaders python -m app.rag.ingest

from app.rag.loader import load_documents
from app.rag.chunker import chunk_documents
from app.rag.vectorstore import build_vectorstore

docs = load_documents()
chunks = chunk_documents(docs)

print("Docs:", len(docs))
print("Chunks:", len(chunks))
vectorstore = build_vectorstore(chunks)
# print(chunks[0].page_content[:10])
