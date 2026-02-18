from app.agents.base import BaseAgent
from app.prompts.domain.summarization_agent_prompt import (
    SUMMARIZATION_AGENT_SYSTEM_PROMPT,
)
from app.utils.logger import logger


class SummarizationAgent(BaseAgent):
    """
    Agent responsible for structured UI-friendly summarization.
    """

    def __init__(self):
        super().__init__(name="summarization_agent", role="Text Summarization Agent")
        self.system_prompt = SUMMARIZATION_AGENT_SYSTEM_PROMPT

    def summarize(self, text: str) -> str:
        """
        Generate structured summary output.
        """

        logger.info("[AGENT] summarization_agent invoked")

        return self.run(text)
