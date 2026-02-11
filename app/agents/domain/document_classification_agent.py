from app.agents.base import BaseAgent
from app.prompts.domain.classification_agent_prompt import CLASSIFICATION_AGENT_SYSTEM_PROMPT
from app.utils.logger import logger


class ClassificationAgent(BaseAgent):
    """
    Agent responsible for classifying user text into predefined categories.
    """

    def __init__(self):
        super().__init__(name="classification_agent", role="Text Classification Agent")
        self.system_prompt = CLASSIFICATION_AGENT_SYSTEM_PROMPT

    def classify(self, text: str) -> str:
        """
        Classify given text and return formatted result.
        """

        logger.info(f"[AGENT] classification_agent invoked")

        return self.run(text)
