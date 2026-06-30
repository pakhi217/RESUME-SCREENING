"""
utils/text_extractor.py
───────────────────────
Extracts raw text from PDF and DOCX resume files.
Falls back gracefully when optional libraries are missing.
"""

from __future__ import annotations
import io
import re


# ── PDF extraction ────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF bytes.
    Uses PyPDF2; falls back to a byte-decode heuristic on failure.
    """
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages  = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
    except Exception as exc:
        # Heuristic fallback: decode printable ASCII from raw bytes
        text = file_bytes.decode("latin-1", errors="replace")
        text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
        text = re.sub(r'\s{4,}', '\n', text)
        return text[:8000]          # cap for safety


# ── DOCX extraction ───────────────────────────────────────────────────────────

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        from docx import Document
        doc   = Document(io.BytesIO(file_bytes))
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paras)
    except Exception as exc:
        return ""


# ── Router ────────────────────────────────────────────────────────────────────

def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Route extraction by file extension.
    Returns cleaned plain-text string.
    """
    ext = filename.lower().rsplit(".", 1)[-1]

    if ext == "pdf":
        raw = extract_text_from_pdf(file_bytes)
    elif ext in ("docx", "doc"):
        raw = extract_text_from_docx(file_bytes)
    elif ext == "txt":
        raw = file_bytes.decode("utf-8", errors="replace")
    else:
        raw = ""

    # Basic cleaning
    raw = re.sub(r'\s+', ' ', raw)
    raw = raw.strip()
    return raw
