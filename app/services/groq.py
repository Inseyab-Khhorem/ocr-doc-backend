import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.ai/v1/inference")

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}

async def groq_ocr_from_bytes(file_bytes: bytes, filename: str = "file") -> str:
    """
    Generic wrapper to send file bytes to Groq OCR model and return extracted text.
    Adjust the payload to match your Groq model's expected inputs.
    """
    # Example payload shape - replace 'model' and keys as needed for your Groq model
    payload = {
        "model": "ocr",  # placeholder; change to real model id if needed
        "input": {
            "filename": filename,
            # if Groq expects base64 or binary, modify accordingly
            "file": file_bytes.decode("latin1")  # NOT ideal for large files; adjust per Groq API
        }
    }
    # Many Groq APIs accept multipart binary; if so you should adapt to upload file in form-data.
    # This is a placeholder: replace this logic with the exact Groq spec you have.
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(GROQ_API_URL, headers=HEADERS, json=payload)
        r.raise_for_status()
        resp = r.json()
    # Heuristic: try multiple keys
    text = ""
    if isinstance(resp, dict):
        text = resp.get("text") or resp.get("response_text") or resp.get("output") or str(resp)
    else:
        text = str(resp)
    return text

async def groq_generate_text(prompt: str) -> str:
    """
    Generic text generation wrapper for Groq.
    Adjust payload/model name according to your Groq model API spec.
    """
    payload = {
        "model": "text-generation",  # placeholder model name
        "input": {"prompt": prompt, "max_tokens": 1000}
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(GROQ_API_URL, headers=HEADERS, json=payload)
        r.raise_for_status()
        resp = r.json()
    if isinstance(resp, dict):
        return resp.get("text") or resp.get("response_text") or resp.get("output", "")
    return str(resp)
