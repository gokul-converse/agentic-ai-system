import json
import re
from typing import Any, Dict, Optional

from pydantic import BaseModel

from app.agents.base import BaseAgent
from app.prompts.orchestrator_prompt import ORCHESTRATOR_SYSTEM_PROMPT
from app.utils.logger import logger


class OrchestratorResponse(BaseModel):
    type: str
    intent: Optional[str] = None
    reply: Optional[str] = None
    tool: Optional[str] = None
    text: Optional[Dict[str, Any]] = None


class OrchestratorAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="orchestrator_agent", role="System Orchestrator")
        self.system_prompt = ORCHESTRATOR_SYSTEM_PROMPT

    def _safe_json_parse(self, raw: str) -> dict:
        """
        Cleans and safely parse llm json output,
        Prevents crashes from gemini formatting issues.
        """

        if not raw or not raw.strip():
            raise ValueError("Empty LLM Response")

        raw = re.sub(r"```json", "", raw, flags=re.IGNORECASE)
        raw = re.sub(r"```", "", raw)
        raw = raw.strip()

        return json.loads(raw)

    def process(self, user_message: str) -> OrchestratorResponse:

        logger.info("[AGENT] orchestrator_agent invoked")

        response = self.run(user_message)
        # print("RAW LLM RESPONSE:", response)

        try:
            data = self._safe_json_parse(response)
            return OrchestratorResponse(**data)

        except Exception:
            logger.exception("[ORCHESTRATOR ERROR] Failed to parse LLM JSON response")

            # Safe fallback (prevents WS crash)
            return OrchestratorResponse(
                type="chat", reply="I had trouble understanding that. Please try again."
            )
