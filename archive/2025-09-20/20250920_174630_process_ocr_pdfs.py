#!/usr/bin/env python3
"""
OCR Processing Script for Scanned PDFs
Intelligent batch processing with AI correction
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional
import json
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.ocr_pipeline import OCRPipeline
from apps.scripturemon.pdf_detector import PDFDetector, PDFType


def setup_dependencies():
    """Check and install OCR dependencies."""
    print("Checking OCR dependencies...")
    print("="*60)
    
    missing = []
    
    # Check Python packages
    try:
        import pytesseract
        print("✓ pytesseract installed")
    except ImportError:
        print("✗ pytesseract not installed")
        missing.append("pip install pytesseract")
    
    try:
        import pdf2image
        print("✓ pdf2image installed")
    except ImportError:
        print("✗ pdf2image not installed")
        missing.append("pip install pdf2image")
    
    try:
        import pdfplumber
        print("✓ pdfplumber installed")
    except ImportError:
        print("✗ pdfplumber not installed")
        missing.append("pip install pdfplumber")
    
    try:
        import easyocr
        print("✓ easyocr installed")
    except ImportError:
        print("✗ easyocr not installed (optional)")
        missing.append("pip install easyocr")
    
    # Check system dependencies
    import subprocess
    try:
        result = subprocess.run(['which', 'tesseract'], capture_output=True)
        if result.returncode == 0:
            print("✓ Tesseract OCR installed")
        else:
            print("✗ Tesseract OCR not installed")
            missing.append("brew install tesseract")
    except:
        print("✗ Could not check Tesseract")
    
    if missing:
        print("\nTo install missing dependencies:")
        for cmd in missing:
            print(f"  {cmd}")
        return False
    
    print("\n✓ All dependencies installed!")
    return True


def analyze_library(library_paths: List[Path]):
    """Analyze PDFs in library directories."""
    print("\n" + "="*60)
    print("ANALYZING PDF LIBRARY")
    print("="*60)
    
    detector = PDFDetector()
    
    all_pdfs = []
    for path in library_paths:
        if path.is_dir():
            pdfs = list(path.glob("**/*.pdf"))
            all_pdfs.extend(pdfs)
        elif path.suffix == '.pdf':
            all_pdfs.append(path)
    
    print(f"\nFound {len(all_pdfs)} PDFs")
    
    categories = {
        'text': [],
        'image': [],
        'mixed': [],
        'encrypted': [],
        'corrupted': [],
        'empty': []
    }
    
    needs_ocr = []
    
    for pdf_path in all_pdfs:
        try:
            analysis = detector.analyze_pdf(pdf_path)
            
            # Categorize
            if analysis.pdf_type == PDFType.TEXT:
                categories['text'].append(pdf_path)
            elif analysis.pdf_type == PDFType.IMAGE:
                categories['image'].append(pdf_path)
                needs_ocr.append(pdf_path)
            elif analysis.pdf_type == PDFType.MIXED:
                categories['mixed'].append(pdf_path)
                if analysis.needs_ocr:
                    needs_ocr.append(pdf_path)
            elif analysis.pdf_type == PDFType.ENCRYPTED:
                categories['encrypted'].append(pdf_path)
            elif analysis.pdf_type == PDFType.CORRUPTED:
                categories['corrupted'].append(pdf_path)
            elif analysis.pdf_type == PDFType.EMPTY:
                categories['empty'].append(pdf_path)
            
            # Progress indicator
            sys.stdout.write('.')
            sys.stdout.flush()
            
        except Exception as e:
            categories['corrupted'].append(pdf_path)
            sys.stdout.write('x')
            sys.stdout.flush()
    
    print("\n\nAnalysis Results:")
    print("-"*40)
    print(f"Text PDFs: {len(categories['text'])}")
    print(f"Image PDFs (scanned): {len(categories['image'])}")
    print(f"Mixed PDFs: {len(categories['mixed'])}")
    print(f"Encrypted: {len(categories['encrypted'])}")
    print(f"Corrupted: {len(categories['corrupted'])}")
    print(f"Empty: {len(categories['empty'])}")
    print(f"\nNeed OCR: {len(needs_ocr)} PDFs")
    
    if needs_ocr:
        print("\nPDFs requiring OCR:")
        for pdf in needs_ocr[:10]:  # Show first 10
            print(f"  - {pdf.name}")
        if len(needs_ocr) > 10:
            print(f"  ... and {len(needs_ocr) - 10} more")
    
    return categories, needs_ocr


def process_pdfs(
    pdf_paths: List[Path],
    output_dir: Path,
    use_ai: bool = True,
    force_ocr: bool = False,
    max_workers: int = 4
):
    """Process PDFs with OCR."""
    print("\n" + "="*60)
    print("PROCESSING PDFS WITH OCR")
    print("="*60)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize pipeline
    pipeline = OCRPipeline(
        language="por+eng",
        use_ai_correction=use_ai,
        ai_model="phi3:mini",
        parallel_pages=2
    )
    
    print(f"\nProcessing {len(pdf_paths)} PDFs...")
    print(f"Output directory: {output_dir}")
    print(f"AI correction: {'Enabled' if use_ai else 'Disabled'}")
    print(f"Force OCR: {'Yes' if force_ocr else 'No'}")
    print(f"Workers: {max_workers}")
    print("-"*40)
    
    stats = {
        'total': len(pdf_paths),
        'successful': 0,
        'failed': 0,
        'ocr_performed': 0,
        'ai_corrected': 0,
        'total_time': 0
    }
    
    start_time = time.time()
    
    for i, pdf_path in enumerate(pdf_paths):
        print(f"\n[{i+1}/{len(pdf_paths)}] Processing: {pdf_path.name}")
        
        try:
            result = pipeline.process_pdf(
                pdf_path,
                output_dir,
                force_ocr=force_ocr
            )
            
            if result.text_extracted:
                stats['successful'] += 1
                print(f"  ✓ Success ({result.processing_time:.1f}s)")
            else:
                stats['failed'] += 1
                print(f"  ✗ Failed: {result.error}")
            
            if result.ocr_performed:
                stats['ocr_performed'] += 1
            if result.ai_correction:
                stats['ai_corrected'] += 1
            
        except Exception as e:
            stats['failed'] += 1
            print(f"  ✗ Error: {e}")
    
    stats['total_time'] = time.time() - start_time
    
    # Print summary
    print("\n" + "="*60)
    print("PROCESSING COMPLETE")
    print("="*60)
    print(f"Total: {stats['total']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"OCR performed: {stats['ocr_performed']}")
    print(f"AI corrected: {stats['ai_corrected']}")
    print(f"Total time: {stats['total_time']:.1f}s")
    print(f"Avg time/PDF: {stats['total_time']/max(stats['total'], 1):.1f}s")
    
    # Save report
    report_path = output_dir / "processing_report.json"
    with open(report_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"\nReport saved: {report_path}")
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Process scanned PDFs with OCR"
    )
    
    parser.add_argument(
        'command',
        choices=['analyze', 'process', 'install', 'test'],
        help='Command to run'
    )
    
    parser.add_argument(
        '--input',
        type=Path,
        nargs='+',
        help='Input PDF files or directories'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/ocr_extracted'),
        help='Output directory'
    )
    
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI correction'
    )
    
    parser.add_argument(
        '--force-ocr',
        action='store_true',
        help='Force OCR even on text PDFs'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers'
    )
    
    args = parser.parse_args()
    
    if args.command == 'install':
        # Check dependencies
        if setup_dependencies():
            print("\nReady to process PDFs!")
        else:
            print("\nPlease install missing dependencies.")
            sys.exit(1)
    
    elif args.command == 'analyze':
        # Analyze library
        if not args.input:
            # Default paths
            args.input = [
                Path('digilibrary/BIBLIOTECA_ROTEIROS'),
                Path('Pesquisas_Digilab')
            ]
        
        categories, needs_ocr = analyze_library(args.input)
    
    elif args.command == 'process':
        # Process PDFs
        if not args.input:
            print("Error: --input required for process command")
            sys.exit(1)
        
        # Collect PDFs
        pdf_paths = []
        for path in args.input:
            if path.is_dir():
                pdf_paths.extend(path.glob("**/*.pdf"))
            elif path.suffix == '.pdf':
                pdf_paths.append(path)
        
        if not pdf_paths:
            print("No PDFs found!")
            sys.exit(1)
        
        # Process
        stats = process_pdfs(
            pdf_paths,
            args.output,
            use_ai=not args.no_ai,
            force_ocr=args.force_ocr,
            max_workers=args.workers
        )
        
        if stats['failed'] > 0:
            sys.exit(1)
    
    elif args.command == 'test':
        # Quick test
        print("Running OCR test...")
        
        # Find a test PDF
        test_pdfs = [
            Path('digilibrary/BIBLIOTECA_ROTEIROS/meus_filmes/SONHOS SEM LEMBRANÇAS T.3.pdf'),
            Path('Pesquisas_Digilab/Memória Viva em IAs Locais_.pdf')
        ]
        
        test_pdf = None
        for pdf in test_pdfs:
            if pdf.exists():
                test_pdf = pdf
                break
        
        if not test_pdf:
            print("No test PDF found!")
            sys.exit(1)
        
        print(f"Testing with: {test_pdf}")
        
        # Test pipeline
        pipeline = OCRPipeline(
            language="por+eng",
            use_ai_correction=False
        )
        
        output_dir = Path('data/ocr_test')
        result = pipeline.process_pdf(test_pdf, output_dir)
        
        print(f"\nResult:")
        print(f"  Type: {result.pdf_type}")
        print(f"  OCR performed: {result.ocr_performed}")
        print(f"  Text extracted: {result.text_extracted}")
        print(f"  Quality: {result.quality_score:.2f}")
        print(f"  Time: {result.processing_time:.2f}s")
        
        if result.text_extracted and result.output_path:
            print(f"  Output: {result.output_path}")


if __name__ == "__main__":
    main()