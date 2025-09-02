from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # ADDED MISSING IMPORT

router = APIRouter()  # ADDED MISSING LINE

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/admin/login")
async def admin_login(request: LoginRequest):
    if request.email == "khhorem.khan@raqmiyat.com" and request.password == "@Inseyab123":
        return {
            "data": {
                "access_token": "admin_mock_token"
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
