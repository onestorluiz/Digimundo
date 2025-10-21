#!/usr/bin/env python3
"""
🚀 DigiLang V27 Adaptive - Tradução Completa da Biblioteca Digital
Sistema Adaptativo que usa V27 MEGA Ultimate como padrão com fallbacks inteligentes

Funcionalidades:
- V27 MEGA Ultimate como motor principal (suas 5 regras definitivas)
- Fallbacks automáticos para casos específicos
- Processamento completo da biblioteca digital
- Relatórios comparativos detalhados
- Sistema robusto com tratamento de erros
"""

import os
import sys
import logging
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apps.scripturemon.digilang_adaptive_selector import DigiLangAdaptiveSelector

class LibraryTranslatorV27Adaptive:
    """
    Tradutor da biblioteca digital usando sistema adaptativo V27
    """

    def __init__(self, output_base_dir: str = "output/v27_adaptive"):
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(parents=True, exist_ok=True)

        # Inicializar selector adaptativo
        self.selector = DigiLangAdaptiveSelector()

        # Estatísticas globais
        self.global_stats = {
            'files_processed': 0,
            'files_successful': 0,
            'files_failed': 0,
            'total_original_chars': 0,
            'total_compressed_chars': 0,
            'total_original_tokens': 0,
            'total_final_tokens': 0,
            'total_tokens_saved': 0,
            'processing_time': 0,
            'version_usage': {},
            'compression_by_file': {},
            'errors': []
        }

    def _find_all_text_files(self, data_dir: str = "data") -> List[Path]:
        """Encontra todos os arquivos de texto na biblioteca"""
        data_path = Path(data_dir)
        if not data_path.exists():
            logger.error(f"Diretório {data_dir} não encontrado")
            return []

        text_files = []

        # Buscar arquivos .txt
        txt_files = list(data_path.rglob("*.txt"))
        text_files.extend(txt_files)

        logger.info(f"📚 Encontrados {len(text_files)} arquivos de texto")

        # Log dos primeiros arquivos encontrados
        for i, file_path in enumerate(text_files[:10]):
            logger.info(f"   {i+1}. {file_path.name}")
        if len(text_files) > 10:
            logger.info(f"   ... e mais {len(text_files) - 10} arquivos")

        return text_files

    def _load_text_safely(self, file_path: Path) -> Optional[str]:
        """Carrega texto do arquivo com tratamento robusto de encoding"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                    if content.strip():  # Verificar se não está vazio
                        return content
            except Exception as e:
                logger.debug(f"Falha com encoding {encoding}: {e}")
                continue

        logger.error(f"❌ Não foi possível ler {file_path}")
        return None

    def _generate_safe_filename(self, original_path: Path, version_used: str) -> str:
        """Gera nome de arquivo seguro para saída"""
        # Remover caracteres problemáticos
        safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in original_path.stem)
        safe_name = safe_name[:100]  # Limitar tamanho

        return f"{safe_name}_v27_{version_used}.digilang"

    def translate_single_file(self, file_path: Path) -> Tuple[bool, Dict]:
        """
        Traduz um único arquivo usando o sistema adaptativo

        Returns:
            Tupla (sucesso, estatísticas)
        """
        logger.info(f"🔄 Processando: {file_path.name}")

        try:
            # Carregar texto
            text = self._load_text_safely(file_path)
            if not text:
                return False, {"error": "Não foi possível carregar o arquivo"}

            # Verificar tamanho mínimo
            if len(text.strip()) < 100:
                logger.warning(f"⚠️ Arquivo muito pequeno: {file_path.name}")
                return False, {"error": "Arquivo muito pequeno"}

            # Comprimir usando sistema adaptativo
            start_time = time.time()
            compressed, replacement_map, stats = self.selector.compress_adaptive(text)
            processing_time = time.time() - start_time

            # Adicionar metadados do arquivo
            stats.update({
                'original_file': str(file_path),
                'file_size_chars': len(text),
                'processing_time': processing_time,
                'compression_success': True
            })

            # Salvar arquivo comprimido
            version_used = stats.get('version_used', 'unknown')
            output_filename = self._generate_safe_filename(file_path, version_used)
            output_path = self.output_base_dir / output_filename

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(compressed)

            # Salvar mapa de substituições
            replacement_path = output_path.with_suffix('.map.json')
            with open(replacement_path, 'w', encoding='utf-8') as f:
                # Converter replacement_map para formato serializável
                serializable_map = {}
                if isinstance(replacement_map, dict):
                    for k, v in replacement_map.items():
                        serializable_map[str(k)] = str(v)

                json.dump({
                    'replacement_map': serializable_map,
                    'stats': stats,
                    'metadata': {
                        'version_used': version_used,
                        'compressed_file': str(output_path),
                        'compression_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ {file_path.name}: {stats.get('compression_ratio', 0):.1%} compressão com {version_used}")

            return True, stats

        except Exception as e:
            logger.error(f"❌ Erro processando {file_path.name}: {e}")
            return False, {"error": str(e)}

    def translate_library(self, data_dir: str = "data") -> Dict:
        """
        Traduz toda a biblioteca digital

        Returns:
            Estatísticas finais da tradução
        """
        logger.info("🚀 INICIANDO TRADUÇÃO V27 ADAPTIVE DA BIBLIOTECA DIGITAL")
        logger.info("="*70)

        start_time = time.time()

        # Encontrar todos os arquivos
        text_files = self._find_all_text_files(data_dir)
        if not text_files:
            logger.error("❌ Nenhum arquivo encontrado")
            return self.global_stats

        self.global_stats['files_found'] = len(text_files)

        # Processar cada arquivo
        for i, file_path in enumerate(text_files, 1):
            logger.info(f"\n📖 Arquivo {i}/{len(text_files)}: {file_path.name}")

            success, file_stats = self.translate_single_file(file_path)

            self.global_stats['files_processed'] += 1

            if success:
                self.global_stats['files_successful'] += 1

                # Acumular estatísticas
                self.global_stats['total_original_chars'] += file_stats.get('original_chars', 0)
                self.global_stats['total_compressed_chars'] += file_stats.get('compressed_chars', 0)
                self.global_stats['total_original_tokens'] += file_stats.get('original_tokens', 0)
                self.global_stats['total_final_tokens'] += file_stats.get('final_tokens', 0)
                self.global_stats['total_tokens_saved'] += file_stats.get('tokens_saved', 0)

                # Rastrear uso de versões
                version_used = file_stats.get('version_used', 'unknown')
                if version_used not in self.global_stats['version_usage']:
                    self.global_stats['version_usage'][version_used] = 0
                self.global_stats['version_usage'][version_used] += 1

                # Salvar compressão por arquivo
                self.global_stats['compression_by_file'][file_path.name] = {
                    'compression_ratio': file_stats.get('compression_ratio', 0),
                    'version_used': version_used,
                    'tokens_saved': file_stats.get('tokens_saved', 0)
                }

            else:
                self.global_stats['files_failed'] += 1
                self.global_stats['errors'].append({
                    'file': str(file_path),
                    'error': file_stats.get('error', 'Unknown error')
                })

        # Calcular estatísticas finais
        self.global_stats['processing_time'] = time.time() - start_time

        if self.global_stats['total_original_tokens'] > 0:
            self.global_stats['overall_compression_ratio'] = 1 - (
                self.global_stats['total_final_tokens'] / self.global_stats['total_original_tokens']
            )
        else:
            self.global_stats['overall_compression_ratio'] = 0

        # Salvar relatório completo
        self._save_final_report()

        return self.global_stats

    def _save_final_report(self):
        """Salva relatório final detalhado"""
        report_path = self.output_base_dir / "translation_report_v27_adaptive.json"

        # Adicionar relatório de performance do selector
        selector_report = self.selector.get_performance_report()
        self.global_stats['selector_performance'] = selector_report

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.global_stats, f, ensure_ascii=False, indent=2)

        logger.info(f"📊 Relatório salvo em: {report_path}")

    def print_final_summary(self):
        """Imprime resumo final da tradução"""
        stats = self.global_stats

        print("\n" + "="*70)
        print("🎯 RELATÓRIO FINAL - TRADUÇÃO V27 ADAPTIVE")
        print("="*70)
        print(f"📚 Arquivos processados: {stats['files_processed']}")
        print(f"✅ Sucessos: {stats['files_successful']}")
        print(f"❌ Falhas: {stats['files_failed']}")
        print(f"📊 Taxa de sucesso: {stats['files_successful']/max(stats['files_processed'],1)*100:.1f}%")
        print()
        print(f"📄 Caracteres: {stats['total_original_chars']:,} → {stats['total_compressed_chars']:,}")
        print(f"🎯 Tokens: {stats['total_original_tokens']:,} → {stats['total_final_tokens']:,}")
        print(f"💰 Tokens economizados: {stats['total_tokens_saved']:,}")
        print(f"📈 Compressão geral: {stats.get('overall_compression_ratio', 0):.1%}")
        print(f"⏱️ Tempo total: {stats['processing_time']:.2f}s")
        print()
        print("🔧 VERSÕES UTILIZADAS:")
        for version, count in stats['version_usage'].items():
            percentage = count / max(stats['files_successful'], 1) * 100
            print(f"   {version}: {count} arquivos ({percentage:.1f}%)")
        print()

        # Top 5 melhores compressões
        if stats['compression_by_file']:
            sorted_files = sorted(
                stats['compression_by_file'].items(),
                key=lambda x: x[1]['compression_ratio'],
                reverse=True
            )
            print("🏆 TOP 5 MELHORES COMPRESSÕES:")
            for i, (filename, data) in enumerate(sorted_files[:5], 1):
                print(f"   {i}. {filename[:50]}... "
                      f"({data['compression_ratio']:.1%} com {data['version_used']})")

        print("="*70)


def main():
    """Função principal"""
    try:
        # Criar tradutor
        translator = LibraryTranslatorV27Adaptive()

        # Executar tradução
        final_stats = translator.translate_library()

        # Mostrar resumo final
        translator.print_final_summary()

        # Verificar se houve sucessos
        if final_stats['files_successful'] > 0:
            print(f"\n🎉 TRADUÇÃO CONCLUÍDA COM SUCESSO!")
            print(f"📁 Arquivos traduzidos salvos em: output/v27_adaptive/")
            return 0
        else:
            print(f"\n❌ NENHUM ARQUIVO FOI TRADUZIDO COM SUCESSO")
            return 1

    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)