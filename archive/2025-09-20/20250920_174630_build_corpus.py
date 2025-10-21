#!/usr/bin/env python3
"""
Build corpus from screenplay PDFs for TPD training
Extracts text from all PDFs and saves to data/original/
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import PyPDF2
import pdfplumber
from typing import Optional
import re

def extract_text_from_pdf(pdf_path: Path) -> Optional[str]:
    """Extract text from PDF using multiple methods."""
    text = ""

    # Try pdfplumber first (better for complex layouts)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except:
        pass

    # Fallback to PyPDF2
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except:
        pass

    return None

def clean_screenplay_text(text: str) -> str:
    """Clean and normalize screenplay text."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    # Preserve screenplay structure
    lines = text.split('\n')
    cleaned = []

    for line in lines:
        line = line.strip()
        if line:
            # Preserve scene headers
            if any(marker in line.upper() for marker in ['INT.', 'EXT.', 'INT/', 'EXT/']):
                cleaned.append('\n' + line)
            # Preserve character names (all caps)
            elif line.isupper() and len(line.split()) <= 3:
                cleaned.append('\n' + line)
            # Preserve dialogue and action
            else:
                cleaned.append(line)

    return '\n'.join(cleaned)

def build_corpus():
    """Build corpus from all screenplay PDFs."""
    print("="*60)
    print("BUILDING SCREENPLAY CORPUS FOR TPD")
    print("="*60)

    # Setup paths
    pdf_dir = Path("digilibrary/BIBLIOTECA_ROTEIROS")
    corpus_dir = Path("data/original")
    corpus_dir.mkdir(parents=True, exist_ok=True)

    # Find all PDFs
    pdf_files = list(pdf_dir.rglob("*.pdf"))
    print(f"\nFound {len(pdf_files)} PDF files")

    # Process each PDF
    successful = 0
    total_chars = 0

    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing {pdf_path.name}")

        # Extract text
        text = extract_text_from_pdf(pdf_path)

        if text:
            # Clean text
            cleaned = clean_screenplay_text(text)

            # Save to corpus
            output_name = pdf_path.stem.replace(' ', '_') + '.txt'
            output_path = corpus_dir / output_name

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            chars = len(cleaned)
            total_chars += chars
            successful += 1
            print(f"  ✓ Extracted {chars:,} characters")
        else:
            print(f"  ✗ No text extracted")

    # Summary
    print("\n" + "="*60)
    print("CORPUS BUILD COMPLETE")
    print(f"Successful: {successful}/{len(pdf_files)} files")
    print(f"Total size: {total_chars:,} characters")
    print(f"Corpus location: {corpus_dir}")
    print("="*60)

    return corpus_dir

if __name__ == "__main__":
    corpus_dir = build_corpus()
    print(f"\n✓ Corpus ready at: {corpus_dir}")
    print("Next step: Build TPD from corpus")