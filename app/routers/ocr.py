from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil, os, uuid
from app.services.supabase_client import supabase
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ocr/convert")
async def convert_ocr(file: UploadFile, user_id: str = Form(...)):
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Simulated conversion (in real case, run OCR + generate DOCX/PDF)
        docx_url = f"/static/{file_id}.docx"
        pdf_url = f"/static/{file_id}.pdf"

        # Insert record into Supabase
        supabase.table("records").insert({
            "id": file_id,
            "user_id": user_id,
            "action": "OCR Conversion",
            "output_file_url": {
                "docx": docx_url,
                "pdf": pdf_url
            },
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return JSONResponse(content={
            "message": "OCR conversion successful",
            "file_id": file_id,
            "docx_url": docx_url,
            "pdf_url": pdf_url
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
