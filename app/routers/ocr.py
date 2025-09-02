from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import uuid, json
from app.services.supabase_client import supabase
from app.services.groq import groq_ocr_from_bytes
from app.utils.files import write_text_to_docx, write_text_to_pdf
from datetime import datetime

router = APIRouter()

@router.post("/convert")
async def convert_ocr(file: UploadFile, user_id: str = Form(...)):
    try:
        # Read file bytes
        file_bytes = await file.read()
        
        # Extract text using Groq OCR
        extracted_text = await groq_ocr_from_bytes(file_bytes, file.filename)
        
        # Generate DOCX and PDF files
        docx_id, docx_path = write_text_to_docx(extracted_text)
        pdf_id, pdf_path = write_text_to_pdf(extracted_text)
        
        # File URLs for serving
        docx_url = f"/files/{docx_path.name}"
        pdf_url = f"/files/{pdf_path.name}"
        
        # Insert record into Supabase
        record_id = str(uuid.uuid4())
        supabase.table("records").insert({
            "id": record_id,
            "user_id": user_id,
            "action": "OCR Conversion",
            "output_file_url_docx": docx_url,
            "output_file_url_pdf": pdf_url,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return {
            "text": extracted_text,
            "record_id": record_id,
            "files": {"docx": docx_url, "pdf": pdf_url}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))