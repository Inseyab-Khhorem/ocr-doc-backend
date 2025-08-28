import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.groq import groq_ocr_from_bytes
from app.services.supabase_client import supabase
from app.utils.files import write_text_to_docx, write_text_to_pdf, save_bytes_to_file
from dotenv import load_dotenv

load_dotenv()
FILES_BASE_URL = os.getenv("FILES_BASE_URL", "http://localhost:8000/files")

router = APIRouter()

@router.post("/convert")
async def convert_ocr(file: UploadFile = File(...), user_id: str = Form(...)):
    # Read bytes
    content = await file.read()
    # Save original uploaded file (optional)
    original_id, original_path = save_bytes_to_file(content, suffix=f"_{file.filename}")
    try:
        extracted_text = await groq_ocr_from_bytes(content, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq OCR error: {e}")

    # Generate DOCX and PDF
    docx_id, docx_path = write_text_to_docx(extracted_text)
    pdf_id, pdf_path = write_text_to_pdf(extracted_text)

    # Build URLs (these are served by /files route)
    docx_url = f"{FILES_BASE_URL}/{docx_path.name}"
    pdf_url = f"{FILES_BASE_URL}/{pdf_path.name}"

    # Save record in Supabase
    record = {
        "id": docx_id,  # use docx_id as record id
        "user_id": user_id,
        "action_type": "OCR",
        "file_url": f"docx:{docx_url};pdf:{pdf_url}"
    }
    try:
        supabase.table("records").insert(record).execute()
    except Exception as e:
        # don't block success, but log/notify in real system
        print("Failed saving record to Supabase:", e)

    return {
        "text": extracted_text,
        "files": {"docx": docx_url, "pdf": pdf_url}
    }
