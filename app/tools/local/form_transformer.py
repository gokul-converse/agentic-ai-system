import json
import os
from typing import Any, Dict

from app.prompts.tools.form_transformer_prompt import FORM_TRANSFORM_SYSTEM_PROMPT
from app.services.llm_factory import get_llm
from app.utils.logger import logger


class FormTransformer:

    def __init__(self):
        self.llm = get_llm()
        self.provider = os.getenv("LLM_PROVIDER", "azure")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    def _build_azure_messages(self, form_json: dict):
        return [
            {"role": "system", "content": FORM_TRANSFORM_SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(form_json)},
        ]

    def _build_gemini_prompt(self, form_json: dict) -> str:
        return f"""
{FORM_TRANSFORM_SYSTEM_PROMPT}

INPUT JSON:
{json.dumps(form_json)}
""".strip()

    # ------------------------------------------------

    def transform(self, form_json: Dict[str, Any]) -> Dict[str, Any]:

        logger.info("[TOOL] FormTransformer invoked")

        try:

            # -------- Azure --------
            if self.provider == "azure":

                messages = self._build_azure_messages(form_json)

                response = self.llm.chat.completions.create(
                    model=self.deployment,
                    messages=messages,
                    temperature=0.0,
                    max_tokens=4000,
                )

                content = response.choices[0].message.content.strip()

            # -------- Gemini --------
            elif self.provider == "gemini":

                model_name = os.getenv("GEMINI_MODEL")

                prompt = self._build_gemini_prompt(form_json)

                response = self.llm.models.generate_content(
                    model=model_name, contents=prompt
                )

                content = response.text.strip()

            else:
                raise ValueError(f"Unsupported provider {self.provider}")

            logger.info("[TOOL] FormTransformer LLM response received")

            return self._clean_json(content)

        except Exception:
            logger.exception("[TOOL ERROR] FormTransformer failed")
            raise

    # ------------------------------------------------

    def _clean_json(self, content: str) -> Dict[str, Any]:

        if not content:
            raise ValueError("Empty LLM response")

        content = content.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(content)
        except Exception:
            logger.exception("[TOOL ERROR] Invalid JSON from FormTransformer")
            raise
