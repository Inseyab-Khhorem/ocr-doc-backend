from pydantic import BaseModel

class GenerateRequest(BaseModel):
    user_id: str
    prompt: str

class RecordsListResponse(BaseModel):
    id: str
    user_id: str
    action: str   # matches DB column
    input_file_url: str | None = None
    output_file_url_docx: str | None = None
    output_file_url_pdf: str | None = None
    prompt: str | None = None
    created_at: str
