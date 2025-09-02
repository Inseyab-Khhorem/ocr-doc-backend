from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.supabase_client import supabase
import json

router = APIRouter()
security = HTTPBearer()

# Admin credentials
ADMIN_EMAIL = "khhorem.khan@raqmiyat.com"
ADMIN_PASSWORD = "@Inseyab123"

def verify_admin(token: str) -> bool:
    """Check if token belongs to admin user"""
    try:
        user = supabase.auth.get_user(token)
        return user.user.email == ADMIN_EMAIL
    except:
        return False

def get_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract user_id from JWT token"""
    try:
        user = supabase.auth.get_user(credentials.credentials)
        return user.user.id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/")
async def get_user_records(user_id: str = Depends(get_user_from_token)):
    """Get records for authenticated user"""
    try:
        response = supabase.table("records").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        records = response.data or []
        
        # Format output_file_url for frontend compatibility
        for rec in records:
            docx = rec.get("output_file_url_docx")
            pdf = rec.get("output_file_url_pdf")
            rec["output_file_url"] = json.dumps({"docx": docx, "pdf": pdf})
        
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/all")
async def get_all_records(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Admin only: Get all records from all users"""
    if not verify_admin(credentials.credentials):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        response = supabase.table("records").select("*").order("created_at", desc=True).execute()
        records = response.data or []
        
        for rec in records:
            docx = rec.get("output_file_url_docx")
            pdf = rec.get("output_file_url_pdf")
            rec["output_file_url"] = json.dumps({"docx": docx, "pdf": pdf})
        
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/admin/record/{record_id}")
async def delete_record(record_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Admin only: Delete a specific record"""
    if not verify_admin(credentials.credentials):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        supabase.table("records").delete().eq("id", record_id).execute()
        return {"message": "Record deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/admin/user/{user_id}")
async def delete_user(user_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Admin only: Delete user and all their records"""
    if not verify_admin(credentials.credentials):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Delete user records first (cascade should handle this, but explicit is better)
        supabase.table("records").delete().eq("user_id", user_id).execute()
        # Note: Can't delete auth.users via client, only via admin API
        return {"message": "User records deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))