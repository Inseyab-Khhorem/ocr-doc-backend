from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from app.supabase_client import supabase
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/document/generate")
async def generate_document(user_id: str = Form(...), prompt: str = Form(...)):
    try:
        file_id = str(uuid.uuid4())

        # Simulated generated document
        docx_url = f"/static/{file_id}.docx"
        pdf_url = f"/static/{file_id}.pdf"

        # Save record to Supabase
        supabase.table("records").insert({
            "id": file_id,
            "user_id": user_id,
            "action": "Document Generation",
            "prompt": prompt,
            "output_file_url": {
                "docx": docx_url,
                "pdf": pdf_url
            },
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return JSONResponse(content={
            "message": "Document generated",
            "file_id": file_id,
            "docx_url": docx_url,
            "pdf_url": pdf_url
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
