#!/usr/bin/env python3
"""
OCR Reader for Scanned Screenplay PDFs
Reads PDFs that are actually images/photos of scripts
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict
import logging
from PIL import Image
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRReader:
    """
    OCR Reader for extracting text from scanned PDFs.
    Uses multiple OCR engines for best results.
    """

    def __init__(self, language: str = 'por+eng'):
        """
        Initialize OCR Reader.

        Args:
            language: OCR language(s) - 'por' for Portuguese, 'eng' for English, 'por+eng' for both
        """
        self.language = language
        self.ocr_available = self._check_ocr_engines()

    def _check_ocr_engines(self) -> Dict[str, bool]:
        """Check which OCR engines are available."""
        engines = {}

        # Check for pytesseract
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            engines['tesseract'] = True
            logger.info("✓ Tesseract OCR available")
        except:
            engines['tesseract'] = False
            logger.warning("✗ Tesseract not available")

        # Check for easyocr
        try:
            import easyocr
            engines['easyocr'] = True
            logger.info("✓ EasyOCR available")
        except:
            engines['easyocr'] = False
            logger.warning("✗ EasyOCR not available")

        # Check for paddleocr
        try:
            from paddleocr import PaddleOCR
            engines['paddle'] = True
            logger.info("✓ PaddleOCR available")
        except:
            engines['paddle'] = False
            logger.warning("✗ PaddleOCR not available")

        return engines

    def pdf_to_images(self, pdf_path: Path) -> List[Image.Image]:
        """Convert PDF pages to images."""
        images = []

        try:
            # Try pdf2image (best quality)
            from pdf2image import convert_from_path
            images = convert_from_path(str(pdf_path), dpi=300)
            logger.info(f"Converted {len(images)} pages using pdf2image")
            return images
        except ImportError:
            logger.warning("pdf2image not available, trying PyMuPDF")

        try:
            # Fallback to PyMuPDF (fitz)
            import fitz
            pdf_document = fitz.open(str(pdf_path))

            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                images.append(img)

            pdf_document.close()
            logger.info(f"Converted {len(images)} pages using PyMuPDF")
            return images
        except ImportError:
            logger.warning("PyMuPDF not available, trying Pillow")

        try:
            # Last resort: Pillow (limited PDF support)
            from PIL import Image
            img = Image.open(str(pdf_path))
            images = [img]
            logger.info(f"Opened PDF as image using Pillow")
            return images
        except:
            logger.error(f"Could not convert PDF to images: {pdf_path}")
            return []

    def ocr_with_tesseract(self, image: Image.Image) -> str:
        """OCR using Tesseract."""
        try:
            import pytesseract

            # Preprocess image for better OCR
            image = self._preprocess_image(image)

            # Custom config for screenplay format
            custom_config = r'--oem 3 --psm 6'

            # Perform OCR
            text = pytesseract.image_to_string(
                image,
                lang=self.language.replace('+', '+'),
                config=custom_config
            )

            return text
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {e}")
            return ""

    def ocr_with_easyocr(self, image: Image.Image) -> str:
        """OCR using EasyOCR."""
        try:
            import easyocr
            import numpy as np

            # Initialize reader (cached)
            if not hasattr(self, '_easyocr_reader'):
                languages = self.language.split('+')
                if 'por' in languages:
                    languages = ['pt'] + [l for l in languages if l != 'por']
                if 'eng' in languages:
                    languages = ['en'] + [l for l in languages if l != 'eng']
                self._easyocr_reader = easyocr.Reader(languages)

            # Convert PIL to numpy
            img_array = np.array(image)

            # Perform OCR
            results = self._easyocr_reader.readtext(img_array)

            # Extract text
            text = '\n'.join([result[1] for result in results])
            return text
        except Exception as e:
            logger.error(f"EasyOCR failed: {e}")
            return ""

    def ocr_with_paddle(self, image: Image.Image) -> str:
        """OCR using PaddleOCR."""
        try:
            from paddleocr import PaddleOCR
            import numpy as np

            # Initialize PaddleOCR (cached)
            if not hasattr(self, '_paddle_ocr'):
                self._paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')

            # Convert PIL to numpy
            img_array = np.array(image)

            # Perform OCR
            result = self._paddle_ocr.ocr(img_array, cls=True)

            # Extract text
            text_lines = []
            for line in result[0]:
                text_lines.append(line[1][0])

            return '\n'.join(text_lines)
        except Exception as e:
            logger.error(f"PaddleOCR failed: {e}")
            return ""

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results."""
        try:
            from PIL import ImageEnhance, ImageFilter, ImageOps

            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)

            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=3))

            # Sharpen
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)

            # Invert if text is white on black
            # (common in some screenplay formats)
            pixels = image.getdata()
            avg_pixel = sum(pixels) / len(pixels)
            if avg_pixel < 128:  # Dark image
                image = ImageOps.invert(image)

            return image
        except:
            return image

    def extract_text_from_pdf(self, pdf_path: Path, engine: str = 'auto') -> Optional[str]:
        """
        Extract text from scanned PDF.

        Args:
            pdf_path: Path to PDF file
            engine: OCR engine to use ('tesseract', 'easyocr', 'paddle', 'auto')

        Returns:
            Extracted text or None if failed
        """
        if not pdf_path.exists():
            logger.error(f"PDF not found: {pdf_path}")
            return None

        logger.info(f"Processing: {pdf_path.name}")

        # Convert PDF to images
        images = self.pdf_to_images(pdf_path)
        if not images:
            logger.error("Failed to convert PDF to images")
            return None

        # Perform OCR on each page
        all_text = []

        for i, image in enumerate(images):
            logger.info(f"OCR page {i+1}/{len(images)}")

            page_text = ""

            if engine == 'auto':
                # Try engines in order of preference
                if self.ocr_available.get('tesseract'):
                    page_text = self.ocr_with_tesseract(image)
                elif self.ocr_available.get('easyocr'):
                    page_text = self.ocr_with_easyocr(image)
                elif self.ocr_available.get('paddle'):
                    page_text = self.ocr_with_paddle(image)
            elif engine == 'tesseract' and self.ocr_available.get('tesseract'):
                page_text = self.ocr_with_tesseract(image)
            elif engine == 'easyocr' and self.ocr_available.get('easyocr'):
                page_text = self.ocr_with_easyocr(image)
            elif engine == 'paddle' and self.ocr_available.get('paddle'):
                page_text = self.ocr_with_paddle(image)

            if page_text:
                all_text.append(page_text)

        # Combine all pages
        full_text = '\n\n'.join(all_text)

        # Post-process for screenplay format
        full_text = self._postprocess_screenplay_text(full_text)

        return full_text if full_text.strip() else None

    def _postprocess_screenplay_text(self, text: str) -> str:
        """Clean up OCR text for screenplay format."""
        import re

        # Fix common OCR errors in screenplays
        replacements = {
            'INT,': 'INT.',
            'EXT,': 'EXT.',
            'FADE IN;': 'FADE IN:',
            'FADE OUT;': 'FADE OUT.',
            'CUT TO;': 'CUT TO:',
            '  ': ' ',  # Multiple spaces to single
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # Fix line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Detect and fix character names (usually in caps)
        lines = text.split('\n')
        fixed_lines = []

        for i, line in enumerate(lines):
            line = line.strip()

            # Character name detection
            if line.isupper() and len(line.split()) <= 3 and len(line) > 2:
                # Likely a character name
                fixed_lines.append('\n' + line)
            else:
                fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def batch_process_pdfs(self, pdf_dir: Path, output_dir: Path, engine: str = 'auto') -> Dict:
        """
        Process multiple PDFs with OCR.

        Args:
            pdf_dir: Directory containing PDFs
            output_dir: Directory to save extracted text
            engine: OCR engine to use

        Returns:
            Statistics dictionary
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_files = list(pdf_dir.glob('*.pdf'))
        stats = {
            'total': len(pdf_files),
            'successful': 0,
            'failed': 0,
            'pages_processed': 0
        }

        logger.info(f"Found {len(pdf_files)} PDFs to process")

        for pdf_path in pdf_files:
            try:
                text = self.extract_text_from_pdf(pdf_path, engine)

                if text:
                    # Save extracted text
                    output_path = output_dir / f"{pdf_path.stem}.txt"
                    output_path.write_text(text, encoding='utf-8')
                    stats['successful'] += 1
                    logger.info(f"✓ Saved: {output_path.name}")
                else:
                    stats['failed'] += 1
                    logger.warning(f"✗ No text extracted: {pdf_path.name}")

            except Exception as e:
                stats['failed'] += 1
                logger.error(f"✗ Error processing {pdf_path.name}: {e}")

        return stats


def main():
    """Test OCR reader."""
    print("="*60)
    print("OCR READER FOR SCANNED SCREENPLAYS")
    print("="*60)

    # Initialize reader
    reader = OCRReader(language='por+eng')

    # Check available engines
    print("\nAvailable OCR Engines:")
    for engine, available in reader.ocr_available.items():
        status = "✓" if available else "✗"
        print(f"  {status} {engine}")

    # Test with a sample PDF if available
    test_pdf = Path("digilibrary/BIBLIOTECA_ROTEIROS/SONHOS SEM LEMBRANÇAS T.3.pdf")

    if test_pdf.exists():
        print(f"\nTesting with: {test_pdf.name}")
        text = reader.extract_text_from_pdf(test_pdf)

        if text:
            print(f"\nExtracted {len(text)} characters")
            print("\nFirst 500 characters:")
            print("-"*40)
            print(text[:500])
            print("-"*40)
        else:
            print("No text extracted")
    else:
        print(f"\nTest PDF not found: {test_pdf}")

    print("\n" + "="*60)
    print("OCR Reader ready for use!")
    print("="*60)


if __name__ == "__main__":
    main()