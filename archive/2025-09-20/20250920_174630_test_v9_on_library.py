#!/usr/bin/env python3
"""
FASE 17.c - Test DigiLang V9 Academic on Library
Tests adaptive compression on mixed content
"""

import os
import sys
from pathlib import Path
import json
import time

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_v9_academic import DigiLangV9Academic
from apps.scripturemon.digilang_v8_1_supreme import DigiLangV8_1Supreme as DigiLangV8Supreme

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF"""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:50]:  # First 50 pages
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except:
        return None

def test_on_library():
    """Test V9 Academic on the digilibrary"""

    print("="*60)
    print("FASE 17.c - DIGILANG V9 ACADEMIC LIBRARY TEST")
    print("="*60)

    # Initialize encoders
    v9_encoder = DigiLangV9Academic()
    v8_encoder = DigiLangV8Supreme()

    # Test on sample files
    library_path = Path('digilibrary/BIBLIOTECA_ROTEIROS')

    # Select diverse test files
    test_files = [
        # Screenplays
        "The Dark Knight - Release.pdf",
        "Inception - Screenplay.pdf",
        "Interstellar - Draft.pdf",
        # Theory books
        "Story (MacKee).pdf",
        "Save the Cat (Snyder).pdf",
        "The Fundamentals Of Screenwriting.pdf",
    ]

    results = []

    print("\n📚 Testing on selected files...")

    for filename in test_files:
        file_path = None

        # Find the file
        for pdf_file in library_path.glob('**/*.pdf'):
            if filename in pdf_file.name:
                file_path = pdf_file
                break

        if not file_path or not file_path.exists():
            print(f"⚠️ {filename} not found")
            continue

        # Extract text
        text = extract_text_from_pdf(file_path)
        if not text:
            print(f"❌ Could not extract text from {filename}")
            continue

        print(f"\n📄 {filename}")

        # Test V9 Academic
        start_time = time.time()
        v9_compressed, v9_stats = v9_encoder.compress(text)
        v9_time = time.time() - start_time

        # Test V8.1 Supreme
        start_time = time.time()
        v8_compressed, v8_stats = v8_encoder.encode(text)
        v8_time = time.time() - start_time

        # V8.1 returns tuple, extract stats
        v8_compression_ratio = v8_stats[2] if len(v8_stats) > 2 else 0
        v8_replacements = v8_stats[3] if len(v8_stats) > 3 else 0

        # Compare results
        print(f"   Content type: {v9_stats['content_type']}")
        print(f"   V9 Academic: {v9_stats['compression_ratio']:.2%} ({v9_stats['replacements']} replacements)")
        print(f"   V8.1 Supreme: {v8_compression_ratio:.2%} ({v8_replacements} replacements)")

        improvement = v9_stats['compression_ratio'] - v8_compression_ratio
        if improvement > 0:
            print(f"   ✅ V9 better by {improvement:.2%}")
        else:
            print(f"   ❌ V8.1 better by {-improvement:.2%}")

        results.append({
            'file': filename,
            'type': v9_stats['content_type'],
            'v9_compression': v9_stats['compression_ratio'],
            'v8_compression': v8_compression_ratio,
            'improvement': improvement,
            'v9_time': v9_time,
            'v8_time': v8_time
        })

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    screenplay_improvements = [r['improvement'] for r in results if 'screenplay' in r['file'].lower()]
    theory_improvements = [r['improvement'] for r in results if 'story' in r['file'].lower() or 'cat' in r['file'].lower() or 'fundamentals' in r['file'].lower()]

    if screenplay_improvements:
        avg_screenplay = sum(screenplay_improvements) / len(screenplay_improvements)
        print(f"\n📺 Screenplays: V9 {'better' if avg_screenplay > 0 else 'worse'} by {abs(avg_screenplay):.2%} average")

    if theory_improvements:
        avg_theory = sum(theory_improvements) / len(theory_improvements)
        print(f"📚 Theory books: V9 {'better' if avg_theory > 0 else 'worse'} by {abs(avg_theory):.2%} average")

    overall_improvement = sum(r['improvement'] for r in results) / len(results) if results else 0
    print(f"\n🎯 Overall: V9 {'better' if overall_improvement > 0 else 'worse'} by {abs(overall_improvement):.2%} average")

    # Save results
    output_file = Path('docs/FASE_17c_V9_ACADEMIC_RESULTS.json')
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📁 Results saved to: {output_file}")

    return results

if __name__ == "__main__":
    test_on_library()