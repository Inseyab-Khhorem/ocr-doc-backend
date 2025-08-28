from fastapi import APIRouter, HTTPException, Query
from app.services.supabase_client import supabase

router = APIRouter()

@router.get("/list")
def list_records(user_id: str = Query(..., description="User ID to fetch records for")):
    try:
        res = supabase.table("records").select("*").eq("user_id", user_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"data": res.data}
