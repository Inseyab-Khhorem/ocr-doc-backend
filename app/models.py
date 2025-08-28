from pydantic import BaseModel

class GenerateRequest(BaseModel):
    user_id: str
    prompt: str

class RecordsListResponse(BaseModel):
    id: str
    user_id: str
    action_type: str
    timestamp: str
    file_url: str
