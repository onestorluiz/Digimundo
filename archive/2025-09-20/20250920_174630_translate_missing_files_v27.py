#!/usr/bin/env python3
"""
🚀 Tradutor V27 para Arquivos Grandes Ausentes
Sistema especializado para processar os 11 arquivos grandes que não foram traduzidos
Utiliza processamento em chunks para superar limitações de tamanho
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

from apps.scripturemon.digilang_adaptive_selector import DigiLangAdaptiveSelector

class LargeFileTranslatorV27:
    """
    Tradutor especializado para arquivos grandes
    Implementa chunking inteligente e processamento otimizado
    """

    def __init__(self, output_dir: str = "output/v27_adaptive", chunk_size: int = 200000):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_size = chunk_size  # 200k chars por chunk

        # Inicializar selector adaptativo
        self.selector = DigiLangAdaptiveSelector()

        # Lista dos arquivos grandes ausentes
        self.missing_files = [
            "The_21st_century_screenplay___a_comprehensive_guide_to_--_Linda_Aronson,_Paul_Thompson_--_Allen_&_Unwin,_Sydney,_2010_--_Allen_et_Unwin_--_9781742371368_--_ec27a9b991fda419187019083e7561ce_--_Anna's_Archive.txt",
            "O-Herói-de-Mil-Faces-_Alta-Qualidade__ATBC_-Jonathan-C_-Young_-Joseph-Campbell-Paperback_-1995-Cult.txt",
            "The_Anatomy_of_Story__22_Steps_to_Becoming_a_Master_--_John_Truby_--_cc9aceb2d5a03088d93aa086b8fb0b9c_--_Anna's_Archive.txt",
            "Screenplay___The_Foundations_of_Screenwriting_--_Syd_Field_--_Newly_Revised_And_Updated,_PS,_2005_--_Delta_Trade_Paperbacks_--_9780307423269_--_3fc0edadf84a796e1fb8cee657d759f3_--_Anna's_Archive.txt",
            "The_Writers_Journey__Mythic_Structure_for_Writers,_2nd_--_by_Christopher_Vogler_--_2nd_ed_,_Studio_City,_CA,_California,_1998_--_Michael_Wiese_--_9780941188708_--_359443807d3bdb7804131de891c529d8_--_Anna's_Archive.txt",
            "The_art_of_dramatic_writing___its_basis_in_the_creative_--_Lajos_Egri_--_Balitmore,_US,_United_States,_2009_--_www_bnpublishing_net_--_9781607961307_--_e8f1bf602b49d38b3658708886c7b28c_--_Anna's_Archive.txt",
            "Writing_the_TV_Drama_Series___How_to_Succeed_As_a_--_Pamela_Douglas_--_Lightning_Source_Inc__(Tier_1),_[N_p_],_2011_--_Michael_Wiese_Productions;_--_9781615930241_--_bc841ecbacb355ca8d2eb6aeffce1141_--_Anna's_Archive.txt",
            "Writing_Short_Films__Structure_and_Content_for_Screenwriters_--_Linda_J__Cowgill_--_2,_2010_--_Potter__TenSpeed__Harmony_--_879c71b5c6667c2796770fa26da4d76c_--_Anna's_Archive.txt",
            "Ontology_and_the_Art_of_Tragedy__An_Approach_to_Aristotle's_--_Martha_Husain;_NetLibrary,_Inc_--_S_U_N_Y_Series_in_Ancient_Greek_Philosophy,_2001_--_9780585427775_--_8002e5f4ff05ee3d5311912e668d7292_--_Anna's_Archive.txt",
            "The_Heroine's_Journey_Workbook__A_Map_for_Every_Woman's_--_Murdock,_Maureen,_author_--_Place_of_publication_not_identified,_2020_--_Shambhala_--_9781570622557_--_3a3502ff855ab55ad41b292ecbef8b47_--_Anna's_Archive.txt",
            "Creating_Character_Arcs__The_Masterful_Author's_Guide_to_--_K_M__Weiland_--_Helping_Writers_Become_Authors_7,_2016_--_PenForASword_Publishing_--_d3ba22b5478bf9fc9026860497e59de3_--_Anna's_Archive.txt"
        ]

    def _find_missing_files(self, data_dir: str = "data") -> List[Path]:
        """Encontra os arquivos que ainda não foram traduzidos"""
        data_path = Path(data_dir)
        missing = []

        for txt_file in data_path.rglob("*.txt"):
            basename = txt_file.stem
            size = txt_file.stat().st_size

            # Verificar se tradução existe
            translated_files = list(self.output_dir.glob(f"{basename}_v27_*.digilang"))

            # Se não tem tradução E é grande (>100k chars)
            if not translated_files and size > 100000:
                missing.append(txt_file)
                logger.info(f"📄 Arquivo ausente: {txt_file.name} ({size:,} chars)")

        return missing

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

    def _split_into_smart_chunks(self, text: str) -> List[str]:
        """
        Divide texto em chunks inteligentes respeitando parágrafos
        """
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

        logger.info(f"📦 Texto dividido em {len(chunks)} chunks")
        return chunks

    def _translate_chunks(self, chunks: List[str]) -> Tuple[List[str], Dict]:
        """Traduz cada chunk e retorna lista de chunks traduzidos"""
        translated_chunks = []
        total_stats = {
            'original_tokens': 0,
            'final_tokens': 0,
            'chunks_processed': 0,
            'chunks_successful': 0,
            'processing_time': 0
        }

        start_time = time.time()

        for i, chunk in enumerate(chunks, 1):
            logger.info(f"🔄 Processando chunk {i}/{len(chunks)} ({len(chunk):,} chars)")

            try:
                # Comprimir chunk usando sistema adaptativo
                compressed, replacement_map, stats = self.selector.compress_adaptive(chunk)

                translated_chunks.append(compressed)
                total_stats['original_tokens'] += stats.get('original_tokens', 0)
                total_stats['final_tokens'] += stats.get('final_tokens', 0)
                total_stats['chunks_successful'] += 1

                logger.info(f"✅ Chunk {i}: {stats.get('compression_ratio', 0):.1%} compressão")

            except Exception as e:
                logger.error(f"❌ Erro no chunk {i}: {e}")
                # Em caso de erro, manter chunk original
                translated_chunks.append(chunk)

            total_stats['chunks_processed'] += 1

        total_stats['processing_time'] = time.time() - start_time
        total_stats['compression_ratio'] = (
            1 - (total_stats['final_tokens'] / total_stats['original_tokens'])
            if total_stats['original_tokens'] > 0 else 0
        )

        logger.info(f"📊 Chunks processados: {total_stats['chunks_successful']}/{total_stats['chunks_processed']}")
        logger.info(f"🎯 Compressão total: {total_stats['compression_ratio']:.1%}")

        return translated_chunks, total_stats

    def translate_large_file(self, file_path: Path) -> Tuple[bool, Dict]:
        """
        Traduz um arquivo grande usando estratégia de chunks
        """
        logger.info(f"🚀 Iniciando tradução: {file_path.name}")
        logger.info(f"📏 Tamanho: {file_path.stat().st_size:,} chars")

        try:
            # Carregar texto
            text = self._load_text_safely(file_path)

            # Dividir em chunks
            chunks = self._split_into_smart_chunks(text)

            # Traduzir chunks
            translated_chunks, stats = self._translate_chunks(chunks)

            # Reunir chunks traduzidos
            final_text = '\n\n'.join(translated_chunks)

            # Gerar nome de arquivo
            basename = file_path.stem
            output_filename = f"{basename}_v27_chunked.digilang"
            output_path = self.output_dir / output_filename

            # Salvar arquivo traduzido
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_text)

            # Salvar metadados
            metadata_path = output_path.with_suffix('.chunked.json')
            metadata = {
                'original_file': str(file_path),
                'chunks_count': len(chunks),
                'translation_strategy': 'chunked_v27_adaptive',
                'stats': stats,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ Tradução concluída: {output_path}")
            logger.info(f"📊 Compressão final: {stats['compression_ratio']:.1%}")

            return True, stats

        except Exception as e:
            logger.error(f"❌ Erro traduzindo {file_path.name}: {e}")
            return False, {"error": str(e)}

    def translate_all_missing(self) -> Dict:
        """Traduz todos os arquivos ausentes"""
        logger.info("🎯 INICIANDO TRADUÇÃO DOS ARQUIVOS GRANDES AUSENTES")
        logger.info("="*70)

        # Encontrar arquivos ausentes
        missing_files = self._find_missing_files()

        if not missing_files:
            logger.info("✅ Todos os arquivos já foram traduzidos!")
            return {"message": "Nenhum arquivo ausente"}

        logger.info(f"📋 Encontrados {len(missing_files)} arquivos para traduzir")

        # Estatísticas globais
        global_stats = {
            'files_processed': 0,
            'files_successful': 0,
            'files_failed': 0,
            'total_original_tokens': 0,
            'total_final_tokens': 0,
            'processing_time': 0,
            'results': []
        }

        start_time = time.time()

        # Processar cada arquivo
        for i, file_path in enumerate(missing_files, 1):
            logger.info(f"\n📖 Arquivo {i}/{len(missing_files)}: {file_path.name}")

            success, file_stats = self.translate_large_file(file_path)

            global_stats['files_processed'] += 1

            if success:
                global_stats['files_successful'] += 1
                global_stats['total_original_tokens'] += file_stats.get('original_tokens', 0)
                global_stats['total_final_tokens'] += file_stats.get('final_tokens', 0)

                global_stats['results'].append({
                    'file': file_path.name,
                    'status': 'success',
                    'compression_ratio': file_stats.get('compression_ratio', 0),
                    'chunks': file_stats.get('chunks_processed', 0)
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
        report_path = self.output_dir / "large_files_translation_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(global_stats, f, ensure_ascii=False, indent=2)

        logger.info("\n" + "="*70)
        logger.info("🎯 RELATÓRIO FINAL - ARQUIVOS GRANDES")
        logger.info("="*70)
        logger.info(f"📋 Processados: {global_stats['files_processed']}")
        logger.info(f"✅ Sucessos: {global_stats['files_successful']}")
        logger.info(f"❌ Falhas: {global_stats['files_failed']}")
        logger.info(f"🎯 Compressão geral: {global_stats['overall_compression']:.1%}")
        logger.info(f"⏱️ Tempo total: {global_stats['processing_time']:.1f}s")
        logger.info("="*70)

        return global_stats


def main():
    """Função principal"""
    try:
        translator = LargeFileTranslatorV27()
        results = translator.translate_all_missing()

        if results.get('files_successful', 0) > 0:
            print("\n🎉 TRADUÇÃO DOS ARQUIVOS GRANDES CONCLUÍDA!")
            print(f"✅ {results['files_successful']} arquivos traduzidos com sucesso")
            print(f"📁 Arquivos salvos em: output/v27_adaptive/")
            return 0
        else:
            print("\n⚠️ Nenhum arquivo novo foi traduzido")
            return 1

    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)