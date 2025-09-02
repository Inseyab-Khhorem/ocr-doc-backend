import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from app.routers import auth, ocr, document, records

app = FastAPI(title="DocuFlow Backend")

# CORS - Keep your specific origins
origins = [
    "https://inseyab-doc.netlify.app",
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tmp directory - Keep this, it's good
TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp_files")
os.makedirs(TMP_DIR, exist_ok=True)

# Mount static files - Keep this
app.mount("/files", StaticFiles(directory=TMP_DIR), name="files")

# Include routers - Keep your structure
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
app.include_router(document.router, prefix="/document", tags=["document"])
app.include_router(records.router, prefix="/records", tags=["records"])

# Keep your endpoints
@app.get("/")
def root():
    return {"status": "ok", "message": "DocuFlow backend running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Add global error handler to catch 500 errors
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error", 
            "path": str(request.url.path),
            "error": str(exc) if app.debug else "Server error"
        }
    )

# Add 404 handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Path {request.url.path} not found"}
    )