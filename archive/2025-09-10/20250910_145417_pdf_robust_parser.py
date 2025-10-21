"""Parser robusto para PDFs com fallback"""
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

def parse_pdf_safe(pdf_path: Path, max_size_mb: int = 50) -> Optional[str]:
    """Parse PDF com múltiplos fallbacks"""
    
    # Verificar tamanho
    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    if size_mb > max_size_mb:
        logger.warning(f"PDF muito grande: {size_mb:.1f}MB > {max_size_mb}MB")
        return f"[PDF grande demais: {size_mb:.1f}MB]"
    
    # Tentar PyPDF2
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:100]:  # Limitar a 100 páginas
                text += page.extract_text()
            return text
    except Exception as e:
        logger.debug(f"PyPDF2 falhou: {e}")
    
    # Fallback para pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages[:100]:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        logger.debug(f"pdfplumber falhou: {e}")
    
    return "[Não foi possível extrair texto do PDF]"
