#!/usr/bin/env python3
"""
Unified OCR Pipeline - Intelligent PDF Processing
Orchestrates detection, OCR, and AI correction
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from .pdf_detector import PDFDetector, PDFType
from .ocr_reader import OCRReader
from .ocr_ai_corrector import OCRAICorrector, OCRCorrection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class OCRPipelineResult:
    """Complete OCR pipeline result."""
    pdf_path: str
    pdf_type: str
    needs_ocr: bool
    ocr_performed: bool
    ai_correction: bool
    text_extracted: bool
    output_path: Optional[str]
    pages_processed: int
    processing_time: float
    quality_score: float
    error: Optional[str] = None
    stats: Dict = None


class OCRPipeline:
    """
    Unified OCR Pipeline for intelligent PDF processing.
    Combines detection, extraction, and AI correction.
    """

    def __init__(
        self,
        language: str = "por+eng",
        use_ai_correction: bool = True,
        ai_model: str = "phi3:mini",
        parallel_pages: int = 2
    ):
        """
        Initialize OCR pipeline.

        Args:
            language: OCR languages
            use_ai_correction: Enable AI-powered correction
            ai_model: Ollama model for corrections
            parallel_pages: Number of pages to process in parallel
        """
        self.detector = PDFDetector()
        self.reader = OCRReader(language=language)
        self.corrector = OCRAICorrector(model=ai_model) if use_ai_correction else None
        self.use_ai = use_ai_correction
        self.parallel = parallel_pages

    def process_pdf(
        self,
        pdf_path: Path,
        output_dir: Optional[Path] = None,
        force_ocr: bool = False
    ) -> OCRPipelineResult:
        """
        Process single PDF through complete pipeline.

        Args:
            pdf_path: Path to PDF
            output_dir: Directory for output (optional)
            force_ocr: Force OCR even for text PDFs

        Returns:
            OCRPipelineResult with all details
        """
        start_time = time.time()
        result = OCRPipelineResult(
            pdf_path=str(pdf_path),
            pdf_type="unknown",
            needs_ocr=False,
            ocr_performed=False,
            ai_correction=False,
            text_extracted=False,
            output_path=None,
            pages_processed=0,
            processing_time=0,
            quality_score=0
        )

        try:
            logger.info(f"Processing: {pdf_path.name}")

            # Step 1: Analyze PDF
            logger.info("Step 1: Analyzing PDF type...")
            analysis = self.detector.analyze_pdf(pdf_path)
            result.pdf_type = analysis.pdf_type.value
            result.needs_ocr = analysis.needs_ocr or force_ocr
            result.quality_score = analysis.quality_score
            result.pages_processed = analysis.page_count

            logger.info(f"  Type: {result.pdf_type}")
            logger.info(f"  Quality: {result.quality_score:.2f}")
            logger.info(f"  Needs OCR: {result.needs_ocr}")

            # Step 2: Extract text
            text = None

            if result.needs_ocr:
                # Use OCR
                logger.info("Step 2: Performing OCR...")
                text = self._perform_ocr_with_correction(pdf_path, analysis)
                result.ocr_performed = True
                result.ai_correction = self.use_ai
            else:
                # Direct extraction
                logger.info("Step 2: Direct text extraction...")
                text = self._extract_text_directly(pdf_path)

            if text:
                result.text_extracted = True

                # Step 3: Save output
                if output_dir:
                    output_path = self._save_output(pdf_path, text, output_dir, analysis)
                    result.output_path = str(output_path)
                    logger.info(f"Step 3: Saved to {output_path.name}")

                # Calculate stats
                result.stats = {
                    "total_chars": len(text),
                    "total_lines": len(text.split('\n')),
                    "avg_chars_per_page": len(text) / max(result.pages_processed, 1)
                }

        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            result.error = str(e)

        result.processing_time = time.time() - start_time
        logger.info(f"Completed in {result.processing_time:.2f}s")

        return result

    def _perform_ocr_with_correction(self, pdf_path: Path, analysis) -> Optional[str]:
        """Perform OCR with optional AI correction."""
        try:
            # First, do OCR
            raw_text = self.reader.extract_text_from_pdf(pdf_path)

            if not raw_text:
                return None

            # Then apply AI correction if enabled
            if self.corrector and self.use_ai:
                logger.info("  Applying AI correction...")
                
                # Split into chunks for AI processing
                chunks = self._split_text_chunks(raw_text)
                corrected_chunks = []

                for i, chunk in enumerate(chunks):
                    logger.info(f"  Correcting chunk {i+1}/{len(chunks)}")
                    correction = self.corrector.correct_with_ai(
                        chunk,
                        context="screenplay"
                    )
                    corrected_chunks.append(correction.corrected_text)

                return '\n\n'.join(corrected_chunks)
            else:
                return raw_text

        except Exception as e:
            logger.error(f"OCR/Correction error: {e}")
            return None

    def _extract_text_directly(self, pdf_path: Path) -> Optional[str]:
        """Extract text directly from text PDF."""
        try:
            import pdfplumber

            text_pages = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_pages.append(text)

            return '\n\n'.join(text_pages) if text_pages else None

        except Exception as e:
            logger.error(f"Direct extraction error: {e}")
            return None

    def _split_text_chunks(self, text: str, max_chunk_size: int = 2000) -> List[str]:
        """Split text into chunks for AI processing."""
        chunks = []
        current_chunk = []
        current_size = 0

        for line in text.split('\n'):
            line_size = len(line)
            if current_size + line_size > max_chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks

    def _save_output(self, pdf_path: Path, text: str, output_dir: Path, analysis) -> Path:
        """Save extracted text with metadata."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save text file
        text_path = output_dir / f"{pdf_path.stem}.txt"
        text_path.write_text(text, encoding='utf-8')

        # Save metadata
        meta_path = output_dir / f"{pdf_path.stem}_meta.json"
        metadata = {
            "source_pdf": str(pdf_path),
            "pdf_type": analysis.pdf_type.value,
            "quality_score": analysis.quality_score,
            "page_count": analysis.page_count,
            "text_pages": analysis.text_pages,
            "image_pages": analysis.image_pages,
            "needs_ocr": analysis.needs_ocr,
            "extraction_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "text_stats": {
                "total_chars": len(text),
                "total_lines": len(text.split('\n')),
                "avg_chars_per_page": len(text) / max(analysis.page_count, 1)
            }
        }
        meta_path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        return text_path

    def batch_process(
        self,
        pdf_dir: Path,
        output_dir: Path,
        force_ocr: bool = False,
        max_workers: int = 4
    ) -> Dict:
        """
        Process multiple PDFs in parallel.

        Args:
            pdf_dir: Directory with PDFs
            output_dir: Output directory
            force_ocr: Force OCR on all
            max_workers: Parallel workers

        Returns:
            Statistics dictionary
        """
        pdf_files = list(pdf_dir.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDFs to process")

        results = []
        stats = {
            "total": len(pdf_files),
            "successful": 0,
            "failed": 0,
            "ocr_performed": 0,
            "ai_corrected": 0,
            "text_pdfs": 0,
            "image_pdfs": 0,
            "mixed_pdfs": 0,
            "total_pages": 0,
            "total_time": 0
        }

        # Process in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self.process_pdf,
                    pdf_path,
                    output_dir,
                    force_ocr
                ): pdf_path
                for pdf_path in pdf_files
            }

            for future in as_completed(futures):
                pdf_path = futures[future]
                try:
                    result = future.result()
                    results.append(result)

                    # Update stats
                    if result.text_extracted:
                        stats["successful"] += 1
                    else:
                        stats["failed"] += 1

                    if result.ocr_performed:
                        stats["ocr_performed"] += 1
                    if result.ai_correction:
                        stats["ai_corrected"] += 1

                    # Count PDF types
                    if result.pdf_type == "text":
                        stats["text_pdfs"] += 1
                    elif result.pdf_type == "image":
                        stats["image_pdfs"] += 1
                    elif result.pdf_type == "mixed":
                        stats["mixed_pdfs"] += 1

                    stats["total_pages"] += result.pages_processed
                    stats["total_time"] += result.processing_time

                    logger.info(f"Processed: {pdf_path.name} - {'✓' if result.text_extracted else '✗'}")

                except Exception as e:
                    logger.error(f"Failed to process {pdf_path.name}: {e}")
                    stats["failed"] += 1

        # Save batch report
        self._save_batch_report(output_dir, results, stats)

        return stats

    def _save_batch_report(self, output_dir: Path, results: List[OCRPipelineResult], stats: Dict):
        """Save detailed batch processing report."""
        report_path = output_dir / "ocr_pipeline_report.json"

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "statistics": stats,
            "results": [asdict(r) for r in results]
        }

        report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
        logger.info(f"Report saved: {report_path}")

    def analyze_library(self, library_dir: Path) -> Dict:
        """
        Analyze entire PDF library without processing.

        Args:
            library_dir: Library directory

        Returns:
            Analysis summary
        """
        pdf_files = list(library_dir.glob("*.pdf"))
        logger.info(f"Analyzing {len(pdf_files)} PDFs...")

        summary = {
            "total_pdfs": len(pdf_files),
            "text_pdfs": [],
            "image_pdfs": [],
            "mixed_pdfs": [],
            "encrypted_pdfs": [],
            "corrupted_pdfs": [],
            "total_pages": 0,
            "pdfs_needing_ocr": 0,
            "average_quality": 0
        }

        quality_scores = []

        for pdf_path in pdf_files:
            try:
                analysis = self.detector.analyze_pdf(pdf_path)

                # Categorize
                if analysis.pdf_type == PDFType.TEXT:
                    summary["text_pdfs"].append(pdf_path.name)
                elif analysis.pdf_type == PDFType.IMAGE:
                    summary["image_pdfs"].append(pdf_path.name)
                elif analysis.pdf_type == PDFType.MIXED:
                    summary["mixed_pdfs"].append(pdf_path.name)
                elif analysis.pdf_type == PDFType.ENCRYPTED:
                    summary["encrypted_pdfs"].append(pdf_path.name)
                elif analysis.pdf_type == PDFType.CORRUPTED:
                    summary["corrupted_pdfs"].append(pdf_path.name)

                if analysis.needs_ocr:
                    summary["pdfs_needing_ocr"] += 1

                summary["total_pages"] += analysis.page_count
                quality_scores.append(analysis.quality_score)

            except Exception as e:
                logger.error(f"Error analyzing {pdf_path.name}: {e}")
                summary["corrupted_pdfs"].append(pdf_path.name)

        # Calculate average quality
        if quality_scores:
            summary["average_quality"] = sum(quality_scores) / len(quality_scores)

        # Print summary
        print("\n" + "="*60)
        print("LIBRARY ANALYSIS SUMMARY")
        print("="*60)
        print(f"Total PDFs: {summary['total_pdfs']}")
        print(f"Text PDFs: {len(summary['text_pdfs'])}")
        print(f"Image PDFs: {len(summary['image_pdfs'])}")
        print(f"Mixed PDFs: {len(summary['mixed_pdfs'])}")
        print(f"Encrypted: {len(summary['encrypted_pdfs'])}")
        print(f"Corrupted: {len(summary['corrupted_pdfs'])}")
        print(f"Need OCR: {summary['pdfs_needing_ocr']}")
        print(f"Total Pages: {summary['total_pages']}")
        print(f"Avg Quality: {summary['average_quality']:.2f}")

        return summary


def main():
    """Test OCR pipeline."""
    print("="*60)
    print("UNIFIED OCR PIPELINE")
    print("="*60)

    pipeline = OCRPipeline(
        language="por+eng",
        use_ai_correction=True,
        ai_model="phi3:mini"
    )

    # Test with library
    library_dir = Path("digilibrary/BIBLIOTECA_ROTEIROS")

    if library_dir.exists():
        print("\nAnalyzing library...")
        summary = pipeline.analyze_library(library_dir)

        # Process a sample
        if summary["image_pdfs"]:
            test_pdf = library_dir / summary["image_pdfs"][0]
            print(f"\nTesting with scanned PDF: {test_pdf.name}")

            output_dir = Path("data/ocr_test")
            result = pipeline.process_pdf(test_pdf, output_dir)

            print(f"\nResult:")
            print(f"  Type: {result.pdf_type}")
            print(f"  OCR: {result.ocr_performed}")
            print(f"  AI: {result.ai_correction}")
            print(f"  Extracted: {result.text_extracted}")
            print(f"  Time: {result.processing_time:.2f}s")

    print("\n" + "="*60)
    print("Pipeline ready!")


if __name__ == "__main__":
    main()