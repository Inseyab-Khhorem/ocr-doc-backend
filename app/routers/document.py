from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.groq import groq_generate_text
from app.utils.files import write_text_to_docx, write_text_to_pdf
from app.services.supabase_client import supabase
from dotenv import load_dotenv
import os

load_dotenv()
FILES_BASE_URL = os.getenv("FILES_BASE_URL", "http://localhost:8000/files")

router = APIRouter()

class GenerateRequest(BaseModel):
    user_id: str
    prompt: str

@router.post("/generate")
async def generate_document(payload: GenerateRequest):
    try:
        generated_text = await groq_generate_text(payload.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq generation error: {e}")

    docx_id, docx_path = write_text_to_docx(generated_text)
    pdf_id, pdf_path = write_text_to_pdf(generated_text)

    docx_url = f"{FILES_BASE_URL}/{docx_path.name}"
    pdf_url = f"{FILES_BASE_URL}/{pdf_path.name}"

    record = {
        "id": docx_id,
        "user_id": payload.user_id,
        "action_type": "Generation",
        "file_url": f"docx:{docx_url};pdf:{pdf_url}"
    }
    try:
        supabase.table("records").insert(record).execute()
    except Exception as e:
        print("Failed saving document record to Supabase:", e)

    return {
        "document": generated_text,
        "files": {"docx": docx_url, "pdf": pdf_url}
    }
