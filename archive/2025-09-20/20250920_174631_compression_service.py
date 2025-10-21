#!/usr/bin/env python3
"""
🗜️ Compression Service - Serviço Unificado de Compressão DigiLang
FASE 21: Integração DigiLang no Sistema Principal
"""

import logging
from typing import Tuple, Dict, Optional, List
from pathlib import Path
import json
import time
from enum import Enum

logger = logging.getLogger(__name__)

class CompressionVersion(Enum):
    """Versões disponíveis de compressão"""
    V22_MEGA = "v22_mega"
    V27_ADAPTIVE = "v27_adaptive"
    ADAPTIVE = "adaptive"
    AUTO = "auto"

class CompressionService:
    """
    Serviço unificado para compressão/descompressão DigiLang
    Integra todas as versões disponíveis com API consistente
    """

    def __init__(self):
        self.versions_available = {}
        self.stats = {
            'total_compressions': 0,
            'total_decompressions': 0,
            'total_tokens_saved': 0,
            'total_processing_time': 0
        }
        self._load_compression_engines()

    def _load_compression_engines(self):
        """Carrega todas as versões de compressão disponíveis"""

        # V22 MEGA
        try:
            from apps.scripturemon.digilang_v22_mega import DigiLangV22Mega
            self.versions_available[CompressionVersion.V22_MEGA] = DigiLangV22Mega
            logger.info("✅ DigiLang V22 MEGA carregado")
        except ImportError as e:
            logger.warning(f"⚠️ DigiLang V22 MEGA não disponível: {e}")

        # V27 Adaptive
        try:
            from apps.scripturemon.digilang_v27_mega_ultimate import DigiLangV27MegaUltimate
            self.versions_available[CompressionVersion.V27_ADAPTIVE] = DigiLangV27MegaUltimate
            logger.info("✅ DigiLang V27 Adaptive carregado")
        except ImportError as e:
            logger.warning(f"⚠️ DigiLang V27 Adaptive não disponível: {e}")

        # Adaptive Selector
        try:
            from apps.scripturemon.digilang_adaptive_selector import DigiLangAdaptiveSelector
            self.adaptive_selector = DigiLangAdaptiveSelector()
            logger.info("✅ Adaptive Selector carregado")
        except ImportError as e:
            logger.warning(f"⚠️ Adaptive Selector não disponível: {e}")
            self.adaptive_selector = None

        logger.info(f"💎 {len(self.versions_available)} versões de compressão carregadas")

    def compress(self, text: str, version: CompressionVersion = CompressionVersion.AUTO) -> Tuple[str, Dict, Dict]:
        """
        Comprime texto usando a versão especificada

        Args:
            text: Texto a comprimir
            version: Versão do compressor a usar (AUTO seleciona automaticamente)

        Returns:
            Tupla (texto_comprimido, dicionário_substituições, estatísticas)
        """
        start_time = time.time()

        # Seleção automática de versão
        if version == CompressionVersion.AUTO:
            version = self._select_best_version(text)
            logger.info(f"🤖 Versão selecionada automaticamente: {version.value}")

        # Usar Adaptive Selector se disponível e solicitado
        if version == CompressionVersion.ADAPTIVE and self.adaptive_selector:
            compressed, dictionary, stats = self.adaptive_selector.compress_adaptive(text)
        else:
            # Usar versão específica
            if version not in self.versions_available:
                raise ValueError(f"Versão {version.value} não disponível")

            compressor_class = self.versions_available[version]
            compressor = compressor_class()
            compressed, dictionary, stats = compressor.compress(text)

        # Atualizar estatísticas globais
        processing_time = time.time() - start_time
        stats['processing_time'] = processing_time
        stats['version_used'] = version.value

        self.stats['total_compressions'] += 1
        self.stats['total_tokens_saved'] += stats.get('tokens_saved', 0)
        self.stats['total_processing_time'] += processing_time

        logger.info(f"✅ Compressão concluída: {stats.get('compression_ratio', 0):.1%} em {processing_time:.2f}s")

        return compressed, dictionary, stats

    def decompress(self, compressed_text: str, dictionary: Dict[str, str]) -> str:
        """
        Descomprime texto usando o dicionário fornecido

        Args:
            compressed_text: Texto comprimido
            dictionary: Dicionário de substituições usado na compressão

        Returns:
            Texto original descomprimido
        """
        start_time = time.time()
        decompressed = compressed_text

        # Aplicar substituições inversas
        # Ordenar por tamanho do símbolo (maior primeiro) para evitar substituições parciais
        sorted_dict = sorted(dictionary.items(), key=lambda x: len(x[1]), reverse=True)

        for original, symbol in sorted_dict:
            decompressed = decompressed.replace(symbol, original)

        processing_time = time.time() - start_time
        self.stats['total_decompressions'] += 1
        self.stats['total_processing_time'] += processing_time

        logger.info(f"✅ Descompressão concluída em {processing_time:.2f}s")

        return decompressed

    def compress_file(self, input_path: Path, output_dir: Optional[Path] = None,
                     version: CompressionVersion = CompressionVersion.AUTO) -> Tuple[Path, Dict]:
        """
        Comprime arquivo e salva resultado

        Args:
            input_path: Caminho do arquivo a comprimir
            output_dir: Diretório de saída (padrão: output/compressed/)
            version: Versão do compressor

        Returns:
            Tupla (caminho_arquivo_comprimido, estatísticas)
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

        # Configurar diretório de saída
        if output_dir is None:
            output_dir = Path("output/compressed")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Ler arquivo
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Comprimir
        compressed, dictionary, stats = self.compress(text, version)

        # Salvar arquivo comprimido
        output_filename = f"{input_path.stem}_{version.value}.digilang"
        output_path = output_dir / output_filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(compressed)

        # Salvar dicionário
        dict_path = output_path.with_suffix('.dict.json')
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=2)

        # Salvar metadados
        meta_path = output_path.with_suffix('.meta.json')
        meta = {
            'original_file': str(input_path),
            'compressed_file': str(output_path),
            'dictionary_file': str(dict_path),
            'stats': stats,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        logger.info(f"📁 Arquivo comprimido salvo: {output_path}")
        logger.info(f"📊 Compressão: {stats.get('compression_ratio', 0):.1%}")
        logger.info(f"💾 Economia: {stats.get('tokens_saved', 0)} tokens")

        return output_path, stats

    def decompress_file(self, compressed_path: Path, output_dir: Optional[Path] = None) -> Path:
        """
        Descomprime arquivo .digilang

        Args:
            compressed_path: Caminho do arquivo comprimido
            output_dir: Diretório de saída (padrão: output/decompressed/)

        Returns:
            Caminho do arquivo descomprimido
        """
        if not compressed_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {compressed_path}")

        # Configurar diretório de saída
        if output_dir is None:
            output_dir = Path("output/decompressed")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Ler arquivo comprimido
        with open(compressed_path, 'r', encoding='utf-8') as f:
            compressed_text = f.read()

        # Ler dicionário
        dict_path = compressed_path.with_suffix('.dict.json')
        if not dict_path.exists():
            raise FileNotFoundError(f"Dicionário não encontrado: {dict_path}")

        with open(dict_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)

        # Descomprimir
        decompressed = self.decompress(compressed_text, dictionary)

        # Salvar arquivo descomprimido
        output_filename = compressed_path.stem.replace('_v22_mega', '').replace('_v27_adaptive', '')
        output_filename += '_decompressed.txt'
        output_path = output_dir / output_filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(decompressed)

        logger.info(f"📁 Arquivo descomprimido salvo: {output_path}")

        return output_path

    def _select_best_version(self, text: str) -> CompressionVersion:
        """
        Seleciona automaticamente a melhor versão baseada no texto

        Args:
            text: Texto a analisar

        Returns:
            Versão recomendada
        """
        text_length = len(text)

        # Heurísticas simples
        if text_length < 50000:  # Textos pequenos/médios
            return CompressionVersion.V27_ADAPTIVE
        elif text_length < 200000:  # Textos médios/grandes
            return CompressionVersion.V22_MEGA
        else:  # Textos muito grandes
            return CompressionVersion.ADAPTIVE

    def get_stats(self) -> Dict:
        """Retorna estatísticas globais do serviço"""
        return {
            **self.stats,
            'versions_available': [v.value for v in self.versions_available.keys()],
            'average_tokens_per_compression': (
                self.stats['total_tokens_saved'] / max(self.stats['total_compressions'], 1)
            ),
            'average_processing_time': (
                self.stats['total_processing_time'] /
                max(self.stats['total_compressions'] + self.stats['total_decompressions'], 1)
            )
        }

    def validate_compression(self, original: str, compressed: str, dictionary: Dict[str, str]) -> bool:
        """
        Valida que a compressão é reversível

        Args:
            original: Texto original
            compressed: Texto comprimido
            dictionary: Dicionário usado

        Returns:
            True se a descompressão retorna ao original
        """
        decompressed = self.decompress(compressed, dictionary)
        is_valid = decompressed == original

        if not is_valid:
            logger.error("❌ Validação falhou: descompressão não retorna ao original")
            # Log das primeiras diferenças
            for i, (c1, c2) in enumerate(zip(original[:100], decompressed[:100])):
                if c1 != c2:
                    logger.error(f"Primeira diferença na posição {i}: '{c1}' != '{c2}'")
                    break

        return is_valid

    def benchmark_versions(self, text: str) -> Dict:
        """
        Compara performance de todas as versões disponíveis

        Args:
            text: Texto para benchmark

        Returns:
            Dicionário com resultados comparativos
        """
        results = {}

        for version in self.versions_available.keys():
            try:
                logger.info(f"🧪 Testando {version.value}...")
                compressed, dictionary, stats = self.compress(text, version)

                # Validar compressão
                is_valid = self.validate_compression(text, compressed, dictionary)

                results[version.value] = {
                    'compression_ratio': stats.get('compression_ratio', 0),
                    'tokens_saved': stats.get('tokens_saved', 0),
                    'processing_time': stats.get('processing_time', 0),
                    'compressed_size': len(compressed),
                    'dictionary_size': len(dictionary),
                    'is_valid': is_valid
                }
            except Exception as e:
                logger.error(f"❌ Erro testando {version.value}: {e}")
                results[version.value] = {'error': str(e)}

        return results


def test_compression_service():
    """Testa o serviço de compressão"""

    service = CompressionService()

    # Texto de teste
    test_text = """FADE IN:

INT. BANK - DAY

The JOKER enters wearing his signature purple suit.

JOKER
Why so serious?

He pulls out a deck of cards.

JOKER (CONT'D)
Let's put a smile on that face!

CUT TO:"""

    print("🧪 TESTANDO COMPRESSION SERVICE")
    print("="*60)

    # Teste de compressão
    print("\n1. Teste de Compressão AUTO:")
    compressed, dictionary, stats = service.compress(test_text)
    print(f"   Versão usada: {stats['version_used']}")
    print(f"   Compressão: {stats.get('compression_ratio', 0):.1%}")
    print(f"   Tokens economizados: {stats.get('tokens_saved', 0)}")

    # Teste de descompressão
    print("\n2. Teste de Descompressão:")
    decompressed = service.decompress(compressed, dictionary)
    is_valid = decompressed == test_text
    print(f"   Validação: {'✅ PASSOU' if is_valid else '❌ FALHOU'}")

    # Benchmark de versões
    print("\n3. Benchmark de Versões:")
    results = service.benchmark_versions(test_text)
    for version, result in results.items():
        if 'error' not in result:
            print(f"   {version}: {result['compression_ratio']:.1%} compressão")

    # Estatísticas globais
    print("\n4. Estatísticas Globais:")
    stats = service.get_stats()
    print(f"   Total compressões: {stats['total_compressions']}")
    print(f"   Total descompressões: {stats['total_decompressions']}")
    print(f"   Tokens economizados: {stats['total_tokens_saved']}")

    print("\n✅ Testes concluídos!")


if __name__ == "__main__":
    test_compression_service()