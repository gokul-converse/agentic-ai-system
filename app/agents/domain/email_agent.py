from app.agents.base import BaseAgent
from app.mcp.registry import TOOL_REGISTRY
from app.utils.logger import logger
import json

class EmailAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="email_agent",
            role="Handles email generation and structured extraction"
        )

    def generate_email(self, user_input: str) -> dict:
        """
        Phase 1:
        - Use tool schema
        - Let LLM extract recipient, subject, body
        - Return structured data for UI confirmation
        """

        logger.info("[AGENT] email_agent invoked")

        try:
            schema = TOOL_REGISTRY["send_email"]

            message = self.call_llm_with_tools(
                user_input=user_input,
                tools=[schema]
            )

            # Azure returns tool_calls inside message
            if hasattr(message, "tool_calls") and message.tool_calls:

                tool_call = message.tool_calls[0]

                # without this our model is returning string not json object so we are doing this
                raw_arguments = tool_call.function.arguments

                # Azure returns arguments as JSON string
                if isinstance(raw_arguments, str):
                    arguments = json.loads(raw_arguments)
                else:
                    arguments = raw_arguments

                return {
                    "type": "confirm_email",
                    "data": arguments
                }

            # If no tool call returned
            return {
                "type": "error",
                "message": "LLM did not return structured email data."
            }

        except Exception:
            logger.exception("[EMAIL AGENT ERROR]")
            raise
