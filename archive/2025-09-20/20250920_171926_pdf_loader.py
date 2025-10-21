from typing import List
import fitz  # PyMuPDF
import os
from .ocr import ocr_pdf_if_needed

def extract_pdf_text_per_page(path: str) -> List[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    pages = []
    with fitz.open(path) as doc:
        for page in doc:
            txt = page.get_text("text")
            pages.append(txt)
    empty_ratio = sum(1 for p in pages if len(p.strip()) == 0) / max(1, len(pages))
    if empty_ratio > 0.3:
        ocr_path = ocr_pdf_if_needed(path)
        pages = []
        with fitz.open(ocr_path) as doc:
            for page in doc:
                pages.append(page.get_text("text"))
    return pages
