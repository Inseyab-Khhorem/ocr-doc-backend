from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def get_records():
    # Return mock records for now
    return {
        "success": True,
        "records": [
            {
                "id": "1",
                "file_name": "test.pdf",
                "created_at": "2024-09-02T10:00:00",
                "processing_type": "ocr"
            }
        ]
    }

@router.get("/admin/all")
async def get_all_records():
    return {
        "success": True, 
        "records": [
            {
                "id": "1",
                "user_id": "user1",
                "file_name": "admin_test.pdf",
                "created_at": "2024-09-02T10:00:00"
            }
        ]
    }