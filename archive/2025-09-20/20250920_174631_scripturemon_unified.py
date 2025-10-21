#!/usr/bin/env python3
"""
ScriptureMon Unified System - FASE 12 Integração Robusta
Sistema completo de processamento de roteiros com OCR, normalização e compressão
DIGIMUNDO PRESENTE
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import time
import traceback

# OCR Components
try:
    from .pdf_detector import PDFDetector
    from .ocr_pipeline import OCRPipeline
    from .ocr_ai_corrector import OCRAICorrector
except ImportError:
    PDFDetector = None
    OCRPipeline = None
    OCRAICorrector = None

# DigiLang Components
try:
    from .digilang_v3_ta import DigiLangV3Encoder
    from .screenplay_normalizer import ScreenplayNormalizer
    from .digilang_unified import DigiLangUnified
except ImportError:
    DigiLangV3Encoder = None
    ScreenplayNormalizer = None
    DigiLangUnified = None

# Memory System
try:
    from .memory_system import MemorySystem
except ImportError:
    from .unified_manager import UnifiedMemoryManager as MemorySystem

# Ollama
try:
    from .ollama_core import OllamaCore
except ImportError:
    OllamaCore = None


@dataclass
class ProcessingResult:
    """Resultado do processamento unificado"""
    success: bool
    file_path: Path
    original_size: int = 0
    compressed_size: int = 0
    compression_ratio: float = 0.0
    processing_time: float = 0.0
    ocr_used: bool = False
    normalized: bool = False
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class ScripturemonUnified:
    """
    Sistema Unificado ScriptureMon - FASE 12
    Integra OCR, Normalização, DigiLang e Memória
    """

    def __init__(self, config: Optional[Dict] = None):
        """Inicializa o sistema unificado"""
        self.config = config or {}
        self.logger = self._setup_logger()

        self.logger.info("Initializing ScriptureMon Unified System - FASE 12")

        # Initialize components
        self._init_ocr()
        self._init_digilang()
        self._init_memory()

        # Output directory
        self.output_dir = Path(self.config.get('output_dir', 'output/unified'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Metrics
        self.metrics = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'total_compression': 0.0,
            'best_compression': 0.0,
            'ocr_count': 0,
            'normalized_count': 0
        }

        self.logger.info("ScriptureMon Unified initialized successfully")

    def _setup_logger(self) -> logging.Logger:
        """Configura o sistema de logging"""
        logger = logging.getLogger("ScriptureMon")
        logger.setLevel(logging.INFO)

        # Console handler
        if not logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)

            # File handler
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            fh = logging.FileHandler(
                log_dir / f"scripturemon_{datetime.now().strftime('%Y%m%d')}.log"
            )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        return logger

    def _init_ocr(self):
        """Inicializa componentes OCR"""
        self.ocr_available = False

        if PDFDetector and OCRPipeline and OCRAICorrector:
            try:
                self.pdf_detector = PDFDetector()
                self.ocr_pipeline = OCRPipeline()
                self.ocr_corrector = OCRAICorrector()
                self.ocr_available = True
                self.logger.info("OCR components initialized")
            except Exception as e:
                self.logger.warning(f"OCR initialization failed: {e}")
        else:
            self.logger.warning("OCR components not available")

    def _init_digilang(self):
        """Inicializa componentes DigiLang com estratégia robusta"""
        self.digilang_available = False

        # PRIORITY 1: DigiLangCompressionBridge (7 encoders disponíveis)
        try:
            from apps.scripturemon.digilang_compression_bridge import DigiLangCompressionBridge
            self.digilang_bridge = DigiLangCompressionBridge()

            # Verificar se tem encoders disponíveis
            if hasattr(self.digilang_bridge, 'available_encoders'):
                available_count = len(self.digilang_bridge.available_encoders)
                if available_count > 0:
                    self.digilang_available = True
                    self.logger.info(f"DigiLang CompressionBridge initialized with {available_count} encoders")
                else:
                    self.logger.warning("CompressionBridge sem encoders disponíveis")
            else:
                # Assumir disponível se bridge foi criada
                self.digilang_available = True
                self.logger.info("DigiLang CompressionBridge initialized")

        except Exception as e:
            self.logger.warning(f"DigiLang CompressionBridge failed: {e}")

        # PRIORITY 2: DigiLangUnified (fallback)
        if not self.digilang_available and DigiLangUnified:
            try:
                self.digilang = DigiLangUnified()
                self.digilang_available = True
                self.logger.info("DigiLang Unified initialized")
            except Exception as e:
                self.logger.warning(f"DigiLang Unified failed: {e}")

        # PRIORITY 3: DigiLangV3 (último recurso)
        if not self.digilang_available and DigiLangV3Encoder:
            try:
                self.digilang_v3 = DigiLangV3Encoder()
                self.digilang_available = True
                self.logger.info("DigiLang V3 initialized")
            except Exception as e:
                self.logger.warning(f"DigiLang V3 failed: {e}")

        # Normalizer
        if ScreenplayNormalizer:
            try:
                self.normalizer = ScreenplayNormalizer()
                self.logger.info("Screenplay Normalizer initialized")
            except Exception as e:
                self.logger.warning(f"Normalizer initialization failed: {e}")
                self.normalizer = None
        else:
            self.normalizer = None

    def _init_memory(self):
        """Inicializa sistema de memória"""
        try:
            # Try to use the data directory
            data_dir = Path("data/memory")
            data_dir.mkdir(parents=True, exist_ok=True)
            self.memory = MemorySystem(str(data_dir))
            self.logger.info("Memory system initialized")
        except Exception as e:
            self.logger.warning(f"Memory system initialization failed: {e}")
            self.memory = None

    def process_document(
        self,
        file_path: Path,
        force_ocr: bool = False,
        normalize: bool = True,
        compress: bool = True
    ) -> ProcessingResult:
        """
        Processa um documento através do pipeline completo

        Args:
            file_path: Caminho do arquivo
            force_ocr: Forçar OCR mesmo em PDFs de texto
            normalize: Aplicar normalização PT→EN
            compress: Aplicar compressão DigiLang

        Returns:
            ProcessingResult com métricas e resultado
        """
        start_time = time.time()
        result = ProcessingResult(
            success=False,
            file_path=file_path
        )

        self.logger.info(f"Processing: {file_path.name}")

        try:
            # 1. Extract text
            text = self._extract_text(file_path, force_ocr)
            result.original_size = len(text)
            result.ocr_used = self._was_ocr_used(file_path, force_ocr)

            if result.ocr_used:
                self.metrics['ocr_count'] += 1

            self.logger.info(f"Extracted {len(text)} characters (OCR: {result.ocr_used})")

            # 2. Normalize if requested
            if normalize and self.normalizer:
                normalized = self.normalizer.normalize(text)
                text = normalized.text
                result.normalized = True
                self.metrics['normalized_count'] += 1
                self.logger.info("Text normalized PT→EN")

            # 3. Compress if requested
            if compress and self.digilang_available:
                compressed_data = self._compress_text(text)
                result.compressed_size = len(compressed_data['compressed_text'])
                result.compression_ratio = compressed_data['ratio']
                result.metrics = compressed_data

                # Update best compression
                compression_pct = (1 - result.compression_ratio) * 100
                if compression_pct > self.metrics['best_compression']:
                    self.metrics['best_compression'] = compression_pct

                self.logger.info(f"Compressed to {result.compression_ratio:.1%}")

                # Save compressed
                self._save_compressed(file_path, compressed_data)
            else:
                result.compressed_size = result.original_size
                result.compression_ratio = 1.0

            # 4. Store in memory if available
            if self.memory:
                try:
                    self.memory.store(str(file_path), {
                        'original_size': result.original_size,
                        'compressed_size': result.compressed_size,
                        'ratio': result.compression_ratio,
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    self.logger.debug(f"Memory storage failed: {e}")

            # Update metrics
            self.metrics['total_processed'] += 1
            self.metrics['successful'] += 1

            result.success = True
            result.processing_time = time.time() - start_time

            self.logger.info(
                f"Success: {file_path.name} "
                f"({result.processing_time:.2f}s, "
                f"compression: {(1-result.compression_ratio)*100:.1f}%)"
            )

        except Exception as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            result.errors.append(error_msg)
            result.processing_time = time.time() - start_time
            self.metrics['failed'] += 1
            self.metrics['total_processed'] += 1

        return result

    def _extract_text(self, file_path: Path, force_ocr: bool) -> str:
        """Extrai texto do arquivo"""
        if file_path.suffix.lower() == '.pdf':
            if self.ocr_available and (force_ocr or self._needs_ocr(file_path)):
                # Use OCR
                self.logger.info("Using OCR pipeline")
                ocr_result = self.ocr_pipeline.process_pdf(file_path)

                # AI correction if available
                if self.ocr_corrector:
                    correction = self.ocr_corrector.correct_with_ai(
                        ocr_result.text,
                        context="screenplay"
                    )
                    return correction.text
                else:
                    return ocr_result.text
            else:
                # Extract text directly
                self.logger.info("Extracting text directly from PDF")
                try:
                    import fitz
                    doc = fitz.open(file_path)
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    doc.close()
                    return text
                except ImportError:
                    # Fallback to pdfplumber
                    import pdfplumber
                    text = ""
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                    return text
        else:
            # Read text file
            return file_path.read_text(encoding='utf-8', errors='ignore')

    def _needs_ocr(self, file_path: Path) -> bool:
        """Verifica se o arquivo precisa de OCR"""
        if self.pdf_detector:
            analysis = self.pdf_detector.analyze_pdf(file_path)
            return analysis.needs_ocr
        return False

    def _was_ocr_used(self, file_path: Path, force_ocr: bool) -> bool:
        """Verifica se OCR foi usado"""
        if force_ocr:
            return True
        if file_path.suffix.lower() != '.pdf':
            return False
        return self.ocr_available and self._needs_ocr(file_path)

    def _compress_text(self, text: str) -> Dict[str, Any]:
        """Comprime texto com DigiLang - prioriza CompressionBridge"""

        # PRIORITY 1: DigiLangCompressionBridge
        if hasattr(self, 'digilang_bridge'):
            try:
                # Use compression bridge with default settings
                result = self.digilang_bridge.compress_text(text)
                return {
                    'compressed_text': result.get('compressed_text', text),
                    'ratio': result.get('compression_ratio', 1.0),
                    'original_tokens': result.get('original_tokens', len(text.split())),
                    'compressed_tokens': result.get('compressed_tokens', len(text.split())),
                    'mapping': result.get('metadata', {})
                }
            except Exception as e:
                self.logger.warning(f"CompressionBridge failed: {e}")

        # PRIORITY 2: DigiLangUnified (fallback)
        if hasattr(self, 'digilang'):
            try:
                result = self.digilang.compress(text)
                return {
                    'compressed_text': result.text,
                    'ratio': result.ratio,
                    'original_tokens': result.original_tokens,
                    'compressed_tokens': result.compressed_tokens,
                    'mapping': getattr(result, 'mapping', {})
                }
            except Exception as e:
                self.logger.warning(f"DigiLang Unified failed: {e}")

        # PRIORITY 3: DigiLangV3 (último recurso)
        if hasattr(self, 'digilang_v3'):
            try:
                encoded, mapping, stats, winners = self.digilang_v3.encode(text)
                return {
                    'compressed_text': encoded,
                    'ratio': stats.get('compression_ratio', 1.0),
                    'original_tokens': stats.get('original_tokens', 0),
                    'compressed_tokens': stats.get('compressed_tokens', 0),
                    'mapping': mapping
                }
            except Exception as e:
                self.logger.warning(f"DigiLang V3 failed: {e}")

        # Fallback: sem compressão
        self.logger.warning("No DigiLang encoder available - using raw text")
        return {
            'compressed_text': text,
            'ratio': 1.0,
            'original_tokens': len(text.split()),
            'compressed_tokens': len(text.split()),
            'mapping': {}
        }

    def _save_compressed(self, original_path: Path, compressed_data: Dict):
        """Salva versão comprimida"""
        output_path = self.output_dir / f"{original_path.stem}_compressed.json"

        save_data = {
            'original_file': str(original_path),
            'timestamp': datetime.now().isoformat(),
            'compression_ratio': compressed_data['ratio'],
            'original_tokens': compressed_data.get('original_tokens', 0),
            'compressed_tokens': compressed_data.get('compressed_tokens', 0),
            'compressed_text': compressed_data['compressed_text'][:1000],  # First 1000 chars
            'full_size': len(compressed_data['compressed_text'])
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        self.logger.debug(f"Saved compressed to {output_path}")

    def process_batch(
        self,
        file_paths: List[Path],
        **kwargs
    ) -> Tuple[List[ProcessingResult], Dict[str, Any]]:
        """
        Processa múltiplos documentos

        Args:
            file_paths: Lista de arquivos
            **kwargs: Argumentos para process_document

        Returns:
            Lista de resultados e métricas
        """
        results = []

        self.logger.info(f"Batch processing {len(file_paths)} files")

        for i, file_path in enumerate(file_paths, 1):
            self.logger.info(f"[{i}/{len(file_paths)}] {file_path.name}")
            result = self.process_document(file_path, **kwargs)
            results.append(result)

            # Log progress
            if i % 5 == 0 or i == len(file_paths):
                success_rate = (
                    self.metrics['successful'] / self.metrics['total_processed'] * 100
                    if self.metrics['total_processed'] > 0 else 0
                )
                self.logger.info(
                    f"Progress: {i}/{len(file_paths)} "
                    f"(Success rate: {success_rate:.1f}%, "
                    f"Best compression: {self.metrics['best_compression']:.1f}%)"
                )

        # Calculate average compression
        if self.metrics['successful'] > 0:
            total_compression = sum(
                (1 - r.compression_ratio) * 100
                for r in results if r.success and r.compression_ratio < 1.0
            )
            compressed_count = sum(
                1 for r in results if r.success and r.compression_ratio < 1.0
            )
            if compressed_count > 0:
                self.metrics['average_compression'] = total_compression / compressed_count
            else:
                self.metrics['average_compression'] = 0.0

        return results, self.metrics

    def get_status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        return {
            'timestamp': datetime.now().isoformat(),
            'components': {
                'ocr': self.ocr_available,
                'digilang': self.digilang_available,
                'normalizer': self.normalizer is not None,
                'memory': self.memory is not None
            },
            'metrics': self.metrics,
            'config': self.config
        }

    def save_report(self, output_path: Optional[Path] = None) -> Path:
        """Salva relatório de processamento"""
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.output_dir / f"report_{timestamp}.json"

        report = self.get_status()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Report saved to {output_path}")
        return output_path

    def list_available_pdfs(self) -> List[Path]:
        """Lista todos os PDFs disponíveis no diretório de dados"""
        pdf_dirs = [
            Path("data/pdfs"),
            Path("data/pdf"),
            Path("data/compressed"),
            Path("data/normalized"),
            Path("output")
        ]

        pdf_files = []
        for pdf_dir in pdf_dirs:
            if pdf_dir.exists():
                # Busca PDFs em qualquer subdiretório
                pdf_files.extend(pdf_dir.rglob("*.pdf"))
                pdf_files.extend(pdf_dir.rglob("*.PDF"))

        # Remove duplicatas e ordena
        pdf_files = sorted(set(pdf_files))

        self.logger.info(f"Found {len(pdf_files)} PDF files")
        return pdf_files


def main():
    """Teste do sistema unificado"""
    import sys

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("\n" + "="*60)
    print("SCRIPTUREMON UNIFIED - FASE 12 TEST")
    print("="*60 + "\n")

    # Create unified system
    system = ScripturemonUnified()

    # Show status
    status = system.get_status()
    print("System Components:")
    for component, available in status['components'].items():
        status_icon = "✅" if available else "❌"
        print(f"  {status_icon} {component}")
    print()

    # Test with sample files
    test_dir = Path("digilibrary/BIBLIOTECA_DIGILANG/DIGILANG_ROTEIROS")

    if test_dir.exists():
        # Get test files
        pdf_files = list(test_dir.glob("*.pdf"))[:3]
        txt_files = list(test_dir.glob("*.txt"))[:2]
        test_files = pdf_files + txt_files

        if test_files:
            print(f"Testing with {len(test_files)} files...\n")

            # Process batch
            results, metrics = system.process_batch(
                test_files,
                normalize=True,
                compress=True
            )

            # Show results
            print("\n" + "="*60)
            print("RESULTS")
            print("="*60 + "\n")

            for result in results:
                status = "✅" if result.success else "❌"
                print(f"{status} {result.file_path.name}")

                if result.success:
                    compression = (1 - result.compression_ratio) * 100
                    print(f"   Compression: {compression:.1f}%")
                    print(f"   Time: {result.processing_time:.2f}s")
                    if result.ocr_used:
                        print("   OCR: Used")
                    if result.normalized:
                        print("   Normalized: Yes")
                else:
                    print(f"   Error: {', '.join(result.errors)}")
                print()

            # Show metrics
            print("="*60)
            print("METRICS")
            print("="*60 + "\n")
            print(f"Total processed: {metrics['total_processed']}")
            print(f"Successful: {metrics['successful']}")
            print(f"Failed: {metrics['failed']}")

            if metrics['successful'] > 0:
                success_rate = metrics['successful'] / metrics['total_processed'] * 100
                print(f"Success rate: {success_rate:.1f}%")

                if 'average_compression' in metrics:
                    print(f"Average compression: {metrics['average_compression']:.1f}%")
                print(f"Best compression: {metrics['best_compression']:.1f}%")

                if metrics['ocr_count'] > 0:
                    ocr_usage = metrics['ocr_count'] / metrics['successful'] * 100
                    print(f"OCR usage: {ocr_usage:.1f}%")

                if metrics['normalized_count'] > 0:
                    norm_usage = metrics['normalized_count'] / metrics['successful'] * 100
                    print(f"Normalization usage: {norm_usage:.1f}%")

            # Save report
            report_path = system.save_report()
            print(f"\nReport saved to: {report_path}")
        else:
            print("No test files found")
    else:
        print(f"Test directory not found: {test_dir}")

    print("\nDIGIMUNDO PRESENTE")
    return 0


if __name__ == "__main__":
    sys.exit(main())