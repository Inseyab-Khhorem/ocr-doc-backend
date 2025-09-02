from fastapi import APIRouter, UploadFile, Form, HTTPException, File as FastAPIFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from app.services.supabase_client import supabase
from app.services.groq import groq_generate_text, groq_ocr_from_bytes
from app.utils.files import write_text_to_docx, write_text_to_pdf
from datetime import datetime
from typing import Optional

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    user_id: str

@router.post("/generate")
async def generate_document(
    request: GenerateRequest = None,
    user_id: str = Form(None),
    prompt: str = Form(None),
    file: Optional[UploadFile] = FastAPIFile(None)
):
    try:
        # Handle both JSON and Form data
        if request:
            user_id = request.user_id
            prompt = request.prompt
        
        if not user_id or not prompt:
            raise HTTPException(status_code=400, detail="user_id and prompt required")
        
        # If file uploaded, extract text first
        context_text = ""
        if file:
            file_bytes = await file.read()
            context_text = await groq_ocr_from_bytes(file_bytes, file.filename)
            prompt = f"Context from uploaded document:\n{context_text}\n\nUser request: {prompt}"
        
        # Generate document using Groq
        generated_content = await groq_generate_text(prompt)
        
        # Create DOCX and PDF files
        docx_id, docx_path = write_text_to_docx(generated_content)
        pdf_id, pdf_path = write_text_to_pdf(generated_content)
        
        docx_url = f"/files/{docx_path.name}"
        pdf_url = f"/files/{pdf_path.name}"
        
        # Save to database
        record_id = str(uuid.uuid4())
        supabase.table("records").insert({
            "id": record_id,
            "user_id": user_id,
            "action": "Document Generation",
            "prompt": prompt,
            "output_file_url_docx": docx_url,
            "output_file_url_pdf": pdf_url,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return {
            "content": generated_content,
            "record_id": record_id,
            "files": {"docx": docx_url, "pdf": pdf_url}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))