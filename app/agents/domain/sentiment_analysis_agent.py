# from app.agents.base import BaseAgent
# from app.prompts.domain.knowledge_agent_prompt import KNOWLEDGE_AGENT_SYSTEM_PROMPT

# class KnowledgeAgent(BaseAgent):
#     """
#     Agent responsible for answering enterprise knowledge questions. This will later augmented with RAG.
#     """
#     def __init__(self):
#         super().__init__(name = 'knowledge_agent', role = "Knowledge Assistant")
#         self.system_prompt = KNOWLEDGE_AGENT_SYSTEM_PROMPT

from app.agents.base import BaseAgent
from app.prompts.domain.sentiment_agent_prompt import SENTIMENT_AGENT_SYSTEM_PROMPT
from app.utils.logger import logger


class SentimentAgent(BaseAgent):
    """Agent responsible for sentiment analysis with explainable output"""

    def __init__(self):
        super().__init__(name="sentiment_agent", role="Sentiment Analysis Agent")
        self.system_prompt = SENTIMENT_AGENT_SYSTEM_PROMPT

    def analyse(self, text: str) -> str:
        """
        Analyse the sentiment of the given text
        """

        logger.info("[AGENT] sentiment_agent invoked")
        return self.run(text)
