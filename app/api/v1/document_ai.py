import os
import uuid
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.agents.domain.document_extraction_agent import InvoiceExtractionAgent
from app.utils.logger import logger

router = APIRouter(prefix="/documents", tags=["Document AI"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

agent = InvoiceExtractionAgent()


@router.post("/extract-invoice")
async def extract_invoice(file: UploadFile = File(...)):

    logger.info("[API] /documents/extract-invoice called")

    filename = file.filename.lower()

    if not filename.endswith((".pdf", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only PDF or image files supported")

    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        # Save file temporarily
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call agent (agent handles extraction + LLM)
        result = agent.extract(temp_path)

        return result

    except Exception as e:
        logger.exception("[API ERROR] Invoice extraction failed")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
