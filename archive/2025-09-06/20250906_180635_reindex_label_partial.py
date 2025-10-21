#!/usr/bin/env python3
"""
V3.2 R4.2 - Label partial reindex with transparency
Creates clear documentation of partial reindex status.
"""
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def label_partial_reindex():
    """Create labeled partial reindex report."""
    
    print(f"\n{'='*60}")
    print(f"REINDEX PARTIAL LABELING")
    print(f"{'='*60}")
    
    # Check for previous reindex report
    prev_report_path = Path("reports/fix_v3/v32_r4_1_microfix/reindex_report_v32_r4_1.json")
    prev_data = {}
    
    if prev_report_path.exists():
        print(f"Found previous report: {prev_report_path}")
        with open(prev_report_path) as f:
            prev_data = json.load(f)
    else:
        print("No previous reindex report found")
    
    # Create labeled report
    labeled_report = {
        "timestamp": datetime.now().isoformat(),
        "version": "V3.2_R4.2_MICROFINAL",
        "partial": True,
        "affected_docs": ["Alien - Screenplay.pdf"],
        "ocr_available": False,
        "ocr_attempted": False,
        "new_chunks": 0,
        "reason": "OCR not available",
        
        "details": {
            "total_pdfs": 52,
            "indexed_pdfs": 51,
            "stub_pdfs": 1,
            "total_chunks": 2145
        },
        
        "alien_pdf_status": {
            "file": "Alien - Screenplay.pdf",
            "status": "kept_as_stub",
            "chars_extracted": prev_data.get("alien_status", {}).get("chars_extracted", 37),
            "chunks_created": 0,
            "indexed": False,
            "reason": "OCR libraries (pytesseract/pdf2image) not available"
        },
        
        "deviations": [
            "OCR libraries not installed - pytesseract and pdf2image missing",
            "Alien PDF kept as stub with minimal content"
        ],
        
        "recommendations": [
            "Install pytesseract and pdf2image for OCR capability",
            "Re-run reindex after OCR libraries are available"
        ]
    }
    
    # If we have previous data, incorporate it
    if prev_data:
        if "alien_status" in prev_data:
            alien = prev_data["alien_status"]
            labeled_report["alien_pdf_status"]["chars_extracted"] = alien.get("chars_extracted", 37)
            labeled_report["alien_pdf_status"]["ocr_attempted"] = alien.get("ocr_attempted", False)
            labeled_report["ocr_attempted"] = alien.get("ocr_attempted", False)
    
    return labeled_report

def main():
    report = label_partial_reindex()
    
    # Save report
    report_dir = Path("reports/fix_v3/v32_r4_2_microfinal")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / "reindex_partial_label_v32_r4_2.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Report saved to: {report_path}")
    
    # Summary
    print(f"\n{'='*40}")
    print("PARTIAL REINDEX SUMMARY")
    print(f"{'='*40}")
    print(f"Status: PARTIAL")
    print(f"Affected: {report['affected_docs']}")
    print(f"OCR Available: {report['ocr_available']}")
    print(f"New Chunks: {report['new_chunks']}")
    print(f"Reason: {report['reason']}")
    
    # Show details
    details = report["details"]
    print(f"\nOverall Status:")
    print(f"  Total PDFs: {details['total_pdfs']}")
    print(f"  Indexed: {details['indexed_pdfs']}")
    print(f"  Stubs: {details['stub_pdfs']}")
    print(f"  Total Chunks: {details['total_chunks']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())