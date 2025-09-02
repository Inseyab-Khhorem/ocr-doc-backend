from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.supabase_client import supabase

router = APIRouter()

ADMIN_EMAIL = "khhorem.khan@raqmiyat.com"
ADMIN_PASSWORD = "@Inseyab123"

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(payload: AuthRequest):
    try:
        result = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })
        
        # Create profile
        if result.user:
            supabase.table("profiles").insert({
                "id": result.user.id,
                "email": payload.email
            }).execute()
        
        return {"status": "ok", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(payload: AuthRequest):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })
        return {"status": "ok", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/admin/login")
def admin_login(payload: AuthRequest):
    if payload.email != ADMIN_EMAIL or payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    return {
        "status": "ok", 
        "data": {
            "user": {"id": "admin", "email": ADMIN_EMAIL},
            "access_token": "admin_token",
            "is_admin": True
        }
    }