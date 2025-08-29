from fastapi import APIRouter
router = APIRouter()

@router.post("/convert")
async def convert_ocr(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    request: Request = None
):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    content = await file.read()
    original_id, original_path = save_bytes_to_file(content, suffix=f"_{file.filename}")

    try:
        extracted_text = await groq_ocr_from_bytes(content, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq OCR error: {e}")

    docx_id, docx_path = write_text_to_docx(extracted_text)
    pdf_id, pdf_path = write_text_to_pdf(extracted_text)

    docx_url = f"{FILES_BASE_URL}/{docx_path.name}"
    pdf_url = f"{FILES_BASE_URL}/{pdf_path.name}"

    record = {
        "id": docx_id,
        "user_id": user_id,
        "action": "OCR Conversion",
        "input_file_url": f"{FILES_BASE_URL}/{original_path.name}",
        "output_file_url_docx": docx_url,
        "output_file_url_pdf": pdf_url,
    }

    try:
        supabase.auth.set_auth(token.replace("Bearer ", ""))
        supabase.table("records").insert(record).execute()
    except Exception as e:
        print("Failed saving record to Supabase:", e)

    return {
        "text": extracted_text,
        "files": {"docx": docx_url, "pdf": pdf_url}
    }
