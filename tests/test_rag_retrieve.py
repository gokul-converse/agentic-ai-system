from app.rag.vectorstore import load_vectorstore

vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever(search_kwargs = {"k":3})

query = "What is the leave policy in my company?"

docs = retriever.invoke(query)

for i, doc in enumerate(docs):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content)

