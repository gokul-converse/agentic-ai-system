from typing import List, Dict
from app.agents.base import BaseAgent
from app.rag.vectorstore import load_vectorstore
from app.utils.logger import logger
import os

class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name = "knowledge_agent", role = "Enterprise Knowledge Assistant")

        # Load vectorstore once
        self.vectorstore = load_vectorstore()
        self.retriever = self.vectorstore.as_retriever(search_kwargs = {"k":3})

    def answer(self, user_input: str) -> dict:

        logger.info("[AGENT] knowledge_agent invoked")

        try:
            docs = self.retriever.invoke(user_input)
            logger.info(f"[RAG] Retrieved {len(docs)} documents")

            context = self._build_context(docs)

            grounded_prompt = f"""
    Use ONLY the context below to answer the question.
    If the answer is not found in the context, say:
    "I do not find this information in the company documents."

    CONTEXT:
    {context}

    QUESTION:
    {user_input}
    """
            #return super().run(grounded_prompt)   #---> If we dont need to show the metadata source pages we can use this alone..
            answer = super().run(grounded_prompt)

            # sources = [
            #     {
            #         "source": doc.metadata.get("source", "unknown"),
            #         "page": doc.metadata.get("page", "N/A")
            #     }
            #     for doc in docs
            # ]

            # return {
            #     "answer": answer,
            #     "sources": sources
            # }

            sources = []

            for doc in docs:
                raw_path = doc.metadata.get("source", "")
                file_name = os.path.basename(raw_path)
                page = doc.metadata.get("page", "N/A")

                # Public URL (served via FastAPI static mount)
                url = f"/docs-files/{file_name}"

                if page != "N/A":
                    url = f"{url}#page={page}"

                sources.append({
                    "file_name": file_name,
                    "page": page,
                    "url": url
                })

            return {
                "answer": answer,
                "sources": sources
            }

        except Exception:
            logger.exception("[RAG ERROR] KnowledgeAgent failed")
            raise


    def _build_context(self, docs:List) ->str:
        """
        Combines retrieved document chunks into single context string
        """

        context_parts = []

        for i, doc in enumerate(docs):
            context_parts.append(f"[Source {i+1}]\n{doc.page_content}")

        return "\n\n".join(context_parts)
