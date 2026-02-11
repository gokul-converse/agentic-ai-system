# Loaders
from app.rag.loader import load_documents
from app.rag.chunker import chunk_documents

docs = load_documents()
chunks = chunk_documents(docs)

print("Docs:", len(docs))
print("Chunks:", len(chunks))
# print(chunks[0].page_content[:10])
