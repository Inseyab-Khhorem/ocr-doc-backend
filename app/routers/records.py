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
    return [
        {
            "id": "1",
            "user_id": "user123",
            "action": "OCR Conversion",
            "created_at": "2024-09-02T10:00:00Z",
            "prompt": "Convert this document",
            "output_file_url": '{"docx": "https://example.com/file.docx", "pdf": "https://example.com/file.pdf"}'
        },
        {
            "id": "2",
            "user_id": "user456",
            "action": "Document Generation",
            "created_at": "2024-09-01T15:30:00Z",
            "prompt": "Generate a report",
            "output_file_url": '{"docx": "https://example.com/report.docx"}'
        }
    ]

@router.delete("/admin/record/{record_id}")
async def delete_record(record_id: str):
    # Mock delete - in real app, delete from database
    return {"success": True}
