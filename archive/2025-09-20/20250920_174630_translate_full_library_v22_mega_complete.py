#!/usr/bin/env python3
"""
🚀 Tradutor Completo V22 MEGA - Biblioteca Digital
Sistema de tradução com V22 MEGA (15.29% de compressão histórica)
Inclui suporte para arquivos grandes com chunking
"""

import os
import sys
import logging
import time
from pathlib import Path
from typing import List, Tuple, Dict
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apps.scripturemon.digilang_v22_mega import DigiLangV22Mega

class V22MegaLibraryTranslator:
    """Tradutor completo da biblioteca usando V22 MEGA"""

    def __init__(self, output_dir: str = "output/v22_mega", chunk_size: int = 200000):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_size = chunk_size  # Para arquivos grandes

        # Diretório para arquivos chunked
        self.chunked_dir = self.output_dir / "chunked"
        self.chunked_dir.mkdir(exist_ok=True)

    def _load_text_safely(self, file_path: Path) -> str:
        """Carrega texto com múltiplos encodings"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                    if content.strip():
                        return content
            except Exception as e:
                logger.debug(f"Falha com encoding {encoding}: {e}")
                continue

        raise RuntimeError(f"Não foi possível ler {file_path}")

    def _is_large_file(self, file_path: Path) -> bool:
        """Verifica se arquivo é grande (>100k chars)"""
        try:
            size = file_path.stat().st_size
            return size > 100000
        except:
            return False

    def _split_into_chunks(self, text: str) -> List[str]:
        """Divide texto grande em chunks menores"""
        chunks = []
        current_chunk = ""
        paragraphs = text.split('\n\n')

        for paragraph in paragraphs:
            # Se adicionar este parágrafo não ultrapassar o limite
            if len(current_chunk) + len(paragraph) + 2 <= self.chunk_size:
                if current_chunk:
                    current_chunk += '\n\n' + paragraph
                else:
                    current_chunk = paragraph
            else:
                # Salvar chunk atual se não vazio
                if current_chunk:
                    chunks.append(current_chunk)

                # Se parágrafo é muito grande, dividir por sentenças
                if len(paragraph) > self.chunk_size:
                    sentences = paragraph.split('. ')
                    current_chunk = ""

                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) + 2 <= self.chunk_size:
                            if current_chunk:
                                current_chunk += '. ' + sentence
                            else:
                                current_chunk = sentence
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            current_chunk = sentence
                else:
                    current_chunk = paragraph

        # Adicionar último chunk
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def translate_file_chunked(self, file_path: Path) -> Tuple[bool, Dict]:
        """Traduz arquivo grande usando chunks"""
        logger.info(f"📄 Traduzindo arquivo grande em chunks: {file_path.name}")

        try:
            # Carregar texto
            text = self._load_text_safely(file_path)

            # Dividir em chunks
            chunks = self._split_into_chunks(text)
            logger.info(f"📦 Dividido em {len(chunks)} chunks")

            # Traduzir cada chunk
            translated_chunks = []
            total_stats = {
                'original_tokens': 0,
                'final_tokens': 0,
                'chunks_processed': 0,
                'chunks_successful': 0
            }

            for i, chunk in enumerate(chunks, 1):
                logger.info(f"🔄 Processando chunk {i}/{len(chunks)}")

                try:
                    # Criar novo compressor para cada chunk
                    compressor = DigiLangV22Mega()
                    compressed, patterns, stats = compressor.compress(chunk)

                    translated_chunks.append(compressed)
                    total_stats['original_tokens'] += stats.get('original_tokens', 0)
                    total_stats['final_tokens'] += stats.get('final_tokens', 0)
                    total_stats['chunks_successful'] += 1

                    # Salvar dicionário do chunk
                    chunk_dict_path = self.chunked_dir / f"{file_path.stem}_chunk_{i:03d}.json"
                    with open(chunk_dict_path, 'w', encoding='utf-8') as f:
                        json.dump(patterns, f, ensure_ascii=False, indent=2)

                except Exception as e:
                    logger.error(f"❌ Erro no chunk {i}: {e}")
                    translated_chunks.append(chunk)  # Manter original se falhar

                total_stats['chunks_processed'] += 1

            # Reunir chunks traduzidos
            final_text = '\n\n'.join(translated_chunks)

            # Salvar arquivo traduzido
            output_filename = f"{file_path.stem}_v22_mega_chunked.digilang"
            output_path = self.output_dir / output_filename

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_text)

            # Calcular estatísticas finais
            total_stats['compression_ratio'] = (
                1 - (total_stats['final_tokens'] / total_stats['original_tokens'])
                if total_stats['original_tokens'] > 0 else 0
            )

            logger.info(f"✅ Arquivo grande traduzido: {output_path}")
            logger.info(f"📊 Compressão: {total_stats['compression_ratio']:.1%}")

            return True, total_stats

        except Exception as e:
            logger.error(f"❌ Erro traduzindo {file_path.name}: {e}")
            return False, {"error": str(e)}

    def translate_single_file(self, file_path: Path) -> Tuple[bool, Dict]:
        """Traduz um único arquivo"""
        try:
            basename = file_path.stem

            # Verificar se já foi traduzido
            existing_files = list(self.output_dir.glob(f"{basename}_v22_mega*.digilang"))
            if existing_files:
                logger.info(f"⏩ Arquivo já traduzido: {basename}")
                return True, {"status": "already_translated"}

            # Verificar tamanho
            if self._is_large_file(file_path):
                return self.translate_file_chunked(file_path)

            # Tradução normal para arquivos pequenos/médios
            logger.info(f"📄 Traduzindo: {file_path.name}")

            # Carregar texto
            text = self._load_text_safely(file_path)

            # Comprimir com V22 MEGA
            compressor = DigiLangV22Mega()
            compressed, patterns, stats = compressor.compress(text)

            # Salvar arquivo traduzido
            output_filename = f"{basename}_v22_mega.digilang"
            output_path = self.output_dir / output_filename

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(compressed)

            # Salvar dicionário de padrões
            dict_path = output_path.with_suffix('.dict.json')
            with open(dict_path, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, ensure_ascii=False, indent=2)

            # Salvar metadados
            meta_path = output_path.with_suffix('.meta.json')
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'original_file': str(file_path),
                    'stats': stats,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ Traduzido: {output_path}")
            logger.info(f"📊 Compressão: {stats['compression_ratio']:.1%}")

            return True, stats

        except Exception as e:
            logger.error(f"❌ Erro traduzindo {file_path.name}: {e}")
            return False, {"error": str(e)}

    def translate_library(self, data_dir: str = "data") -> Dict:
        """Traduz toda a biblioteca"""
        logger.info("🚀 INICIANDO TRADUÇÃO COMPLETA V22 MEGA")
        logger.info("="*70)

        # Encontrar todos os arquivos .txt
        data_path = Path(data_dir)
        text_files = list(data_path.rglob("*.txt"))

        logger.info(f"📚 Encontrados {len(text_files)} arquivos para traduzir")

        # Estatísticas globais
        global_stats = {
            'files_processed': 0,
            'files_successful': 0,
            'files_failed': 0,
            'files_skipped': 0,
            'total_original_tokens': 0,
            'total_final_tokens': 0,
            'processing_time': 0,
            'results': []
        }

        start_time = time.time()

        # Processar cada arquivo
        for i, file_path in enumerate(text_files, 1):
            logger.info(f"\n📖 Processando {i}/{len(text_files)}: {file_path.name}")

            success, file_stats = self.translate_single_file(file_path)

            global_stats['files_processed'] += 1

            if success:
                if file_stats.get('status') == 'already_translated':
                    global_stats['files_skipped'] += 1
                else:
                    global_stats['files_successful'] += 1
                    global_stats['total_original_tokens'] += file_stats.get('original_tokens', 0)
                    global_stats['total_final_tokens'] += file_stats.get('final_tokens', 0)

                    global_stats['results'].append({
                        'file': file_path.name,
                        'status': 'success',
                        'compression_ratio': file_stats.get('compression_ratio', 0)
                    })
            else:
                global_stats['files_failed'] += 1
                global_stats['results'].append({
                    'file': file_path.name,
                    'status': 'failed',
                    'error': file_stats.get('error', 'Unknown error')
                })

        global_stats['processing_time'] = time.time() - start_time
        global_stats['overall_compression'] = (
            1 - (global_stats['total_final_tokens'] / global_stats['total_original_tokens'])
            if global_stats['total_original_tokens'] > 0 else 0
        )

        # Salvar relatório
        report_path = self.output_dir / "v22_mega_translation_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(global_stats, f, ensure_ascii=False, indent=2)

        logger.info("\n" + "="*70)
        logger.info("🎯 RELATÓRIO FINAL V22 MEGA")
        logger.info("="*70)
        logger.info(f"📋 Processados: {global_stats['files_processed']}")
        logger.info(f"✅ Novos sucessos: {global_stats['files_successful']}")
        logger.info(f"⏩ Já traduzidos: {global_stats['files_skipped']}")
        logger.info(f"❌ Falhas: {global_stats['files_failed']}")
        logger.info(f"🎯 Compressão geral: {global_stats['overall_compression']:.1%}")
        logger.info(f"⏱️ Tempo total: {global_stats['processing_time']:.1f}s")
        logger.info("="*70)

        return global_stats


def main():
    """Função principal"""
    try:
        translator = V22MegaLibraryTranslator()
        results = translator.translate_library()

        if results['files_successful'] > 0 or results['files_skipped'] > 0:
            print(f"\n🎉 TRADUÇÃO V22 MEGA CONCLUÍDA!")
            print(f"✅ {results['files_successful']} novos arquivos traduzidos")
            print(f"⏩ {results['files_skipped']} arquivos já traduzidos")
            print(f"📁 Arquivos salvos em: output/v22_mega/")
            return 0
        else:
            print("\n⚠️ Nenhum arquivo foi traduzido")
            return 1

    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)