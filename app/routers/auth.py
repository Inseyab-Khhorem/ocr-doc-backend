from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.supabase_client import supabase

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(payload: SignupRequest):
    try:
        result = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })
        return {"status": "ok", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(payload: LoginRequest):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })
        return {"status": "ok", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
