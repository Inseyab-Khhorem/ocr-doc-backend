from fastapi import APIRouter
router = APIRouter()


@router.post("/generate")
async def generate_document(payload: GenerateRequest, request: Request):
    # Extract JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    try:
        generated_text = await groq_generate_text(payload.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq generation error: {e}")

    docx_id, docx_path = write_text_to_docx(generated_text)
    pdf_id, pdf_path = write_text_to_pdf(generated_text)

    docx_url = f"{FILES_BASE_URL}/{docx_path.name}"
    pdf_url = f"{FILES_BASE_URL}/{pdf_path.name}"

    record = {
        "id": docx_id,
        "user_id": payload.user_id,
        "action": "Document Generation",
        "output_file_url_docx": docx_url,
        "output_file_url_pdf": pdf_url,
        "prompt": payload.prompt,
    }

    try:
        supabase.auth.set_auth(token.replace("Bearer ", ""))
        supabase.table("records").insert(record).execute()
    except Exception as e:
        print("Failed saving document record to Supabase:", e)

    return {
        "document": generated_text,
        "files": {"docx": docx_url, "pdf": pdf_url}
    }
