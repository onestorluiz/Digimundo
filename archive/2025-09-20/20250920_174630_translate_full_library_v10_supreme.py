#!/usr/bin/env python3
"""
FASE 18 - DigiLang V10 SUPREME - Tradução Completa da Biblioteca
Sistema ScriptureMon Champion

Assinado: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion
Data: 14/09/2025
"""

import sys
from pathlib import Path
import json
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from apps.scripturemon.digilang_v10_supreme import DigiLangV10Supreme
from apps.scripturemon.pdf_detector import PDFDetector

@dataclass
class TranslationResult:
    """Resultado de tradução de um arquivo"""
    file_path: str
    success: bool
    original_chars: int = 0
    compressed_chars: int = 0
    original_tokens: int = 0
    compressed_tokens: int = 0
    char_compression: float = 0.0
    token_compression: float = 0.0
    execution_time: float = 0.0
    error: Optional[str] = None

class DigiLangV10LibraryTranslator:
    """Tradutor completo da biblioteca com DigiLang V10 Supreme"""

    def __init__(self, base_path: str = "./digilibrary"):
        """
        Inicializar tradutor

        Args:
            base_path: Caminho base da digilibrary
        """
        self.base_path = Path(base_path)
        self.output_path = Path("./output/v10_supreme")
        self.detector = PDFDetector()

        # Criar diretórios de saída
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Estatísticas globais
        self.global_stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'total_original_chars': 0,
            'total_compressed_chars': 0,
            'total_original_tokens': 0,
            'total_compressed_tokens': 0,
            'total_execution_time': 0.0,
            'best_compression': 0.0,
            'worst_compression': 100.0,
            'average_compression': 0.0
        }

    def find_pdf_files(self) -> List[Path]:
        """Encontrar todos arquivos PDF na biblioteca"""
        if not self.base_path.exists():
            logger.error(f"Diretório {self.base_path} não existe!")
            return []

        pdf_files = list(self.base_path.rglob("*.pdf"))
        logger.info(f"📚 Encontrados {len(pdf_files)} arquivos PDF")

        return pdf_files

    def translate_single_pdf(self, pdf_path: Path) -> TranslationResult:
        """
        Traduzir um único PDF

        Args:
            pdf_path: Caminho para o PDF

        Returns:
            TranslationResult com informações da tradução
        """
        start_time = time.time()

        try:
            logger.info(f"🔄 Processando: {pdf_path.name}")

            # Inicializar V10 Supreme
            v10 = DigiLangV10Supreme()

            # Processar PDF
            result = v10.process_pdf(str(pdf_path))

            if not result:
                return TranslationResult(
                    file_path=str(pdf_path),
                    success=False,
                    execution_time=time.time() - start_time,
                    error="Falha no processamento V10"
                )

            # Extrair estatísticas
            stats = result.get('stats', {})

            # Calcular tempo de execução
            execution_time = time.time() - start_time

            # Salvar resultado
            output_file = self.output_path / f"{pdf_path.stem}_v10_supreme.json"

            # Dados completos para salvamento
            save_data = {
                'version': 'V10 Supreme',
                'source_file': str(pdf_path),
                'processed_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'execution_time': execution_time,
                'statistics': stats,
                'compressed_content': result.get('compressed_text', ''),
                'dictionary': result.get('dictionary', {}),
                'signature': 'Nestor Luiz, CEO - Digimundo/ScriptureMon Champion'
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ {pdf_path.name}: {stats.get('token_compression', 0):.2f}% compressão")

            return TranslationResult(
                file_path=str(pdf_path),
                success=True,
                original_chars=stats.get('original_chars', 0),
                compressed_chars=stats.get('compressed_chars', 0),
                original_tokens=stats.get('original_tokens', 0),
                compressed_tokens=stats.get('compressed_tokens', 0),
                char_compression=stats.get('char_compression', 0.0),
                token_compression=stats.get('token_compression', 0.0),
                execution_time=execution_time
            )

        except Exception as e:
            error_msg = f"Erro processando {pdf_path.name}: {str(e)}"
            logger.error(error_msg)

            return TranslationResult(
                file_path=str(pdf_path),
                success=False,
                execution_time=time.time() - start_time,
                error=error_msg
            )

    def translate_all(self) -> Dict:
        """
        Traduzir toda a biblioteca

        Returns:
            Estatísticas finais da tradução
        """
        logger.info("🚀 INICIANDO TRADUÇÃO COMPLETA - DigiLang V10 Supreme")
        logger.info("=" * 60)

        # Encontrar PDFs
        pdf_files = self.find_pdf_files()
        if not pdf_files:
            logger.error("❌ Nenhum PDF encontrado!")
            return self.global_stats

        self.global_stats['total_files'] = len(pdf_files)

        # Lista para resultados detalhados
        detailed_results = []

        # Processar cada PDF
        for i, pdf_path in enumerate(pdf_files, 1):
            logger.info(f"📄 [{i}/{len(pdf_files)}] {pdf_path.name}")

            result = self.translate_single_pdf(pdf_path)
            detailed_results.append(result)

            # Atualizar estatísticas globais
            if result.success:
                self.global_stats['successful'] += 1
                self.global_stats['total_original_chars'] += result.original_chars
                self.global_stats['total_compressed_chars'] += result.compressed_chars
                self.global_stats['total_original_tokens'] += result.original_tokens
                self.global_stats['total_compressed_tokens'] += result.compressed_tokens
                self.global_stats['total_execution_time'] += result.execution_time

                # Atualizar melhor/pior compressão
                if result.token_compression > self.global_stats['best_compression']:
                    self.global_stats['best_compression'] = result.token_compression
                if result.token_compression < self.global_stats['worst_compression']:
                    self.global_stats['worst_compression'] = result.token_compression
            else:
                self.global_stats['failed'] += 1

        # Calcular compressão média
        if self.global_stats['successful'] > 0:
            if self.global_stats['total_original_tokens'] > 0:
                total_saved = self.global_stats['total_original_tokens'] - self.global_stats['total_compressed_tokens']
                self.global_stats['average_compression'] = (total_saved / self.global_stats['total_original_tokens']) * 100

        # Salvar relatório final
        self.save_final_report(detailed_results)

        return self.global_stats

    def save_final_report(self, detailed_results: List[TranslationResult]):
        """Salvar relatório final detalhado"""

        # Preparar dados do relatório
        report_data = {
            'project': 'FASE 18 - DigiLang V10 Supreme Library Translation',
            'version': 'V10 Supreme',
            'processed_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'signature': 'Nestor Luiz, CEO - Digimundo/ScriptureMon Champion',
            'global_statistics': self.global_stats,
            'detailed_results': []
        }

        # Adicionar resultados detalhados
        for result in detailed_results:
            report_data['detailed_results'].append({
                'file_path': result.file_path,
                'success': result.success,
                'statistics': {
                    'original_chars': result.original_chars,
                    'compressed_chars': result.compressed_chars,
                    'original_tokens': result.original_tokens,
                    'compressed_tokens': result.compressed_tokens,
                    'char_compression': result.char_compression,
                    'token_compression': result.token_compression,
                    'execution_time': result.execution_time
                },
                'error': result.error
            })

        # Salvar relatório
        report_file = self.output_path / 'FASE_18_V10_SUPREME_FINAL_REPORT.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        logger.info(f"📊 Relatório salvo: {report_file}")

def main():
    """Função principal"""
    print("🌟 FASE 18 - DigiLang V10 SUPREME")
    print("Tradução Completa da Biblioteca")
    print("=" * 50)
    print("Assinado: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion")
    print()

    # Inicializar tradutor
    translator = DigiLangV10LibraryTranslator()

    # Executar tradução completa
    final_stats = translator.translate_all()

    # Mostrar resultados finais
    print("\n" + "=" * 60)
    print("📊 RESULTADOS FINAIS - V10 SUPREME")
    print("=" * 60)
    print(f"📁 Arquivos processados: {final_stats['successful']}/{final_stats['total_files']}")
    print(f"❌ Falhas: {final_stats['failed']}")

    if final_stats['successful'] > 0:
        print(f"💾 Compressão média: {final_stats['average_compression']:.2f}%")
        print(f"🏆 Melhor compressão: {final_stats['best_compression']:.2f}%")
        print(f"📉 Pior compressão: {final_stats['worst_compression']:.2f}%")
        print(f"🔢 Tokens economizados: {final_stats['total_original_tokens'] - final_stats['total_compressed_tokens']:,}")
        print(f"⏱️ Tempo total: {final_stats['total_execution_time']:.2f}s")

    print("\n✅ TRADUÇÃO V10 SUPREME CONCLUÍDA!")

    return 0 if final_stats['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())