import os
import uuid
from pathlib import Path
from typing import Tuple
from docx import Document as DocxDocument
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

TMP_DIR = Path(__file__).resolve().parents[1] / "tmp_files"
TMP_DIR.mkdir(parents=True, exist_ok=True)

def save_bytes_to_file(data: bytes, suffix: str = "") -> Tuple[str, Path]:
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{suffix}"
    path = TMP_DIR / filename
    with open(path, "wb") as f:
        f.write(data)
    return file_id, path

def write_text_to_docx(text: str) -> Tuple[str, Path]:
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.docx"
    path = TMP_DIR / filename
    doc = DocxDocument()
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(path)
    return file_id, path

def write_text_to_pdf(text: str) -> Tuple[str, Path]:
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.pdf"
    path = TMP_DIR / filename
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    # Simple text wrapping
    lines = []
    for paragraph in text.split("\n"):
        # naive wrap at ~90 chars
        while len(paragraph) > 90:
            lines.append(paragraph[:90])
            paragraph = paragraph[90:]
        lines.append(paragraph)
    y = height - 40
    for ln in lines:
        c.drawString(40, y, ln)
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    return file_id, path
