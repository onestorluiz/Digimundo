"""
PDF extraction utilities with real text extraction
"""
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def extract_text(pdf_path: Path) -> str:
    """
    Extract text from PDF with fallback strategies.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    if not pdf_path.exists():
        logger.error(f"PDF not found: {pdf_path}")
        return ""
    
    text = ""
    extraction_method = "none"
    
    # Try pdfminer.six first (better for complex layouts)
    try:
        from pdfminer.high_level import extract_text as pdfminer_extract
        text = pdfminer_extract(str(pdf_path))
        extraction_method = "pdfminer"
        logger.debug(f"Extracted {len(text)} chars via pdfminer from {pdf_path.name}")
    except ImportError:
        logger.debug("pdfminer.six not available")
    except Exception as e:
        logger.warning(f"pdfminer extraction failed: {e}")
    
    # Fallback to pypdf if pdfminer failed
    if not text or len(text) < 100:
        try:
            import pypdf
            reader = pypdf.PdfReader(str(pdf_path))
            pages_text = []
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    pages_text.append(page_text)
            text = "\n\n".join(pages_text)
            extraction_method = "pypdf"
            logger.debug(f"Extracted {len(text)} chars via pypdf from {pdf_path.name}")
        except ImportError:
            logger.debug("pypdf not available")
        except Exception as e:
            logger.warning(f"pypdf extraction failed: {e}")
    
    # Fallback to PyPDF2 if still no text
    if not text or len(text) < 100:
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages_text = []
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                text = "\n\n".join(pages_text)
                extraction_method = "PyPDF2"
                logger.debug(f"Extracted {len(text)} chars via PyPDF2 from {pdf_path.name}")
        except ImportError:
            logger.debug("PyPDF2 not available")
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {e}")
    
    # Check if PDF might be scanned (very little text extracted)
    char_to_size_ratio = len(text) / (pdf_path.stat().st_size / 1024) if pdf_path.stat().st_size > 0 else 0
    is_likely_scanned = char_to_size_ratio < 10 and len(text) < 500
    
    if is_likely_scanned:
        logger.info(f"PDF {pdf_path.name} likely scanned (ratio: {char_to_size_ratio:.2f})")
        # Try OCR if available
        ocr_text = attempt_ocr(pdf_path)
        if ocr_text and len(ocr_text) > len(text):
            text = ocr_text
            extraction_method = "ocr"
    
    # Normalize text
    text = normalize_text(text)
    
    # If still no text, return stub
    if not text:
        logger.warning(f"No text extracted from {pdf_path.name}, using stub")
        return f"[PDF Content: {pdf_path.name}]"
    
    logger.info(f"Extracted {len(text)} chars from {pdf_path.name} via {extraction_method}")
    return text

def attempt_ocr(pdf_path: Path) -> str:
    """
    Attempt OCR on PDF pages.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        OCR extracted text or empty string
    """
    try:
        import pytesseract
        from pdf2image import convert_from_path
        
        # Convert PDF pages to images
        images = convert_from_path(str(pdf_path), dpi=200, first_page=1, last_page=3)  # OCR first 3 pages as sample
        
        ocr_texts = []
        for i, image in enumerate(images):
            try:
                page_text = pytesseract.image_to_string(image, lang='por+eng')
                if page_text:
                    ocr_texts.append(page_text)
                    logger.debug(f"OCR page {i+1}: {len(page_text)} chars")
            except Exception as e:
                logger.warning(f"OCR failed for page {i+1}: {e}")
        
        text = "\n\n".join(ocr_texts)
        logger.info(f"OCR extracted {len(text)} chars from {pdf_path.name}")
        return text
        
    except ImportError as e:
        logger.debug(f"OCR dependencies not available: {e}")
        return ""
    except Exception as e:
        logger.warning(f"OCR failed: {e}")
        return ""

def normalize_text(text: str) -> str:
    """
    Normalize extracted text.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    import re
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common extraction artifacts
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)  # Rejoin hyphenated words
    text = re.sub(r'\s+([.,;!?])', r'\1', text)    # Fix punctuation spacing
    
    # Remove multiple consecutive line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def get_pdf_metadata(pdf_path: Path) -> dict:
    """
    Extract metadata from PDF.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Metadata dictionary
    """
    metadata = {
        "title": pdf_path.stem,
        "pages": 0,
        "author": None,
        "creation_date": None
    }
    
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        metadata["pages"] = len(reader.pages)
        
        if reader.metadata:
            metadata["title"] = reader.metadata.get('/Title', pdf_path.stem)
            metadata["author"] = reader.metadata.get('/Author')
            metadata["creation_date"] = str(reader.metadata.get('/CreationDate', ''))
            
    except Exception as e:
        logger.debug(f"Could not extract metadata: {e}")
    
    return metadata