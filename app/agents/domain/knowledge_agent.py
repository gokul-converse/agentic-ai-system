import os
from typing import Dict, List

from app.agents.base import BaseAgent
from app.rag.vectorstore import load_vectorstore
from app.utils.logger import logger


class KnowledgeAgent(BaseAgent):

    FALLBACK_MESSAGE = "I do not find this information in the company documents."

    def __init__(self):
        super().__init__(name="knowledge_agent", role="Enterprise Knowledge Assistant")

        # Load vectorstore once
        self.vectorstore = load_vectorstore()

    def answer(self, user_input: str) -> dict:

        logger.info("[AGENT] knowledge_agent invoked")

        try:
            # Step 1: Retrieve Top 5 with scores
            results = self.vectorstore.similarity_search_with_score(user_input, k=5)

            logger.info("[RAG] --- Similarity Scores ---")

            # Step 2: Sort by score (lower = more similar)
            results = sorted(results, key=lambda x: x[1])

            # Step 3: Remove duplicates (same file + page)
            unique = {}
            for doc, score in results:
                source = doc.metadata.get("source")
                page = doc.metadata.get("page")

                key = (source, page)

                if key not in unique:
                    unique[key] = (doc, score)

            # Step 4: Take best 3 unique results
            top_results = list(unique.values())[:3]

            docs = []
            for doc, score in top_results:
                logger.info(
                    f"[RAG SCORE] {score:.4f} | "
                    f"{doc.metadata.get('source')} | "
                    f"page={doc.metadata.get('page')}"
                )
                docs.append(doc)

            logger.info(f"[RAG] Final selected documents: {len(docs)}")

            # Guard 1 — No documents retrieved from the vector DB - If docs is empty we do not call the llm , immediately fallback
            if not docs:
                logger.info("[RAG] Guard 1 triggered - No documents retrieved")
                return {"answer": self.FALLBACK_MESSAGE, "sources": []}

            # Step 5: Build context
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
            # return super().run(grounded_prompt)   #---> If we dont need to show the metadata source pages we can use this alone..
            answer = super().run(grounded_prompt)

            # Guard 2 — LLM fallback detection -  Retriever DID return some documents. llm was called, but still respond "I do not..."
            if self.FALLBACK_MESSAGE in answer:
                logger.info("[RAG] Guard 2 triggered - LLM fallback despite context")
                return {"answer": self.FALLBACK_MESSAGE, "sources": []}

            # Step 5: Build context
            sources = []

            for doc in docs:
                raw_path = doc.metadata.get("source", "")
                file_name = os.path.basename(raw_path)
                page = doc.metadata.get("page", "N/A")

                # Public URL (served via FastAPI static mount)
                url = f"/docs-files/{file_name}"

                if page != "N/A":
                    url = f"{url}#page={page}"

                sources.append({"file_name": file_name, "page": page, "url": url})

            return {"answer": answer, "sources": sources}

        except Exception:
            logger.exception("[RAG ERROR] KnowledgeAgent failed")
            raise

    def _build_context(self, docs: List) -> str:
        """
        Combines retrieved document chunks into single context string
        """

        context_parts = []

        for i, doc in enumerate(docs):
            context_parts.append(f"[Source {i+1}]\n{doc.page_content}")

        return "\n\n".join(context_parts)
