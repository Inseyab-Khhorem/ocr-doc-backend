import os
import httpx
from dotenv import load_dotenv
import base64

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1")

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}

# ---------- TEXT GENERATION ----------
async def groq_generate_text(prompt: str) -> str:
    """
    Call Groq's OpenAI-compatible Chat Completions API.
    """
    payload = {
        "model": "llama3-8b-8192",  # choose available model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 800
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{GROQ_API_URL}/chat/completions", headers=HEADERS, json=payload)
        r.raise_for_status()
        resp = r.json()
    
    return resp["choices"][0]["message"]["content"]

# ---------- OCR (vision / image captioning) ----------
async def groq_ocr_from_bytes(file_bytes: bytes, filename: str = "file.png") -> str:
    """
    Send image bytes to Groq vision model for OCR.
    """
    b64_image = base64.b64encode(file_bytes).decode("utf-8")
    
    # Determine the image type based on filename extension
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        image_type = "jpeg"
    elif filename.lower().endswith('.png'):
        image_type = "png"
    elif filename.lower().endswith('.webp'):
        image_type = "webp"
    else:
        # Default to png if unknown
        image_type = "png"

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",  # Updated to current vision model
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "Extract all readable text from this image. Return only the clean text without any additional formatting or explanations."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{image_type};base64,{b64_image}"
                        }
                    }
                ]
            }
        ],
        "max_completion_tokens": 1200,  # Updated parameter name
        "temperature": 0.1  # Lower temperature for more consistent OCR results
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{GROQ_API_URL}/chat/completions",
            headers=HEADERS,
            json=payload
        )
        r.raise_for_status()
        resp = r.json()

    return resp["choices"][0]["message"]["content"]