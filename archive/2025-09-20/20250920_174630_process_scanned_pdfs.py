#!/usr/bin/env python3
"""
Process scanned PDFs with OCR
Extract text from image-based PDFs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.ocr_reader import OCRReader
import typer
from rich.console import Console
from rich.progress import track
from rich.table import Table
from typing import Optional

app = typer.Typer()
console = Console()

@app.command()
def process(
    input_dir: str = typer.Argument("digilibrary/BIBLIOTECA_ROTEIROS", help="Directory with PDFs"),
    output_dir: str = typer.Option("data/ocr_extracted", help="Output directory"),
    language: str = typer.Option("por+eng", help="OCR language(s)"),
    engine: str = typer.Option("auto", help="OCR engine: auto, tesseract, easyocr, paddle"),
    limit: Optional[int] = typer.Option(None, help="Process only first N PDFs")
):
    """Process scanned PDFs with OCR to extract text."""

    console.print("[bold cyan]📚 OCR PDF PROCESSOR[/bold cyan]")
    console.print("="*60)

    # Setup paths
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        console.print(f"[red]❌ Input directory not found: {input_path}[/red]")
        raise typer.Exit(1)

    # Initialize OCR reader
    console.print(f"\n[yellow]Initializing OCR reader...[/yellow]")
    reader = OCRReader(language=language)

    # Show available engines
    console.print("\n[bold]Available OCR Engines:[/bold]")
    table = Table()
    table.add_column("Engine", style="cyan")
    table.add_column("Status", style="green")

    for eng, available in reader.ocr_available.items():
        status = "✓ Available" if available else "✗ Not installed"
        table.add_row(eng.capitalize(), status)

    console.print(table)

    # Find PDFs
    pdf_files = list(input_path.rglob("*.pdf"))
    if limit:
        pdf_files = pdf_files[:limit]

    console.print(f"\n[bold]Found {len(pdf_files)} PDFs to process[/bold]")

    # Process each PDF
    output_path.mkdir(parents=True, exist_ok=True)

    stats = {
        'successful': 0,
        'failed': 0,
        'total_chars': 0,
        'files': []
    }

    for pdf_path in track(pdf_files, description="Processing PDFs..."):
        try:
            console.print(f"\n[cyan]Processing: {pdf_path.name}[/cyan]")

            # Extract text with OCR
            text = reader.extract_text_from_pdf(pdf_path, engine=engine)

            if text and len(text) > 100:  # Minimum 100 chars to be valid
                # Save extracted text
                output_file = output_path / f"{pdf_path.stem}_ocr.txt"
                output_file.write_text(text, encoding='utf-8')

                chars = len(text)
                stats['successful'] += 1
                stats['total_chars'] += chars
                stats['files'].append({
                    'name': pdf_path.name,
                    'chars': chars,
                    'output': output_file.name
                })

                console.print(f"  [green]✓ Extracted {chars:,} characters[/green]")
            else:
                stats['failed'] += 1
                console.print(f"  [red]✗ No text extracted or too short[/red]")

        except Exception as e:
            stats['failed'] += 1
            console.print(f"  [red]✗ Error: {e}[/red]")

    # Show summary
    console.print("\n" + "="*60)
    console.print("[bold green]PROCESSING COMPLETE[/bold green]")
    console.print(f"✓ Successful: {stats['successful']}")
    console.print(f"✗ Failed: {stats['failed']}")
    console.print(f"📝 Total characters extracted: {stats['total_chars']:,}")
    console.print(f"📁 Output directory: {output_path}")

    # Show top files by size
    if stats['files']:
        console.print("\n[bold]Top 5 largest extractions:[/bold]")
        top_files = sorted(stats['files'], key=lambda x: x['chars'], reverse=True)[:5]
        for f in top_files:
            console.print(f"  • {f['name']}: {f['chars']:,} chars")

    console.print("="*60)

@app.command()
def test():
    """Test OCR with a sample PDF."""
    console.print("[bold cyan]🔍 OCR TEST MODE[/bold cyan]")
    console.print("="*60)

    # Find a test PDF
    test_pdfs = [
        "digilibrary/BIBLIOTECA_ROTEIROS/SONHOS SEM LEMBRANÇAS T.3.pdf",
        "digilibrary/BIBLIOTECA_ROTEIROS/Alien - Screenplay.pdf",
        "digilibrary/BIBLIOTECA_ROTEIROS/films/The Matrix - Screenplay.pdf"
    ]

    test_pdf = None
    for pdf in test_pdfs:
        if Path(pdf).exists():
            test_pdf = Path(pdf)
            break

    if not test_pdf:
        console.print("[red]No test PDF found![/red]")
        raise typer.Exit(1)

    console.print(f"\n[yellow]Testing with: {test_pdf.name}[/yellow]")

    # Initialize reader
    reader = OCRReader(language='por+eng')

    # Test each engine
    engines = ['tesseract', 'easyocr', 'paddle']

    for engine in engines:
        if reader.ocr_available.get(engine, False):
            console.print(f"\n[cyan]Testing {engine}...[/cyan]")

            try:
                text = reader.extract_text_from_pdf(test_pdf, engine=engine)

                if text:
                    console.print(f"  [green]✓ Extracted {len(text):,} characters[/green]")
                    console.print(f"\n[dim]First 200 chars:[/dim]")
                    console.print(text[:200])
                else:
                    console.print(f"  [red]✗ No text extracted[/red]")

            except Exception as e:
                console.print(f"  [red]✗ Error: {e}[/red]")
        else:
            console.print(f"\n[yellow]{engine} not available - skipping[/yellow]")

    console.print("\n" + "="*60)
    console.print("[green]Test complete![/green]")

@app.command()
def install():
    """Install OCR dependencies."""
    console.print("[bold cyan]📦 INSTALLING OCR DEPENDENCIES[/bold cyan]")
    console.print("="*60)

    import subprocess

    # Python packages
    packages = [
        "pytesseract",
        "pdf2image",
        "Pillow",
        "opencv-python",
        "easyocr"
    ]

    console.print("\n[yellow]Installing Python packages...[/yellow]")
    for package in packages:
        console.print(f"  Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package],
                         capture_output=True, check=True)
            console.print(f"    [green]✓ {package} installed[/green]")
        except:
            console.print(f"    [red]✗ {package} failed[/red]")

    # System dependencies
    console.print("\n[yellow]System dependencies needed:[/yellow]")
    console.print("  • Tesseract: brew install tesseract")
    console.print("  • Tesseract Portuguese: brew install tesseract-lang")
    console.print("  • Poppler (for pdf2image): brew install poppler")

    console.print("\n" + "="*60)
    console.print("[green]Installation complete![/green]")
    console.print("Run 'python scripts/process_scanned_pdfs.py test' to verify")

if __name__ == "__main__":
    app()