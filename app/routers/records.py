from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.supabase_client import supabase

router = APIRouter()

@router.get("/records/{user_id}")
async def get_records(user_id: str):
    try:
        response = supabase.table("records").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        records = response.data or []

        # Ensure output_file_url is returned as JSON string
        for rec in records:
            if isinstance(rec.get("output_file_url"), dict):
                import json
                rec["output_file_url"] = json.dumps(rec["output_file_url"])

        return JSONResponse(content=records)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
