# from app.services.llm_factory import get_llm
# from app.prompts.base_prompt import SYSTEM_BASE_PROMPT
# import os
# from typing import Optional

# class BaseAgent:
#     """
#     Base class for all agents in the system, Every agent must inherit from this.
#     """

#     def __init__(self, name:str, role: Optional[str] = None):
#         self.name = name
#         self.role = role or "Generic Ai Agent"

#         self.llm = get_llm()

#         self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

#         self.system_prompt = SYSTEM_BASE_PROMPT.strip()

#     def _build_message(self, user_input:str):
#         """
#         Constructs the message payload for the llm,
#         Centralized so behaviour stays consisten.
#         """
#         return [
#             {
#                 "role": "system",
#                 "content": self.system_prompt.strip()
#             },
#             {
#                 "role": "user",
#                 "content": user_input.strip()
#             }
#         ]
    
#     def call_llm(self, messages):
#         """
#         Low level llm call, Agents should not override this unless absolutely required.
#         """
#         response = self.llm.chat.completions.create(
#             model = self.deployment,
#             messages=messages,
#             temperature=0.2,
#             max_tokens=5000
#         )

#         return response.choices[0].message.content.strip()
    
#     def run(self, user_input:str) -> str:
#         """
#         Standard entrypoint for all agents. this is what orchestrators and appi will call.
#         """

#         messages = self._build_message(user_input)

#         return self.call_llm(messages)




from app.services.llm_factory import get_llm
from app.prompts.base_prompt import SYSTEM_BASE_PROMPT
import os
from typing import Optional
from app.utils.logger import logger

class BaseAgent:
    """
    Base class for all agents in the system.
    Every agent must inherit from this.
    """

    def __init__(self, name: str, role: Optional[str] = None):
        self.name = name
        self.role = role or "Generic AI Agent"

        self.llm = get_llm()
        self.provider = os.getenv("LLM_PROVIDER", "azure")

        # Azure-specific
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        # Shared
        self.system_prompt = SYSTEM_BASE_PROMPT.strip()

    # -------------------------
    # Prompt builders
    # -------------------------

    def _build_azure_messages(self, user_input: str):
        """
        Azure OpenAI uses role-based chat messages.
        """
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input.strip()}
        ]

    def _build_gemini_prompt(self, user_input: str) -> str:
        """
        Gemini does NOT support role-based messages.
        We merge system + user into a single prompt.
        """
        return f"""
{self.system_prompt}

User input:
{user_input.strip()}
""".strip()

    # -------------------------
    # Core LLM call
    # -------------------------

    def call_llm(self, user_input: str) -> str:
        """
        Low-level LLM call.
        This is the ONLY place provider-specific logic is allowed.
        """

        # -------- Azure OpenAI --------
        if self.provider == "azure":
            logger.info(f"[LLM CALL] provider=azure | deployment={self.deployment} | agent={self.name}")

            try:
                messages = self._build_azure_messages(user_input)

                response = self.llm.chat.completions.create(
                    model=self.deployment,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=5000
                )

                return response.choices[0].message.content.strip()
            
            except Exception as e:
                logger.exception(f"[LLM ERROR] provider=azure | deployment={self.deployment} | agent={self.name}")
                raise

        # -------- Gemini (google-genai) --------
        elif self.provider == "gemini":
            model_name = os.getenv("GEMINI_MODEL")

            logger.info(f"[LLM CALL] provider=gemini | model={model_name} | agent={self.name}")

            try:
                prompt = self._build_gemini_prompt(user_input)

                response = self.llm.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )

                return response.text.strip()
            
            except Exception as e:
                logger.exception(f"[LLM ERROR] provider=gemini | model={model_name} | agent={self.name}")
                raise

        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {self.provider}")

    # -------------------------
    # Public entrypoint
    # -------------------------

    def run(self, user_input: str) -> str:
        """
        Standard entrypoint for all agents.
        Orchestrators and APIs should ONLY call this.
        """
        return self.call_llm(user_input)





"""
This file is responsible for:

Talking to any LLM

Handling provider differences

Logging LLM calls

Providing a single execution interface

This file is NOT responsible for:

Deciding which agent to use ❌

RAG ❌

Validation ❌

API ❌
"""