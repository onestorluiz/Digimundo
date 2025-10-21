import os, subprocess, tempfile, shutil
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from ..config import load_config

_cfg = load_config()

def has_ocrmypdf() -> bool:
    return shutil.which("ocrmypdf") is not None

def ocr_pdf_if_needed(path: str) -> str:
    os.makedirs(_cfg.paths.ocr_tmp_dir, exist_ok=True)
    out_pdf = os.path.join(_cfg.paths.ocr_tmp_dir, os.path.basename(path).replace(".pdf", "_ocr.pdf"))
    if os.path.exists(out_pdf):
        return out_pdf
    if has_ocrmypdf():
        subprocess.run(["ocrmypdf", "--skip-text", path, out_pdf], check=False)
        return out_pdf if os.path.exists(out_pdf) else path
    images = convert_from_path(path, dpi=200)
    tmpdir = tempfile.mkdtemp()
    try:
        img_paths = []
        for i, img in enumerate(images):
            ip = os.path.join(tmpdir, f"page_{i}.png")
            img.save(ip, "PNG")
            img_paths.append(ip)
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        for i, ip in enumerate(img_paths):
            outp = os.path.join(tmpdir, f"page_{i}")
            subprocess.run(["tesseract", ip, outp, "pdf"], check=False)
            merger.append(outp + ".pdf")
        merger.write(out_pdf)
        merger.close()
        return out_pdf
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
