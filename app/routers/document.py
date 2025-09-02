from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/generate")
async def generate_document(
    prompt: str = Form(...),
    output_format: str = Form("docx"),
    file: UploadFile = File(None)
):
    try:
        # Mock response for now
        response_text = f"Generated document based on: {prompt[:100]}..."
        
        if file:
            response_text += f" (with context from {file.filename})"
            
        return {
            "success": True,
            "content": response_text,
            "download_url": f"/download/generated.{output_format}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}