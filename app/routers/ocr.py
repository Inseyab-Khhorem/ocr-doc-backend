from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import json

router = APIRouter()

@router.post("/convert")
async def convert_file(file: UploadFile):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
            
        # Read file content
        content = await file.read()
        
        # For now, return mock data that matches your frontend expectations
        return {
            "success": True,
            "text": f"Mock extracted text from {file.filename}. File size: {len(content)} bytes",
            "files": {
                "docx": f"/files/mock_{file.filename}.docx",
                "pdf": f"/files/mock_{file.filename}.pdf"
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}