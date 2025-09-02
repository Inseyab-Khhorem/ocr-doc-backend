# main.py - CORRECTED
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routers import auth, ocr, document, records

app = FastAPI(title="DocuFlow Backend")

# CORS
origins = [
    "https://inseyab-doc.netlify.app",
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # FIXED: was [""]
    allow_headers=["*"],  # FIXED: was [""]
)

# Create tmp directory
TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp_files")  # FIXED: was file
os.makedirs(TMP_DIR, exist_ok=True)

# Mount static files
app.mount("/files", StaticFiles(directory=TMP_DIR), name="files")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
app.include_router(document.router, prefix="/document", tags=["document"])
app.include_router(records.router, prefix="/records", tags=["records"])

@app.get("/")
def root():
    return {"status": "ok", "message": "DocuFlow backend running"}

@app.get("/health")
def health():
    return {"status": "healthy"}