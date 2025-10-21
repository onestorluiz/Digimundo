#!/usr/bin/env python3
"""
Processador de Biblioteca DigiLang V23 ULTIMATE
================================================

Script para processar toda a biblioteca de PDFs com compressão
personalizada V23 ULTIMATE.

Cada PDF é:
1. Minerado individualmente
2. Comprimido com dicionário personalizado
3. Salvo com pacote completo para interpretação

Autor: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion
Data: 14/09/2025
"""

import sys
from pathlib import Path
import json
import time
import logging
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from apps.scripturemon.digilang_v23_ultimate import DigiLangV23Ultimate

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LibraryProcessor:
    """Processador de biblioteca completa"""

    def __init__(self, library_path: str = "./digilibrary"):
        """
        Inicializar processador

        Args:
            library_path: Caminho para a biblioteca de PDFs
        """
        self.library_path = Path(library_path)
        self.v23 = DigiLangV23Ultimate()
        self.results = []

    def find_all_pdfs(self) -> List[Path]:
        """Encontrar todos os PDFs na biblioteca"""
        pdfs = []

        # Diretórios específicos de roteiros
        screenplay_dirs = [
            self.library_path / "BIBLIOTECA_ROTEIROS" / "roteiros_mestres",
            self.library_path / "BIBLIOTECA_ROTEIROS" / "roteiros_classicos",
            self.library_path / "BIBLIOTECA_ROTEIROS" / "roteiros_modernos",
            self.library_path / "BIBLIOTECA_ROTEIROS",
        ]

        # Buscar em cada diretório
        for dir_path in screenplay_dirs:
            if dir_path.exists():
                pdfs.extend(dir_path.glob("*.pdf"))
                pdfs.extend(dir_path.glob("*.PDF"))

        # Buscar recursivamente em toda a biblioteca também
        pdfs.extend(self.library_path.rglob("*.pdf"))
        pdfs.extend(self.library_path.rglob("*.PDF"))

        # Remover duplicatas
        pdfs = list(set(pdfs))

        logger.info(f"📚 Encontrados {len(pdfs)} PDFs na biblioteca")
        return pdfs

    def process_single_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Processar um único PDF

        Args:
            pdf_path: Caminho do PDF

        Returns:
            Dict com resultado do processamento
        """
        start_time = time.time()
        logger.info(f"\n{'='*60}")
        logger.info(f"📄 Processando: {pdf_path.name}")

        try:
            # Processar com V23
            result = self.v23.process_pdf(str(pdf_path))

            if result.success:
                # Salvar pacote completo
                output_path = self.v23.save_compression_package(result)

                processing_time = time.time() - start_time

                return {
                    'success': True,
                    'pdf_name': pdf_path.name,
                    'pdf_path': str(pdf_path),
                    'output_path': output_path,
                    'stats': result.stats,
                    'processing_time': processing_time
                }
            else:
                return {
                    'success': False,
                    'pdf_name': pdf_path.name,
                    'pdf_path': str(pdf_path),
                    'error': 'Compression failed',
                    'processing_time': time.time() - start_time
                }

        except Exception as e:
            logger.error(f"❌ Erro ao processar {pdf_path.name}: {e}")
            logger.error(traceback.format_exc())

            return {
                'success': False,
                'pdf_name': pdf_path.name,
                'pdf_path': str(pdf_path),
                'error': str(e),
                'processing_time': time.time() - start_time
            }

    def process_library(self, max_workers: int = 3) -> Dict[str, Any]:
        """
        Processar toda a biblioteca

        Args:
            max_workers: Número máximo de threads paralelas

        Returns:
            Dict com estatísticas gerais
        """
        logger.info("\n" + "="*80)
        logger.info("🚀 INICIANDO PROCESSAMENTO DA BIBLIOTECA V23 ULTIMATE")
        logger.info("="*80)

        # Encontrar todos os PDFs
        pdfs = self.find_all_pdfs()

        if not pdfs:
            logger.warning("⚠️ Nenhum PDF encontrado na biblioteca")
            return {'total': 0, 'successful': 0, 'failed': 0}

        # Processar em paralelo
        successful = 0
        failed = 0
        total_tokens_saved = 0
        best_compression = 0
        best_pdf = ""

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.process_single_pdf, pdf): pdf for pdf in pdfs}

            for future in as_completed(futures):
                pdf = futures[future]
                try:
                    result = future.result()
                    self.results.append(result)

                    if result['success']:
                        successful += 1
                        stats = result['stats']
                        total_tokens_saved += stats['tokens_saved']

                        if stats['token_compression'] > best_compression:
                            best_compression = stats['token_compression']
                            best_pdf = result['pdf_name']

                        logger.info(f"✅ {result['pdf_name']}: {stats['token_compression']:.2f}% compressão")
                    else:
                        failed += 1
                        logger.error(f"❌ {result['pdf_name']}: {result.get('error', 'Unknown error')}")

                except Exception as e:
                    failed += 1
                    logger.error(f"❌ Erro ao processar {pdf.name}: {e}")

        # Salvar relatório geral
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'version': 'V23_ULTIMATE',
            'total_pdfs': len(pdfs),
            'successful': successful,
            'failed': failed,
            'total_tokens_saved': total_tokens_saved,
            'best_compression': best_compression,
            'best_pdf': best_pdf,
            'results': self.results
        }

        report_path = Path("./output/v23_ultimate/library_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # Exibir resumo
        logger.info("\n" + "="*80)
        logger.info("📊 RESUMO DO PROCESSAMENTO V23 ULTIMATE")
        logger.info("="*80)
        logger.info(f"✅ Sucesso: {successful}/{len(pdfs)} PDFs")
        logger.info(f"❌ Falhas: {failed} PDFs")
        logger.info(f"💾 Total economizado: {total_tokens_saved:,} tokens")
        logger.info(f"🏆 Melhor compressão: {best_pdf} ({best_compression:.2f}%)")
        logger.info(f"📄 Relatório salvo em: {report_path}")

        return report

    def create_master_index(self):
        """Criar índice mestre para acesso rápido"""
        index = {
            'version': 'V23_ULTIMATE',
            'created': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_documents': len(self.results),
            'documents': {}
        }

        for result in self.results:
            if result['success']:
                index['documents'][result['pdf_name']] = {
                    'path': result['output_path'],
                    'compression': result['stats']['token_compression'],
                    'tokens_saved': result['stats']['tokens_saved'],
                    'dictionary_size': result['stats']['dictionary_size']
                }

        index_path = Path("./output/v23_ultimate/master_index.json")
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        logger.info(f"\n📑 Índice mestre criado: {index_path}")


def main():
    """Função principal"""
    processor = LibraryProcessor()

    # Processar biblioteca completa
    report = processor.process_library(max_workers=3)

    # Criar índice mestre
    if report['successful'] > 0:
        processor.create_master_index()

    # Criar README geral
    readme_content = f"""# DigiLang V23 ULTIMATE - Biblioteca Processada

## 📊 Estatísticas Gerais
- **Total de PDFs**: {report['total_pdfs']}
- **Processados com sucesso**: {report['successful']}
- **Falhas**: {report['failed']}
- **Tokens economizados**: {report['total_tokens_saved']:,}
- **Melhor compressão**: {report['best_pdf']} ({report['best_compression']:.2f}%)

## 🔍 Como Acessar

### Para AI/Ollama/Digimon:
1. Consulte `master_index.json` para localizar documentos
2. Cada documento tem seu próprio diretório em `output/v23_ultimate/`
3. Use o `digilang_interpreter.py` para decodificar

### Estrutura de cada documento:
```
output/v23_ultimate/[nome_do_pdf]/
├── compressed_text.txt   # Texto comprimido com símbolos
├── dictionary.json        # Dicionário de decodificação
├── metadata.json         # Metadados e estatísticas
└── README.md            # Instruções específicas
```

## 💡 Princípios V23 ULTIMATE
1. **Mineração personalizada**: Cada PDF tem seu próprio dicionário
2. **Priorização inteligente**: Foco em palavras multi-token
3. **Máxima eficiência**: Usa 1,200+ símbolos Unicode de 1 token
4. **Nunca substitui palavras de 1 token**: Evita desperdício

---
*Processado em: {report['timestamp']}*
*Sistema ScriptureMon Champion - DigiLang V23 ULTIMATE*
"""

    readme_path = Path("./output/v23_ultimate/README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    logger.info(f"\n📝 README geral criado: {readme_path}")
    logger.info("\n✅ PROCESSAMENTO COMPLETO DA BIBLIOTECA!")

    return 0


if __name__ == "__main__":
    sys.exit(main())