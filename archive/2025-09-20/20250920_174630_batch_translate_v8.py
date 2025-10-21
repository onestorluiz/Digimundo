#!/usr/bin/env python3
"""
BATCH TRANSLATOR DIGILANG V8.1 SUPREME - FASE 17
================================================
Sistema completo para traduzir toda a digilibrary para DigiLang V8.1 Supreme
com processamento paralelo e relatórios estatísticos detalhados.
"""

import os
import sys
import json
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import multiprocessing as mp

# Imports para extração de texto
try:
    import PyPDF2
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("⚠️ PyPDF2/pdfplumber não disponíveis - PDFs não serão processados")

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

# Importar DigiLang V8.1 Supreme
sys.path.append('/Users/clubproducoes/Digimundo/scripturemon-champion/apps/scripturemon')
try:
    from digilang_v8_1_supreme import DigiLangV8_1Supreme, SupremeStats
    DIGILANG_AVAILABLE = True
except ImportError:
    DIGILANG_AVAILABLE = False
    print("❌ DigiLang V8.1 Supreme não disponível")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BatchTranslateV8")

@dataclass
class FileProcessingResult:
    """Resultado do processamento de um arquivo"""
    file_path: str
    file_type: str
    file_size: int
    original_text_length: int
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    patterns_applied: int
    processing_time: float
    success: bool
    error: Optional[str] = None
    compressed_text: Optional[str] = None
    output_path: Optional[str] = None

@dataclass
class BatchProcessingReport:
    """Relatório consolidado do processamento batch"""
    total_files: int
    processed_files: int
    failed_files: int
    total_original_tokens: int
    total_compressed_tokens: int
    average_compression_ratio: float
    best_compression_file: str
    best_compression_ratio: float
    worst_compression_file: str
    worst_compression_ratio: float
    total_processing_time: float
    total_patterns_applied: int
    files_by_type: Dict[str, int]
    compression_by_type: Dict[str, float]
    processing_start: str
    processing_end: str

class TextExtractor:
    """Classe para extrair texto de diferentes tipos de arquivos"""

    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """Extrai texto de PDF usando pdfplumber como primeira opção"""
        text = ""

        if not PDF_SUPPORT:
            raise ValueError("PDF support not available")

        try:
            # Tentar com pdfplumber primeiro (melhor qualidade)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            if text.strip():
                return text

        except Exception as e:
            logger.warning(f"pdfplumber falhou para {file_path}: {e}")

        try:
            # Fallback para PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"

        except Exception as e:
            logger.error(f"Erro extraindo PDF {file_path}: {e}")
            raise

        return text

    @staticmethod
    def extract_from_txt(file_path: str) -> str:
        """Extrai texto de arquivo TXT"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue

        raise ValueError(f"Não foi possível decodificar {file_path}")

    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """Extrai texto de arquivo DOCX"""
        if not DOCX_SUPPORT:
            raise ValueError("DOCX support not available")

        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

def process_single_file(file_info: Tuple[str, str]) -> FileProcessingResult:
    """Processa um único arquivo (função para paralelização)"""
    file_path, output_dir = file_info
    start_time = time.time()

    try:
        # Obter informações do arquivo
        file_size = os.path.getsize(file_path)
        file_type = Path(file_path).suffix.lower()
        file_name = Path(file_path).name

        # Extrair texto baseado no tipo
        extractor = TextExtractor()

        if file_type == '.pdf':
            text = extractor.extract_from_pdf(file_path)
        elif file_type == '.txt':
            text = extractor.extract_from_txt(file_path)
        elif file_type == '.docx':
            text = extractor.extract_from_docx(file_path)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_type}")

        if not text.strip():
            raise ValueError("Texto extraído está vazio")

        # Inicializar DigiLang V8.1 Supreme
        digilang = DigiLangV8_1Supreme()

        # Comprimir texto
        compressed_text, stats = digilang.encode(text)

        # Salvar versão comprimida
        output_filename = f"{Path(file_name).stem}_digilang_v8.1_supreme.txt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(compressed_text)

        processing_time = time.time() - start_time

        return FileProcessingResult(
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            original_text_length=len(text),
            original_tokens=stats.original_tokens,
            compressed_tokens=stats.compressed_tokens,
            compression_ratio=stats.compression_ratio,
            patterns_applied=stats.patterns_applied,
            processing_time=processing_time,
            success=True,
            compressed_text=compressed_text[:1000] + "..." if len(compressed_text) > 1000 else compressed_text,
            output_path=output_path
        )

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Erro processando {file_path}: {e}")

        return FileProcessingResult(
            file_path=file_path,
            file_type=Path(file_path).suffix.lower(),
            file_size=os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            original_text_length=0,
            original_tokens=0,
            compressed_tokens=0,
            compression_ratio=0.0,
            patterns_applied=0,
            processing_time=processing_time,
            success=False,
            error=str(e)
        )

class BatchTranslatorV8:
    """Sistema batch para traduzir arquivos para DigiLang V8.1 Supreme"""

    def __init__(self, library_path: str, output_path: str):
        self.library_path = Path(library_path)
        self.output_path = Path(output_path)
        # Definir extensões suportadas baseado nas dependências disponíveis
        self.supported_extensions = {'.txt'}
        if PDF_SUPPORT:
            self.supported_extensions.add('.pdf')
        if DOCX_SUPPORT:
            self.supported_extensions.add('.docx')

        # Criar diretório de saída
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Diretório para arquivos comprimidos
        self.compressed_dir = self.output_path / "compressed_files"
        self.compressed_dir.mkdir(exist_ok=True)

        # Diretório para relatórios
        self.reports_dir = self.output_path / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        logger.info(f"✅ BatchTranslator inicializado")
        logger.info(f"   Biblioteca: {self.library_path}")
        logger.info(f"   Output: {self.output_path}")

    def scan_files(self) -> List[str]:
        """Escaneia todos os arquivos suportados na biblioteca"""
        files = []

        for ext in self.supported_extensions:
            pattern = f"**/*{ext}"
            found_files = list(self.library_path.glob(pattern))
            files.extend([str(f) for f in found_files if f.is_file()])

        # Filtrar arquivos DS_Store e outros indesejados
        files = [f for f in files if not Path(f).name.startswith('.')]

        logger.info(f"📁 Encontrados {len(files)} arquivos para processar:")
        for ext in self.supported_extensions:
            count = len([f for f in files if f.endswith(ext)])
            if count > 0:
                logger.info(f"   {ext.upper()}: {count} arquivos")

        return files

    def process_batch(self, max_workers: Optional[int] = None) -> BatchProcessingReport:
        """Processa todos os arquivos em batch com paralelização"""
        start_time = time.time()
        processing_start = datetime.now().isoformat()

        if max_workers is None:
            max_workers = min(mp.cpu_count(), 8)  # Máximo de 8 workers

        logger.info(f"🚀 Iniciando processamento batch com {max_workers} workers")

        files = self.scan_files()
        if not files:
            logger.warning("❌ Nenhum arquivo encontrado para processar")
            return self._create_empty_report(processing_start)

        # Preparar argumentos para paralelização
        file_args = [(file_path, str(self.compressed_dir)) for file_path in files]

        results = []
        completed = 0

        # Processar arquivos em paralelo
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submeter todos os jobs
            future_to_file = {executor.submit(process_single_file, arg): arg[0]
                             for arg in file_args}

            # Coletar resultados conforme completam
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1

                    if result.success:
                        logger.info(f"✅ [{completed}/{len(files)}] {Path(file_path).name} - "
                                  f"{result.compression_ratio:.2f}% compressão")
                    else:
                        logger.error(f"❌ [{completed}/{len(files)}] {Path(file_path).name} - "
                                   f"Erro: {result.error}")

                except Exception as e:
                    logger.error(f"❌ Erro inesperado processando {file_path}: {e}")

        total_time = time.time() - start_time
        processing_end = datetime.now().isoformat()

        # Gerar relatório
        report = self._generate_report(results, total_time, processing_start, processing_end)

        # Salvar relatório
        self._save_report(report)

        return report

    def _generate_report(self, results: List[FileProcessingResult],
                        total_time: float, start_time: str, end_time: str) -> BatchProcessingReport:
        """Gera relatório consolidado"""

        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]

        if not successful_results:
            return self._create_empty_report(start_time, end_time, len(results))

        # Estatísticas gerais
        total_original_tokens = sum(r.original_tokens for r in successful_results)
        total_compressed_tokens = sum(r.compressed_tokens for r in successful_results)
        total_patterns_applied = sum(r.patterns_applied for r in successful_results)

        avg_compression = (sum(r.compression_ratio for r in successful_results) /
                          len(successful_results))

        # Melhores e piores compressões
        best_compression = max(successful_results, key=lambda x: x.compression_ratio)
        worst_compression = min(successful_results, key=lambda x: x.compression_ratio)

        # Estatísticas por tipo de arquivo
        files_by_type = {}
        compression_by_type = {}

        for ext in self.supported_extensions:
            ext_results = [r for r in successful_results if r.file_type == ext]
            if ext_results:
                files_by_type[ext] = len(ext_results)
                compression_by_type[ext] = sum(r.compression_ratio for r in ext_results) / len(ext_results)

        return BatchProcessingReport(
            total_files=len(results),
            processed_files=len(successful_results),
            failed_files=len(failed_results),
            total_original_tokens=total_original_tokens,
            total_compressed_tokens=total_compressed_tokens,
            average_compression_ratio=avg_compression,
            best_compression_file=best_compression.file_path,
            best_compression_ratio=best_compression.compression_ratio,
            worst_compression_file=worst_compression.file_path,
            worst_compression_ratio=worst_compression.compression_ratio,
            total_processing_time=total_time,
            total_patterns_applied=total_patterns_applied,
            files_by_type=files_by_type,
            compression_by_type=compression_by_type,
            processing_start=start_time,
            processing_end=end_time
        )

    def _create_empty_report(self, start_time: str, end_time: str = None, total_files: int = 0) -> BatchProcessingReport:
        """Cria relatório vazio para quando não há arquivos processados"""
        if end_time is None:
            end_time = datetime.now().isoformat()

        return BatchProcessingReport(
            total_files=total_files,
            processed_files=0,
            failed_files=total_files,
            total_original_tokens=0,
            total_compressed_tokens=0,
            average_compression_ratio=0.0,
            best_compression_file="N/A",
            best_compression_ratio=0.0,
            worst_compression_file="N/A",
            worst_compression_ratio=0.0,
            total_processing_time=0.0,
            total_patterns_applied=0,
            files_by_type={},
            compression_by_type={},
            processing_start=start_time,
            processing_end=end_time
        )

    def _save_report(self, report: BatchProcessingReport):
        """Salva relatório em JSON e texto legível"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Salvar JSON
        json_path = self.reports_dir / f"batch_report_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)

        # Salvar relatório legível
        txt_path = self.reports_dir / f"batch_report_{timestamp}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(self._format_report(report))

        logger.info(f"📊 Relatório salvo: {txt_path}")

    def _format_report(self, report: BatchProcessingReport) -> str:
        """Formata relatório para leitura humana"""
        report_text = f"""
DIGILANG V8.1 SUPREME - RELATÓRIO BATCH PROCESSING
================================================
Processamento: {report.processing_start} até {report.processing_end}
Tempo total: {report.total_processing_time:.2f} segundos

📊 ESTATÍSTICAS GERAIS
=====================
Total de arquivos: {report.total_files}
Processados com sucesso: {report.processed_files}
Falhas: {report.failed_files}
Taxa de sucesso: {(report.processed_files/report.total_files*100):.1f}%

🔥 COMPRESSÃO
=============
Tokens originais: {report.total_original_tokens:,}
Tokens comprimidos: {report.total_compressed_tokens:,}
Economia total: {report.total_original_tokens - report.total_compressed_tokens:,} tokens
Taxa média de compressão: {report.average_compression_ratio:.2f}%
Total de padrões aplicados: {report.total_patterns_applied:,}

🏆 MELHORES E PIORES
==================
Melhor compressão: {Path(report.best_compression_file).name} ({report.best_compression_ratio:.2f}%)
Pior compressão: {Path(report.worst_compression_file).name} ({report.worst_compression_ratio:.2f}%)

📁 POR TIPO DE ARQUIVO
=====================
"""

        for file_type, count in report.files_by_type.items():
            avg_compression = report.compression_by_type.get(file_type, 0)
            report_text += f"{file_type.upper()}: {count} arquivos - {avg_compression:.2f}% compressão média\n"

        if report.average_compression_ratio >= 20:
            report_text += f"\n🎯 META ALCANÇADA! Compressão média de {report.average_compression_ratio:.2f}% >= 20%"
        elif report.average_compression_ratio >= 15:
            report_text += f"\n🔄 Próximo da meta: {report.average_compression_ratio:.2f}% (meta: 20%)"
        else:
            report_text += f"\n⚠️ Abaixo da meta: {report.average_compression_ratio:.2f}% (meta: 20%)"

        return report_text

    def print_summary(self, report: BatchProcessingReport):
        """Imprime resumo do processamento"""
        print("\n" + "="*80)
        print("DIGILANG V8.1 SUPREME - BATCH PROCESSING COMPLETO")
        print("="*80)

        print(f"\n📊 RESULTADOS:")
        print(f"  Total de arquivos: {report.total_files}")
        print(f"  Processados: {report.processed_files}")
        print(f"  Falhas: {report.failed_files}")
        print(f"  Tempo total: {report.total_processing_time:.2f}s")

        print(f"\n🔥 COMPRESSÃO:")
        print(f"  Taxa média: {report.average_compression_ratio:.2f}%")
        print(f"  Tokens economizados: {report.total_original_tokens - report.total_compressed_tokens:,}")
        print(f"  Padrões aplicados: {report.total_patterns_applied:,}")

        print(f"\n🏆 DESTAQUES:")
        print(f"  Melhor: {Path(report.best_compression_file).name} ({report.best_compression_ratio:.2f}%)")
        print(f"  Pior: {Path(report.worst_compression_file).name} ({report.worst_compression_ratio:.2f}%)")

        if report.average_compression_ratio >= 20:
            print(f"\n🎯 META ALCANÇADA! ({report.average_compression_ratio:.2f}% >= 20%)")
        else:
            print(f"\n⚠️ Meta não alcançada ({report.average_compression_ratio:.2f}% < 20%)")

        print("="*80)

def main():
    """Função principal"""
    library_path = "/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS"
    output_path = "/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_DIGILANG_V8_SUPREME"

    if not os.path.exists(library_path):
        print(f"❌ Caminho da biblioteca não encontrado: {library_path}")
        return

    # Verificar dependências
    print("🔍 Verificando dependências...")
    if not PDF_SUPPORT:
        print("⚠️ Suporte a PDF limitado - instale PyPDF2 e pdfplumber")
    if not DOCX_SUPPORT:
        print("⚠️ Suporte a DOCX não disponível - instale python-docx")
    if not DIGILANG_AVAILABLE:
        print("❌ DigiLang V8.1 Supreme não disponível")
        return

    print("✅ Dependências OK")

    # Inicializar tradutor
    translator = BatchTranslatorV8(library_path, output_path)

    # Executar processamento batch
    print("\n🚀 Iniciando processamento batch...")
    report = translator.process_batch()

    # Mostrar resumo
    translator.print_summary(report)

    print(f"\n📂 Arquivos salvos em: {output_path}")
    print(f"📊 Relatórios em: {output_path}/reports/")

if __name__ == "__main__":
    main()