#!/usr/bin/env python3
"""
🎯 DigiLang Adaptive Selector - Sistema Inteligente de Seleção
Escolhe automaticamente a melhor versão DigiLang baseado nas características do texto

Sistema Hierárquico:
1. V27 MEGA Ultimate (PADRÃO) - Regras definitivas do usuário
2. V22 MEGA (FALLBACK) - Para casos que precisam de mais símbolos
3. V26 Multi-Layer (FALLBACK) - Para textos extremamente complexos
"""

import logging
from typing import Dict, Tuple, Optional
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DigiLangAdaptiveSelector:
    """
    Selector inteligente que escolhe a melhor versão DigiLang
    baseado nas características específicas do texto
    """

    def __init__(self):
        self.versions_available = {}
        self.performance_history = []
        self._load_available_versions()

    def _load_available_versions(self):
        """Carrega as versões DigiLang disponíveis"""
        try:
            from apps.scripturemon.digilang_v27_mega_ultimate import DigiLangV27MegaUltimate
            self.versions_available['v27_mega_ultimate'] = DigiLangV27MegaUltimate
            logger.info("✅ V27 MEGA Ultimate carregado")
        except ImportError:
            logger.warning("⚠️ V27 MEGA Ultimate não disponível")

        try:
            from apps.scripturemon.digilang_v22_mega import DigiLangV22Mega
            self.versions_available['v22_mega'] = DigiLangV22Mega
            logger.info("✅ V22 MEGA carregado")
        except ImportError:
            logger.warning("⚠️ V22 MEGA não disponível")

        try:
            from apps.scripturemon.digilang_v26_mega_multilayer import DigiLangV26MegaMultiLayer
            self.versions_available['v26_multilayer'] = DigiLangV26MegaMultiLayer
            logger.info("✅ V26 Multi-Layer carregado")
        except ImportError:
            logger.warning("⚠️ V26 Multi-Layer não disponível")

        logger.info(f"💎 {len(self.versions_available)} versões DigiLang carregadas")

    def _analyze_text_characteristics(self, text: str) -> Dict:
        """Analisa características do texto para decidir a melhor versão"""
        import tiktoken

        try:
            encoder = tiktoken.get_encoding("cl100k_base")
            tokens = encoder.encode(text)
        except:
            # Fallback se tiktoken não disponível
            tokens = list(range(len(text) // 4))

        characteristics = {
            'text_length': len(text),
            'token_count': len(tokens),
            'lines': text.count('\n'),
            'words': len(text.split()),
            'avg_word_length': sum(len(word) for word in text.split()) / max(len(text.split()), 1),
            'screenplay_patterns': self._count_screenplay_patterns(text),
            'repetitive_patterns': self._count_repetitive_patterns(text),
            'complexity_score': self._calculate_complexity_score(text)
        }

        return characteristics

    def _count_screenplay_patterns(self, text: str) -> int:
        """Conta padrões típicos de roteiro"""
        import re
        patterns = [
            r'FADE IN:', r'FADE OUT\.', r'CUT TO:', r'INT\.', r'EXT\.',
            r'\([A-Za-z\s,]+\)', r'[A-Z]{2,}\n', r'CLOSE UP', r'WIDE SHOT'
        ]

        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, text))

        return count

    def _count_repetitive_patterns(self, text: str) -> int:
        """Conta padrões repetitivos que podem ser otimizados"""
        words = text.split()
        word_freq = {}

        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Contar palavras que aparecem 3+ vezes
        repetitive = sum(1 for freq in word_freq.values() if freq >= 3)
        return repetitive

    def _calculate_complexity_score(self, text: str) -> float:
        """Calcula score de complexidade do texto (0-1)"""
        chars = len(text)
        unique_chars = len(set(text))

        if chars == 0:
            return 0

        # Complexidade = diversidade de caracteres
        complexity = unique_chars / min(chars, 1000)  # Normalizado
        return min(complexity, 1.0)

    def _choose_version_strategy(self, characteristics: Dict) -> str:
        """
        Escolhe a estratégia baseada nas características do texto

        HIERARQUIA DE DECISÃO:
        1. V27 MEGA Ultimate - PADRÃO (95% dos casos)
        2. V22 MEGA - Para textos que precisam de mais símbolos
        3. V26 Multi-Layer - Para textos extremamente complexos
        """

        # REGRA 1: V27 MEGA Ultimate é SEMPRE a primeira opção
        if 'v27_mega_ultimate' in self.versions_available:
            return 'v27_mega_ultimate'

        # REGRA 2: Se V27 não disponível, usar V22 MEGA para textos médios
        if characteristics['token_count'] > 1000 and 'v22_mega' in self.versions_available:
            return 'v22_mega'

        # REGRA 3: V26 Multi-Layer para textos muito complexos
        if (characteristics['complexity_score'] > 0.8 and
            characteristics['token_count'] > 5000 and
            'v26_multilayer' in self.versions_available):
            return 'v26_multilayer'

        # FALLBACK: Primeira versão disponível
        return list(self.versions_available.keys())[0]

    def compress_adaptive(self, text: str, force_version: Optional[str] = None) -> Tuple[str, Dict, Dict]:
        """
        Comprime texto escolhendo automaticamente a melhor versão

        Args:
            text: Texto a comprimir
            force_version: Força uso de uma versão específica (opcional)

        Returns:
            Tupla (texto_comprimido, dicionário_substituições, estatísticas)
        """
        logger.info("🎯 DigiLang Adaptive Selector - Iniciando compressão inteligente")
        start_time = time.time()

        if not self.versions_available:
            raise RuntimeError("❌ Nenhuma versão DigiLang disponível")

        # Analisar características do texto
        characteristics = self._analyze_text_characteristics(text)

        # Escolher versão (ou usar forçada)
        if force_version and force_version in self.versions_available:
            chosen_version = force_version
            logger.info(f"🔧 Versão forçada: {chosen_version}")
        else:
            chosen_version = self._choose_version_strategy(characteristics)
            logger.info(f"🤖 Versão escolhida automaticamente: {chosen_version}")

        # Log das características
        logger.info(f"📊 Características do texto:")
        logger.info(f"   Tamanho: {characteristics['text_length']:,} chars")
        logger.info(f"   Tokens: {characteristics['token_count']:,}")
        logger.info(f"   Complexidade: {characteristics['complexity_score']:.2f}")
        logger.info(f"   Padrões de roteiro: {characteristics['screenplay_patterns']}")

        # Comprimir com a versão escolhida
        try:
            compressor_class = self.versions_available[chosen_version]
            compressor = compressor_class()

            # Adaptar chamada baseado na versão
            if chosen_version == 'v27_mega_ultimate':
                compressed, replacement_map, stats = compressor.compress(text)
            elif chosen_version == 'v22_mega':
                # Adaptar para interface do V22
                compressed, replacement_map, stats = compressor.compress(text)
            elif chosen_version == 'v26_multilayer':
                # Adaptar para interface do V26
                compressed, layers, stats = compressor.compress(text)
                replacement_map = {}  # V26 usa layers em vez de replacement_map
            else:
                # Interface genérica
                compressed, replacement_map, stats = compressor.compress(text)

            # Adicionar metadados do selector
            stats.update({
                'version_used': chosen_version,
                'text_characteristics': characteristics,
                'selection_time': time.time() - start_time,
                'adaptive_selector': True
            })

            # Registrar performance para futuras decisões
            self.performance_history.append({
                'version': chosen_version,
                'compression_ratio': stats.get('compression_ratio', 0),
                'text_size': characteristics['text_length'],
                'complexity': characteristics['complexity_score']
            })

            logger.info(f"✅ Compressão concluída com {chosen_version}")
            logger.info(f"📊 Taxa de compressão: {stats.get('compression_ratio', 0):.1%}")

            return compressed, replacement_map, stats

        except Exception as e:
            logger.error(f"❌ Erro na compressão com {chosen_version}: {e}")

            # Tentar fallback para outra versão
            for fallback_version in self.versions_available.keys():
                if fallback_version != chosen_version:
                    logger.info(f"🔄 Tentando fallback: {fallback_version}")
                    try:
                        return self.compress_adaptive(text, force_version=fallback_version)
                    except:
                        continue

            raise RuntimeError(f"❌ Todas as versões falharam na compressão")

    def get_performance_report(self) -> Dict:
        """Gera relatório de performance das versões"""
        if not self.performance_history:
            return {"message": "Nenhum histórico de performance disponível"}

        report = {
            'total_compressions': len(self.performance_history),
            'versions_used': {},
            'average_compression': 0,
            'best_compression': 0
        }

        total_compression = 0
        best_compression = 0

        for record in self.performance_history:
            version = record['version']
            compression = record['compression_ratio']

            if version not in report['versions_used']:
                report['versions_used'][version] = {'count': 0, 'avg_compression': 0}

            report['versions_used'][version]['count'] += 1
            report['versions_used'][version]['avg_compression'] += compression

            total_compression += compression
            best_compression = max(best_compression, compression)

        # Calcular médias
        if self.performance_history:
            report['average_compression'] = total_compression / len(self.performance_history)
            report['best_compression'] = best_compression

        for version_data in report['versions_used'].values():
            if version_data['count'] > 0:
                version_data['avg_compression'] /= version_data['count']

        return report

    def test_all_versions(self, text: str) -> Dict:
        """Testa todas as versões disponíveis para comparação"""
        results = {}

        for version_name in self.versions_available.keys():
            try:
                logger.info(f"🧪 Testando {version_name}...")
                compressed, replacement_map, stats = self.compress_adaptive(text, force_version=version_name)
                results[version_name] = {
                    'compression_ratio': stats.get('compression_ratio', 0),
                    'tokens_saved': stats.get('tokens_saved', 0),
                    'processing_time': stats.get('processing_time', 0),
                    'success': True
                }
            except Exception as e:
                results[version_name] = {
                    'success': False,
                    'error': str(e)
                }

        return results


def test_adaptive_selector():
    """Testa o sistema adaptativo com texto do Batman"""

    batman_text = '''FADE IN:

EXT. GOTHAM CITY - ROOFTOP - NIGHT

The city sprawls below, a maze of shadows and neon. BATMAN stands on the edge of a skyscraper, cape billowing in the wind.

BATMAN
(into comm)
Alfred, I'm seeing movement in the warehouse district.

CUT TO:

INT. ABANDONED WAREHOUSE - NIGHT

THE JOKER paces among crates of stolen weapons.

JOKER
(maniacal laugh)
Tonight, Gotham will see what true chaos looks like!

FADE OUT.'''

    print("🦇 TESTE DO SISTEMA ADAPTATIVO")
    print("="*60)

    # Criar selector
    selector = DigiLangAdaptiveSelector()

    # Teste automático
    print("\n🤖 COMPRESSÃO AUTOMÁTICA:")
    print("-"*40)
    compressed, replacement_map, stats = selector.compress_adaptive(batman_text)

    print(f"Versão escolhida: {stats['version_used']}")
    print(f"Compressão: {stats['compression_ratio']:.1%}")
    print(f"Tokens economizados: {stats.get('tokens_saved', 0)}")

    # Teste de todas as versões
    print("\n🔬 COMPARAÇÃO DE TODAS AS VERSÕES:")
    print("-"*40)
    comparison = selector.test_all_versions(batman_text)

    for version, result in comparison.items():
        if result['success']:
            print(f"{version}: {result['compression_ratio']:.1%} compressão")
        else:
            print(f"{version}: ERRO - {result['error']}")

    # Relatório de performance
    print("\n📊 RELATÓRIO DE PERFORMANCE:")
    print("-"*40)
    report = selector.get_performance_report()
    print(f"Total de compressões: {report['total_compressions']}")
    print(f"Compressão média: {report['average_compression']:.1%}")
    print(f"Melhor compressão: {report['best_compression']:.1%}")

if __name__ == "__main__":
    test_adaptive_selector()