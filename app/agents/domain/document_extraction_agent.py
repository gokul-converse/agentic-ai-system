import json
import re
import os

from app.agents.base import BaseAgent
from app.prompts.domain.extraction_agent_prompt import EXTRACTION_AGENT_SYSTEM_PROMPT
from app.tools.local.pdf_text_extractor import extract_text_from_pdf
from app.tools.local.ocr_extractor import extract_text_with_ocr
from app.tools.local.image_ocr_extractor import extract_text_from_image
from app.utils.logger import logger


class InvoiceExtractionAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="invoice_extraction_agent", role="Invoice Extraction Agent")
        self.system_prompt = EXTRACTION_AGENT_SYSTEM_PROMPT

    def extract(self, file_path: str) -> dict:

        logger.info("[AGENT] invoice_extraction_agent invoked")

        document_text = self._extract_text(file_path)

        response = self.run(document_text)

        return self._clean_llm_json(response)

    def _extract_text(self, file_path: str) -> str:

        ext = os.path.splitext(file_path)[1].lower()

        logger.info(f"[TOOLS] Extracting text from file type={ext}")

        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)

            # If no real text found → fallback to OCR
            if not text or len(text.strip()) < 20:
                logger.info("[OCR FALLBACK] No text layer detected, using OCR")
                text = extract_text_with_ocr(file_path)

            return text

        elif ext in [".png", ".jpg", ".jpeg"]:
            return extract_text_from_image(file_path)

        else:
            logger.warning("Unsupported file type, trying OCR fallback")
            return extract_text_with_ocr(file_path)

    def _clean_llm_json(self, content: str) -> dict:

        if not content or not content.strip():
            raise ValueError("LLM returned empty response")

        content = re.sub(r"```json", "", content, flags=re.IGNORECASE)
        content = re.sub(r"```", "", content)
        content = content.strip()

        return json.loads(content)