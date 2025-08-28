import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from app.routers import auth, ocr, document, records  # package import via app/routers/__init__.py

app = FastAPI(title="FastAPI Groq + Supabase Backend")

# Create tmp dir if missing
TMP_DIR = os.path.join(os.path.dirname(__file__), "..", "tmp_files")
TMP_DIR = os.path.abspath(TMP_DIR)
os.makedirs(TMP_DIR, exist_ok=True)

# Mount static file serving for generated files
app.mount("/files", StaticFiles(directory=TMP_DIR), name="files")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
app.include_router(document.router, prefix="/document", tags=["document"])
app.include_router(records.router, prefix="/records", tags=["records"])

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI Groq+Supabase backend is running"}
