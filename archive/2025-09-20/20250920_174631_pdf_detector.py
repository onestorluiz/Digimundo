#!/usr/bin/env python3
"""
PDF Type Detector - Identifies if PDF contains text or images
Intelligently routes to appropriate processing pipeline
"""

import PyPDF2
import pdfplumber
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFType(Enum):
    """PDF content types."""
    TEXT = "text"          # Native text PDF
    IMAGE = "image"        # Scanned/image PDF
    MIXED = "mixed"        # Contains both
    ENCRYPTED = "encrypted" # Password protected
    CORRUPTED = "corrupted" # Cannot be read
    EMPTY = "empty"        # No content


@dataclass
class PDFAnalysis:
    """PDF analysis results."""
    pdf_type: PDFType
    confidence: float
    page_count: int
    text_pages: int
    image_pages: int
    avg_chars_per_page: float
    has_text: bool
    has_images: bool
    needs_ocr: bool
    quality_score: float
    metadata: Dict


class PDFDetector:
    """
    Intelligent PDF type detector.
    Determines optimal processing strategy.
    """

    def __init__(self, min_chars_for_text: int = 100):
        """
        Initialize detector.

        Args:
            min_chars_for_text: Minimum characters to consider page as text
        """
        self.min_chars = min_chars_for_text

    def analyze_pdf(self, pdf_path: Path) -> PDFAnalysis:
        """
        Comprehensive PDF analysis.

        Args:
            pdf_path: Path to PDF file

        Returns:
            PDFAnalysis object with detailed information
        """
        if not pdf_path.exists():
            logger.error(f"PDF not found: {pdf_path}")
            return PDFAnalysis(
                pdf_type=PDFType.CORRUPTED,
                confidence=1.0,
                page_count=0,
                text_pages=0,
                image_pages=0,
                avg_chars_per_page=0,
                has_text=False,
                has_images=False,
                needs_ocr=False,
                quality_score=0,
                metadata={"error": "File not found"}
            )

        # Try multiple methods
        analysis = self._analyze_with_pdfplumber(pdf_path)

        if analysis.pdf_type == PDFType.CORRUPTED:
            # Fallback to PyPDF2
            analysis = self._analyze_with_pypdf2(pdf_path)

        # Determine if OCR is needed
        analysis.needs_ocr = self._needs_ocr(analysis)

        # Calculate quality score
        analysis.quality_score = self._calculate_quality(analysis)

        return analysis

    def _analyze_with_pdfplumber(self, pdf_path: Path) -> PDFAnalysis:
        """Analyze using pdfplumber."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                page_count = len(pdf.pages)
                text_pages = 0
                image_pages = 0
                total_chars = 0
                has_images = False

                for page in pdf.pages:
                    # Extract text
                    text = page.extract_text() or ""
                    char_count = len(text.strip())
                    total_chars += char_count

                    if char_count >= self.min_chars:
                        text_pages += 1

                    # Check for images
                    if hasattr(page, 'images') and page.images:
                        has_images = True
                        image_pages += 1

                # Determine type
                has_text = text_pages > 0
                avg_chars = total_chars / page_count if page_count > 0 else 0

                if text_pages == 0 and page_count > 0:
                    pdf_type = PDFType.IMAGE
                    confidence = 0.95
                elif text_pages == page_count:
                    pdf_type = PDFType.TEXT
                    confidence = 0.95 if avg_chars > 500 else 0.8
                elif text_pages > 0 and text_pages < page_count:
                    pdf_type = PDFType.MIXED
                    confidence = 0.9
                else:
                    pdf_type = PDFType.EMPTY
                    confidence = 1.0

                return PDFAnalysis(
                    pdf_type=pdf_type,
                    confidence=confidence,
                    page_count=page_count,
                    text_pages=text_pages,
                    image_pages=image_pages,
                    avg_chars_per_page=avg_chars,
                    has_text=has_text,
                    has_images=has_images,
                    needs_ocr=False,  # Will be set later
                    quality_score=0,  # Will be calculated
                    metadata={
                        "tool": "pdfplumber",
                        "total_chars": total_chars
                    }
                )

        except Exception as e:
            logger.error(f"pdfplumber failed: {e}")
            return PDFAnalysis(
                pdf_type=PDFType.CORRUPTED,
                confidence=0.5,
                page_count=0,
                text_pages=0,
                image_pages=0,
                avg_chars_per_page=0,
                has_text=False,
                has_images=False,
                needs_ocr=False,
                quality_score=0,
                metadata={"error": str(e)}
            )

    def _analyze_with_pypdf2(self, pdf_path: Path) -> PDFAnalysis:
        """Analyze using PyPDF2 as fallback."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                # Check if encrypted
                if reader.is_encrypted:
                    return PDFAnalysis(
                        pdf_type=PDFType.ENCRYPTED,
                        confidence=1.0,
                        page_count=len(reader.pages),
                        text_pages=0,
                        image_pages=0,
                        avg_chars_per_page=0,
                        has_text=False,
                        has_images=False,
                        needs_ocr=False,
                        quality_score=0,
                        metadata={"encrypted": True}
                    )

                page_count = len(reader.pages)
                text_pages = 0
                total_chars = 0

                for page in reader.pages:
                    text = page.extract_text()
                    char_count = len(text.strip())
                    total_chars += char_count

                    if char_count >= self.min_chars:
                        text_pages += 1

                avg_chars = total_chars / page_count if page_count > 0 else 0
                has_text = text_pages > 0

                if text_pages == 0:
                    pdf_type = PDFType.IMAGE
                elif text_pages == page_count:
                    pdf_type = PDFType.TEXT
                else:
                    pdf_type = PDFType.MIXED

                confidence = 0.8  # Lower confidence for PyPDF2

                return PDFAnalysis(
                    pdf_type=pdf_type,
                    confidence=confidence,
                    page_count=page_count,
                    text_pages=text_pages,
                    image_pages=page_count - text_pages,
                    avg_chars_per_page=avg_chars,
                    has_text=has_text,
                    has_images=text_pages < page_count,
                    needs_ocr=False,
                    quality_score=0,
                    metadata={
                        "tool": "PyPDF2",
                        "total_chars": total_chars
                    }
                )

        except Exception as e:
            logger.error(f"PyPDF2 failed: {e}")
            return PDFAnalysis(
                pdf_type=PDFType.CORRUPTED,
                confidence=1.0,
                page_count=0,
                text_pages=0,
                image_pages=0,
                avg_chars_per_page=0,
                has_text=False,
                has_images=False,
                needs_ocr=False,
                quality_score=0,
                metadata={"error": str(e)}
            )

    def _needs_ocr(self, analysis: PDFAnalysis) -> bool:
        """Determine if PDF needs OCR processing."""
        if analysis.pdf_type == PDFType.IMAGE:
            return True
        elif analysis.pdf_type == PDFType.MIXED:
            # Need OCR for pages without text
            return analysis.image_pages > 0
        elif analysis.pdf_type == PDFType.TEXT:
            # Check if text quality is too low
            return analysis.avg_chars_per_page < 200
        else:
            return False

    def _calculate_quality(self, analysis: PDFAnalysis) -> float:
        """
        Calculate quality score (0-1).
        Higher score = better quality, less need for processing.
        """
        if analysis.pdf_type == PDFType.CORRUPTED:
            return 0.0
        elif analysis.pdf_type == PDFType.ENCRYPTED:
            return 0.1
        elif analysis.pdf_type == PDFType.EMPTY:
            return 0.0

        score = 0.0

        # Text presence (40% weight)
        if analysis.has_text:
            text_ratio = analysis.text_pages / max(analysis.page_count, 1)
            score += text_ratio * 0.4

        # Character density (30% weight)
        if analysis.avg_chars_per_page > 0:
            # Normalize to 0-1 (assume 2000 chars/page is excellent)
            char_score = min(analysis.avg_chars_per_page / 2000, 1.0)
            score += char_score * 0.3

        # Consistency (20% weight)
        if analysis.pdf_type == PDFType.TEXT:
            score += 0.2
        elif analysis.pdf_type == PDFType.MIXED:
            score += 0.1

        # Confidence (10% weight)
        score += analysis.confidence * 0.1

        return min(score, 1.0)

    def get_processing_recommendation(self, analysis: PDFAnalysis) -> str:
        """
        Get processing recommendation based on analysis.

        Args:
            analysis: PDFAnalysis object

        Returns:
            Recommendation string
        """
        if analysis.pdf_type == PDFType.TEXT and analysis.quality_score > 0.7:
            return "Direct text extraction (high quality)"
        elif analysis.pdf_type == PDFType.TEXT and analysis.quality_score <= 0.7:
            return "Text extraction with quality enhancement"
        elif analysis.pdf_type == PDFType.IMAGE:
            return "Full OCR processing required"
        elif analysis.pdf_type == PDFType.MIXED:
            return "Hybrid: Text extraction + OCR for images"
        elif analysis.pdf_type == PDFType.ENCRYPTED:
            return "Decrypt first, then reanalyze"
        elif analysis.pdf_type == PDFType.CORRUPTED:
            return "Repair or re-scan document"
        else:
            return "Manual review recommended"


def analyze_pdf_batch(pdf_dir: Path) -> Dict[str, PDFAnalysis]:
    """
    Analyze all PDFs in directory.

    Args:
        pdf_dir: Directory containing PDFs

    Returns:
        Dictionary mapping filename to analysis
    """
    detector = PDFDetector()
    results = {}

    pdf_files = list(pdf_dir.glob("*.pdf"))
    logger.info(f"Analyzing {len(pdf_files)} PDFs...")

    for pdf_path in pdf_files:
        logger.info(f"Analyzing: {pdf_path.name}")
        analysis = detector.analyze_pdf(pdf_path)
        results[pdf_path.name] = analysis

        # Log summary
        logger.info(f"  Type: {analysis.pdf_type.value}")
        logger.info(f"  Quality: {analysis.quality_score:.2f}")
        logger.info(f"  Needs OCR: {analysis.needs_ocr}")

    return results


def main():
    """Test PDF detector."""
    print("="*60)
    print("PDF TYPE DETECTOR")
    print("="*60)

    detector = PDFDetector()

    # Test with sample PDFs
    test_pdfs = [
        Path("digilibrary/BIBLIOTECA_ROTEIROS/Alien - Screenplay-ocr.pdf"),
        Path("digilibrary/BIBLIOTECA_ROTEIROS/The Matrix - Screenplay.pdf"),
        Path("data/sample.pdf")
    ]

    for pdf_path in test_pdfs:
        if pdf_path.exists():
            print(f"\nAnalyzing: {pdf_path.name}")
            print("-"*40)

            analysis = detector.analyze_pdf(pdf_path)

            print(f"Type: {analysis.pdf_type.value}")
            print(f"Confidence: {analysis.confidence:.2f}")
            print(f"Pages: {analysis.page_count}")
            print(f"Text pages: {analysis.text_pages}")
            print(f"Image pages: {analysis.image_pages}")
            print(f"Avg chars/page: {analysis.avg_chars_per_page:.0f}")
            print(f"Quality score: {analysis.quality_score:.2f}")
            print(f"Needs OCR: {analysis.needs_ocr}")
            print(f"Recommendation: {detector.get_processing_recommendation(analysis)}")

    print("\n" + "="*60)
    print("Detector ready for use!")


if __name__ == "__main__":
    main()