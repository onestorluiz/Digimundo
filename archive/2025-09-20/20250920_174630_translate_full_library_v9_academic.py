#!/usr/bin/env python3
"""
FASE 17.f - Tradução Completa da DigiLibrary com V9 Academic
Sistema adaptativo que detecta tipo de conteúdo (roteiro vs teoria)
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_v9_academic import DigiLangV9Academic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DigiLibraryTranslatorV9:
    """Tradutor completo da biblioteca para DigiLang V9 Academic"""

    def __init__(self):
        self.encoder = DigiLangV9Academic()
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'screenplay_files': 0,
            'theory_files': 0,
            'mixed_files': 0,
            'total_original_tokens': 0,
            'total_compressed_tokens': 0,
            'total_original_chars': 0,
            'total_compressed_chars': 0,
            'best_compression': 0,
            'best_file': '',
            'processing_time': 0
        }

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF"""
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                # Process all pages (not just first 50)
                for i, page in enumerate(pdf.pages):
                    if i % 50 == 0 and i > 0:
                        logger.info(f"  Processing page {i} of {pdf_path.name}")
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting from {pdf_path}: {e}")
            return None

    def process_file(self, file_path):
        """Process a single file with V9 Academic"""
        logger.info(f"Processing: {file_path.name}")

        # Extract text
        if file_path.suffix.lower() == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except:
                text = None
        else:
            return None

        if not text or len(text.strip()) < 100:
            logger.warning(f"  ⚠️ Skipping {file_path.name} - no content")
            return None

        # Compress with V9 Academic (adaptive)
        try:
            # V9 uses compress method, not encode
            compressed, stats = self.encoder.compress(text)

            # Extract metadata from stats dict
            content_type = stats['content_type']
            patterns_used = stats['patterns_used']
            original_tokens = len(text) // 4  # Estimate
            compressed_tokens = len(compressed) // 4  # Estimate

            token_compression = ((original_tokens - compressed_tokens) / original_tokens) if original_tokens > 0 else 0

            output = {
                'file': file_path.name,
                'content_type': content_type,
                'patterns_used': patterns_used,
                'original_chars': len(text),
                'compressed_chars': len(compressed),
                'char_compression': ((len(text) - len(compressed)) / len(text)) if len(text) > 0 else 0,
                'token_compression': token_compression,
                'status': 'success'
            }

            # Save compressed file
            output_dir = Path('digilibrary/BIBLIOTECA_DIGILANG_V9_ACADEMIC')
            output_dir.mkdir(parents=True, exist_ok=True)

            output_file = output_dir / f"{file_path.stem}_digilang_v9.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(compressed)

            logger.info(f"  ✅ {file_path.name}: {token_compression:.2%} compression ({content_type})")

            return output

        except Exception as e:
            logger.error(f"  ❌ Error processing {file_path.name}: {e}")
            return {
                'file': file_path.name,
                'status': 'failed',
                'error': str(e)
            }

    def translate_library(self):
        """Translate entire library with V9 Academic"""
        print("="*60)
        print("FASE 17.f - TRADUÇÃO COMPLETA COM V9 ACADEMIC")
        print("Sistema: DigiLang V9 Academic (Adaptativo)")
        print("="*60)

        start_time = time.time()

        # Find all files
        library_path = Path('digilibrary/BIBLIOTECA_ROTEIROS')
        pdf_files = list(library_path.glob('**/*.pdf'))
        txt_files = list(library_path.glob('**/*.txt'))

        all_files = pdf_files + txt_files
        self.stats['total_files'] = len(all_files)

        print(f"\n📚 Arquivos encontrados:")
        print(f"  PDFs: {len(pdf_files)}")
        print(f"  TXTs: {len(txt_files)}")
        print(f"  TOTAL: {len(all_files)}")

        if not all_files:
            print("❌ Nenhum arquivo encontrado!")
            return

        print(f"\n🚀 Iniciando tradução adaptativa com {os.cpu_count()} workers paralelos...")

        results = []

        # Process files in parallel
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            future_to_file = {executor.submit(self.process_file, f): f for f in all_files}

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        if result['status'] == 'success':
                            self.stats['successful'] += 1

                            # Track content types
                            content_type = result.get('content_type', 'unknown')
                            if content_type == 'screenplay':
                                self.stats['screenplay_files'] += 1
                            elif content_type == 'theory':
                                self.stats['theory_files'] += 1
                            else:
                                self.stats['mixed_files'] += 1

                            # Update stats
                            self.stats['total_original_chars'] += result['original_chars']
                            self.stats['total_compressed_chars'] += result['compressed_chars']

                            # Track best compression
                            if result['token_compression'] > self.stats['best_compression']:
                                self.stats['best_compression'] = result['token_compression']
                                self.stats['best_file'] = result['file']
                        else:
                            self.stats['failed'] += 1
                    else:
                        self.stats['failed'] += 1

                except Exception as e:
                    logger.error(f"Future failed for {file_path}: {e}")
                    self.stats['failed'] += 1

        self.stats['processing_time'] = time.time() - start_time

        # Calculate averages
        if self.stats['successful'] > 0:
            avg_compression = (self.stats['total_original_chars'] - self.stats['total_compressed_chars']) / self.stats['total_original_chars']
        else:
            avg_compression = 0

        # Generate report
        self.generate_report(results, avg_compression)

        return self.stats

    def generate_report(self, results, avg_compression):
        """Generate final report"""

        # Save JSON results
        output_file = Path('docs/FASE_17f_V9_ACADEMIC_RESULTS.json')
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump({
                'stats': self.stats,
                'results': results,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)

        # Generate markdown report
        report = f"""# FASE 17.f - RELATÓRIO V9 ACADEMIC

**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Sistema:** DigiLang V9 Academic (Adaptativo)
**Duração:** {self.stats['processing_time']:.2f} segundos

## 📊 ESTATÍSTICAS GERAIS

- **Total de arquivos:** {self.stats['total_files']}
- **Processados com sucesso:** {self.stats['successful']} ({self.stats['successful']/self.stats['total_files']*100:.1f}%)
- **Falhas:** {self.stats['failed']}

## 📂 TIPOS DE CONTEÚDO DETECTADOS

- **Roteiros:** {self.stats['screenplay_files']}
- **Teoria:** {self.stats['theory_files']}
- **Misto:** {self.stats['mixed_files']}

## 🔥 RESULTADOS DE COMPRESSÃO

- **Caracteres originais:** {self.stats['total_original_chars']:,}
- **Caracteres comprimidos:** {self.stats['total_compressed_chars']:,}
- **Compressão média:** {avg_compression:.2%}
- **Melhor compressão:** {self.stats['best_compression']:.2%} ({self.stats['best_file']})

## 📈 ECONOMIA ESTIMADA

- **Caracteres economizados:** {self.stats['total_original_chars'] - self.stats['total_compressed_chars']:,}
- **Economia em tokens (estimada):** ~{int((self.stats['total_original_chars'] - self.stats['total_compressed_chars']) / 4):,}
- **Redução de custo em APIs:** ~{avg_compression:.1%}

## ✅ CONCLUSÃO

A biblioteca foi traduzida com DigiLang V9 Academic, utilizando detecção adaptativa de conteúdo para aplicar os padrões mais apropriados para cada tipo de arquivo.

**Arquivos salvos em:** `digilibrary/BIBLIOTECA_DIGILANG_V9_ACADEMIC/`
"""

        report_file = Path('docs/FASE_17f_V9_ACADEMIC.md')
        with open(report_file, 'w') as f:
            f.write(report)

        print("\n" + "="*60)
        print("RELATÓRIO FINAL - V9 ACADEMIC")
        print("="*60)
        print(f"\n✅ Arquivos processados: {self.stats['successful']}/{self.stats['total_files']}")
        print(f"❌ Falhas: {self.stats['failed']}")
        print(f"\n📂 Tipos detectados:")
        print(f"  Roteiros: {self.stats['screenplay_files']}")
        print(f"  Teoria: {self.stats['theory_files']}")
        print(f"  Misto: {self.stats['mixed_files']}")
        print(f"\n📊 Compressão média: {avg_compression:.2%}")
        print(f"🏆 Melhor compressão: {self.stats['best_compression']:.2%} ({self.stats['best_file']})")
        print(f"⏱️ Tempo total: {self.stats['processing_time']:.2f}s")
        print(f"\n📁 Relatório salvo em: {report_file}")
        print(f"📁 Arquivos traduzidos em: digilibrary/BIBLIOTECA_DIGILANG_V9_ACADEMIC/")

def main():
    translator = DigiLibraryTranslatorV9()
    stats = translator.translate_library()

    print("\n" + "="*60)
    print("🎯 FASE 17.f - V9 ACADEMIC CONCLUÍDA!")
    print("="*60)
    print("\nDiGiLaNg V9 Academic demonstrou detecção adaptativa.")
    print("Próximo: Comparação V8.1 vs V9")

    return stats

if __name__ == "__main__":
    main()