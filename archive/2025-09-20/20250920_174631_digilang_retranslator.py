#!/usr/bin/env python3
"""
DigiLang Retranslator - Reprocess all PDFs with advanced compression
Uses the new token-aware DigiLang system for better compression
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# PDF processing
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

# Import DigiLang manager
from .digilang_manager import get_digilang_manager, DigiLangManager
from .digilang_advanced import DigiLangEncoder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DigiLangRetranslator:
    """Retranslate all PDFs with advanced DigiLang compression."""

    def __init__(self,
                 source_dir: Path = None,
                 target_dir: Path = None,
                 mode: str = "advanced"):
        """
        Initialize retranslator.

        Args:
            source_dir: Directory with original PDFs
            target_dir: Directory for DigiLang translations
            mode: Compression mode (simple/advanced/auto)
        """
        self.source_dir = source_dir or Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")
        self.target_dir = target_dir or Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_DIGILANG_V2")

        # Create target directory
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Initialize DigiLang manager
        self.manager = get_digilang_manager(mode=mode)

        # Statistics
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'total_original_chars': 0,
            'total_compressed_chars': 0,
            'total_original_tokens': 0,
            'total_compressed_tokens': 0,
            'best_compression': 0.0,
            'worst_compression': 1.0,
            'average_compression': 0.0,
            'files_processed': []
        }

    def extract_pdf_text(self, pdf_path: Path) -> Optional[str]:
        """Extract text from PDF file."""
        try:
            # Try pdfplumber first (better for complex layouts)
            if pdfplumber:
                with pdfplumber.open(pdf_path) as pdf:
                    text_parts = []
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    return "\n\n".join(text_parts) if text_parts else None

            # Fallback to PyPDF2
            elif PyPDF2:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text_parts = []
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            text_parts.append(text)
                    return "\n\n".join(text_parts) if text_parts else None

            else:
                logger.error("No PDF library available (install pdfplumber or PyPDF2)")
                return None

        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {e}")
            return None

    def retranslate_file(self, pdf_path: Path) -> Dict[str, any]:
        """
        Retranslate a single PDF with advanced compression.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Translation result dictionary
        """
        result = {
            'source': str(pdf_path),
            'status': 'pending',
            'original_size': 0,
            'compressed_size': 0,
            'original_tokens': 0,
            'compressed_tokens': 0,
            'compression_ratio': 0.0,
            'method': None,
            'error': None
        }

        try:
            # Extract text
            logger.info(f"Extracting text from {pdf_path.name}")
            text = self.extract_pdf_text(pdf_path)

            if not text:
                result['status'] = 'failed'
                result['error'] = 'No text extracted'
                return result

            result['original_size'] = len(text)

            # Compress with advanced DigiLang
            logger.info(f"Compressing {pdf_path.name} with {self.manager.mode} mode")
            compression_result = self.manager.compress(text)

            result['compressed_size'] = len(compression_result.compressed_text)
            result['original_tokens'] = compression_result.original_tokens
            result['compressed_tokens'] = compression_result.compressed_tokens
            result['compression_ratio'] = compression_result.compression_ratio
            result['method'] = compression_result.method_used

            # Save compressed version preserving directory structure
            relative_path = pdf_path.relative_to(self.source_dir)
            output_dir = self.target_dir / relative_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)

            output_name = pdf_path.stem + ".dlg"
            output_path = output_dir / output_name

            # Create metadata
            metadata = {
                'original_file': pdf_path.name,
                'translation_date': datetime.now().isoformat(),
                'digilang_version': '2.0.0',
                'compression_method': compression_result.method_used,
                'original_chars': len(text),
                'compressed_chars': len(compression_result.compressed_text),
                'original_tokens': compression_result.original_tokens,
                'compressed_tokens': compression_result.compressed_tokens,
                'compression_ratio': compression_result.compression_ratio,
                'reversible': True,
                'canonicalized': compression_result.metadata.get('canonicalized', False),
                'has_tiktoken': compression_result.metadata.get('has_tiktoken', False)
            }

            # Save compressed text and metadata
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(compression_result.compressed_text)

            metadata_path = output_dir / (pdf_path.stem + ".meta.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            result['status'] = 'success'
            result['output'] = str(output_path)

            logger.info(f"✓ {pdf_path.name}: {compression_result.compression_ratio:.1%} compression")

        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            logger.error(f"✗ {pdf_path.name}: {e}")

        return result

    def retranslate_all(self) -> Dict[str, any]:
        """
        Retranslate all PDFs in source directory.

        Returns:
            Summary statistics
        """
        logger.info(f"\n{'='*60}")
        logger.info("DIGILANG RETRANSLATION - ADVANCED MODE")
        logger.info(f"{'='*60}")
        logger.info(f"Source: {self.source_dir}")
        logger.info(f"Target: {self.target_dir}")
        logger.info(f"Mode: {self.manager.mode}")
        logger.info(f"Has tiktoken: {self.manager.has_advanced}")
        logger.info(f"{'='*60}\n")

        # Find all PDFs recursively
        pdf_files = sorted(self.source_dir.rglob("*.pdf"))
        self.stats['total_files'] = len(pdf_files)

        logger.info(f"Found {len(pdf_files)} PDF files to process\n")

        # Process each file
        for i, pdf_path in enumerate(pdf_files, 1):
            logger.info(f"[{i}/{len(pdf_files)}] Processing {pdf_path.name}")

            result = self.retranslate_file(pdf_path)

            # Update statistics
            if result['status'] == 'success':
                self.stats['successful'] += 1
                self.stats['total_original_chars'] += result['original_size']
                self.stats['total_compressed_chars'] += result['compressed_size']
                self.stats['total_original_tokens'] += result['original_tokens']
                self.stats['total_compressed_tokens'] += result['compressed_tokens']

                if result['compression_ratio'] > self.stats['best_compression']:
                    self.stats['best_compression'] = result['compression_ratio']
                if result['compression_ratio'] < self.stats['worst_compression']:
                    self.stats['worst_compression'] = result['compression_ratio']

                self.stats['files_processed'].append({
                    'file': pdf_path.name,
                    'ratio': result['compression_ratio'],
                    'method': result['method']
                })
            else:
                self.stats['failed'] += 1
                logger.warning(f"Failed: {result['error']}")

        # Calculate averages
        if self.stats['successful'] > 0:
            self.stats['average_compression'] = sum(
                f['ratio'] for f in self.stats['files_processed']
            ) / self.stats['successful']

            self.stats['overall_char_compression'] = 1 - (
                self.stats['total_compressed_chars'] /
                self.stats['total_original_chars']
            )

            if self.stats['total_original_tokens'] > 0:
                self.stats['overall_token_compression'] = 1 - (
                    self.stats['total_compressed_tokens'] /
                    self.stats['total_original_tokens']
                )
            else:
                self.stats['overall_token_compression'] = 0

        # Print summary
        self._print_summary()

        # Save statistics
        stats_path = self.target_dir / "retranslation_stats.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

        return self.stats

    def _print_summary(self):
        """Print retranslation summary."""
        logger.info(f"\n{'='*60}")
        logger.info("RETRANSLATION SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total files: {self.stats['total_files']}")
        logger.info(f"Successful: {self.stats['successful']}")
        logger.info(f"Failed: {self.stats['failed']}")
        logger.info(f"{'='*60}")

        if self.stats['successful'] > 0:
            logger.info("COMPRESSION STATISTICS:")
            logger.info(f"Average compression: {self.stats['average_compression']:.2%}")
            logger.info(f"Best compression: {self.stats['best_compression']:.2%}")
            logger.info(f"Worst compression: {self.stats['worst_compression']:.2%}")
            logger.info(f"{'='*60}")
            logger.info("OVERALL REDUCTION:")
            logger.info(f"Characters: {self.stats['overall_char_compression']:.2%}")
            logger.info(f"Tokens: {self.stats['overall_token_compression']:.2%}")
            logger.info(f"Total chars saved: {self.stats['total_original_chars'] - self.stats['total_compressed_chars']:,}")
            logger.info(f"Total tokens saved: {self.stats['total_original_tokens'] - self.stats['total_compressed_tokens']:,}")
            logger.info(f"{'='*60}")

            # Top 5 best compressions
            sorted_files = sorted(
                self.stats['files_processed'],
                key=lambda x: x['ratio'],
                reverse=True
            )[:5]

            logger.info("TOP 5 BEST COMPRESSIONS:")
            for f in sorted_files:
                logger.info(f"  {f['ratio']:5.1%} - {f['file'][:40]} ({f['method']})")

        logger.info(f"{'='*60}\n")

    def compare_versions(self):
        """Compare old vs new DigiLang translations."""
        old_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_DIGILANG")

        if not old_dir.exists():
            logger.warning("Old DigiLang directory not found for comparison")
            return

        logger.info(f"\n{'='*60}")
        logger.info("VERSION COMPARISON: OLD vs NEW")
        logger.info(f"{'='*60}")

        comparison = []

        for new_file in self.target_dir.glob("*.dlg"):
            old_file = old_dir / new_file.name

            if old_file.exists():
                old_size = old_file.stat().st_size
                new_size = new_file.stat().st_size

                improvement = 1 - (new_size / old_size)

                comparison.append({
                    'file': new_file.name,
                    'old_size': old_size,
                    'new_size': new_size,
                    'improvement': improvement
                })

        if comparison:
            avg_improvement = sum(c['improvement'] for c in comparison) / len(comparison)

            logger.info(f"Files compared: {len(comparison)}")
            logger.info(f"Average improvement: {avg_improvement:.2%}")

            # Show top improvements
            sorted_comp = sorted(comparison, key=lambda x: x['improvement'], reverse=True)[:5]
            logger.info("\nTOP 5 IMPROVEMENTS:")
            for c in sorted_comp:
                logger.info(f"  {c['improvement']:5.1%} - {c['file'][:40]}")

        logger.info(f"{'='*60}\n")


def main():
    """Run retranslation."""
    retranslator = DigiLangRetranslator(mode="advanced")

    # Retranslate all files
    stats = retranslator.retranslate_all()

    # Compare with old version
    retranslator.compare_versions()

    # Report manager statistics
    manager_stats = retranslator.manager.get_statistics()
    logger.info("DIGILANG MANAGER STATISTICS:")
    logger.info(f"  Cache hits: {manager_stats['cache_hits']}")
    logger.info(f"  Simple compressions: {manager_stats['simple_count']}")
    logger.info(f"  Advanced compressions: {manager_stats['advanced_count']}")

    return stats['failed'] == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)