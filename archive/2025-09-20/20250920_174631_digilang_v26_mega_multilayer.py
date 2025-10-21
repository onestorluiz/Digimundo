#!/usr/bin/env python3
"""
🚀 DigiLang V26 MEGA Multi-Layer - O Melhor dos Dois Mundos
Combina:
- Base sólida do V22 MEGA (15.29% compressão comprovada)
- Arquitetura multi-layer do TPD (múltiplas passadas)

Estratégia: V22 MEGA como Camada 1, depois aplicar camadas adicionais
"""

import logging
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter
import re
import json
from pathlib import Path
import time
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MegaPattern:
    """Estrutura para armazenar padrões com economia calculada"""
    text: str
    frequency: int
    original_tokens: int
    potential_savings_1token: int
    potential_savings_2token: int
    potential_savings_3token: int

class DigiLangV26MegaMultiLayer:
    """
    DigiLang V26 - V22 MEGA + Multi-Layer TPD
    Usa V22 MEGA como base e aplica múltiplas camadas adicionais
    """

    def __init__(self, max_layers: int = 4):
        self.max_layers = max_layers
        self.layers = []
        self.symbols_used = set()

        # Importar tiktoken
        try:
            import tiktoken
            self.encoder = tiktoken.get_encoding("cl100k_base")
            self.tiktoken_available = True
        except ImportError:
            logger.warning("⚠️ tiktoken não disponível")
            self.tiktoken_available = False
            self.encoder = None

        # Descobrir TODOS os símbolos como V22 MEGA
        self.symbols_1token = self._discover_all_1token_symbols()
        self.symbols_2token = self._discover_all_2token_symbols()
        self.symbols_3token = self._discover_all_3token_symbols()

        logger.info(f"💎 Símbolos descobertos: {len(self.symbols_1token)} (1-token), {len(self.symbols_2token)} (2-token), {len(self.symbols_3token)} (3-token)")

    def _discover_all_1token_symbols(self) -> List[str]:
        """Descobrir símbolos de 1 token - EXATAMENTE como V22 MEGA"""
        symbols = []

        # Ranges exatos do V22 MEGA
        ranges = [
            (0x2500, 0x257F),   # Box Drawing
            (0x2580, 0x259F),   # Block Elements
            (0x25A0, 0x25FF),   # Geometric Shapes
            (0x2600, 0x26FF),   # Miscellaneous Symbols
            (0x2700, 0x27BF),   # Dingbats
            (0x2800, 0x28FF),   # Braille
            (0x2900, 0x297F),   # Supplemental Arrows-B
            (0x2B00, 0x2BFF),   # Miscellaneous Symbols and Arrows
            (0x1F300, 0x1F5FF), # Miscellaneous Symbols and Pictographs
            (0x1F600, 0x1F64F), # Emoticons
            (0x1F680, 0x1F6FF), # Transport and Map
            (0x1F900, 0x1F9FF), # Supplemental Symbols
            # CJK ranges
            (0x4E00, 0x9FFF),   # CJK Unified Ideographs
            (0x3400, 0x4DBF),   # CJK Extension A
            (0x3040, 0x309F),   # Hiragana
            (0x30A0, 0x30FF),   # Katakana
            # Scripts
            (0x0590, 0x05FF),   # Hebrew
            (0x0600, 0x06FF),   # Arabic
            (0x0900, 0x097F),   # Devanagari
            (0x0980, 0x09FF),   # Bengali
            (0x0E00, 0x0E7F),   # Thai
        ]

        for start, end in ranges:
            for codepoint in range(start, min(end + 1, 0x110000)):
                try:
                    char = chr(codepoint)
                    if self.tiktoken_available:
                        if len(self.encoder.encode(char)) == 1:
                            if char not in [' ', '\n', '\t', '\r', '\x00']:
                                symbols.append(char)
                    else:
                        symbols.append(char)
                except:
                    pass

        return symbols

    def _discover_all_2token_symbols(self) -> List[str]:
        """Descobrir símbolos de 2 tokens - EXATAMENTE como V22 MEGA"""
        symbols = []

        combos = ['##', '@@', '$$', '%%', '&&', '**', '++', '--', '//', '::',
                  '<<', '>>', '==', '!=', '<=', '>=', '||', '&&', '~~', '``']

        for combo in combos:
            if self.tiktoken_available:
                if len(self.encoder.encode(combo)) == 2:
                    symbols.append(combo)
            else:
                symbols.append(combo)

        # Emojis de 2 tokens
        emoji_ranges = [
            (0x1F300, 0x1F5FF),
            (0x1F600, 0x1F64F),
            (0x1F680, 0x1F6FF),
            (0x1F900, 0x1F9FF),
        ]

        for start, end in emoji_ranges:
            for codepoint in range(start, min(end + 1, 0x110000)):
                try:
                    char = chr(codepoint)
                    if self.tiktoken_available:
                        if len(self.encoder.encode(char)) == 2:
                            symbols.append(char)
                except:
                    pass

        return symbols[:1000]

    def _discover_all_3token_symbols(self) -> List[str]:
        """Descobrir símbolos de 3 tokens - EXATAMENTE como V22 MEGA"""
        symbols = []

        combos = ['###', '@@@', '$$$', '%%%', '&&&', '***', '+++', '---', '///', ':::',
                  '<<<', '>>>', '===', '!==', '<==', '>==', '|||', '&&&', '~~~', '```']

        for combo in combos:
            if self.tiktoken_available:
                if len(self.encoder.encode(combo)) == 3:
                    symbols.append(combo)
            else:
                symbols.append(combo)

        # Emojis compostos
        composite_emojis = ['👨‍👩‍👧', '👨‍👩‍👦', '👨‍👨‍👦', '👩‍👩‍👧', '🏳️‍🌈', '🏴‍☠️']

        for emoji in composite_emojis:
            if self.tiktoken_available:
                token_count = len(self.encoder.encode(emoji))
                if token_count == 3:
                    symbols.append(emoji)

        return symbols[:100]

    def mine_all_patterns(self, text: str) -> List[MegaPattern]:
        """Minerar TODOS os padrões - EXATAMENTE como V22 MEGA"""
        patterns = []

        logger.info("⛏️ Minerando TODOS os padrões do texto...")

        # 1. Extrair TODAS as palavras individuais
        words = re.findall(r'\b[\w\']+\b', text)
        word_freq = Counter(words)

        for word, freq in word_freq.items():
            if not self.tiktoken_available:
                original_tokens = len(word) // 4  # Estimativa
            else:
                original_tokens = len(self.encoder.encode(word))

            # Calcular economia para cada tipo de símbolo
            savings_1 = (original_tokens - 1) * freq if original_tokens > 1 else 0
            savings_2 = (original_tokens - 2) * freq if original_tokens > 2 else 0
            savings_3 = (original_tokens - 3) * freq if original_tokens > 3 else 0

            if savings_1 > 0:
                patterns.append(MegaPattern(
                    text=word,
                    frequency=freq,
                    original_tokens=original_tokens,
                    potential_savings_1token=savings_1,
                    potential_savings_2token=savings_2,
                    potential_savings_3token=savings_3
                ))

        # 2. Extrair frases comuns (2-5 palavras)
        for n in range(2, 6):
            ngrams = []
            words_list = text.split()

            for i in range(len(words_list) - n + 1):
                ngram = ' '.join(words_list[i:i+n])
                if len(ngram) < 100:
                    ngrams.append(ngram)

            ngram_freq = Counter(ngrams)

            for ngram, freq in ngram_freq.items():
                if freq > 2:
                    if not self.tiktoken_available:
                        original_tokens = len(ngram) // 4
                    else:
                        original_tokens = len(self.encoder.encode(ngram))

                    savings_1 = (original_tokens - 1) * freq if original_tokens > 1 else 0
                    savings_2 = (original_tokens - 2) * freq if original_tokens > 2 else 0
                    savings_3 = (original_tokens - 3) * freq if original_tokens > 3 else 0

                    if savings_1 > 0:
                        patterns.append(MegaPattern(
                            text=ngram,
                            frequency=freq,
                            original_tokens=original_tokens,
                            potential_savings_1token=savings_1,
                            potential_savings_2token=savings_2,
                            potential_savings_3token=savings_3
                        ))

        # 3. Elementos técnicos de roteiro
        tech_elements = [
            'FADE IN:', 'FADE OUT', 'CUT TO:', 'DISSOLVE TO:', 'CONTINUED:',
            'INT.', 'EXT.', 'INT/EXT', 'V.O.', 'O.S.', 'CONT\'D',
            'DAY', 'NIGHT', 'CONTINUOUS', 'LATER', 'MOMENTS LATER'
        ]

        for element in tech_elements:
            freq = text.count(element)
            if freq > 0:
                if not self.tiktoken_available:
                    original_tokens = len(element) // 4
                else:
                    original_tokens = len(self.encoder.encode(element))

                savings_1 = (original_tokens - 1) * freq if original_tokens > 1 else 0
                savings_2 = (original_tokens - 2) * freq if original_tokens > 2 else 0
                savings_3 = (original_tokens - 3) * freq if original_tokens > 3 else 0

                if savings_1 > 0:
                    patterns.append(MegaPattern(
                        text=element,
                        frequency=freq,
                        original_tokens=original_tokens,
                        potential_savings_1token=savings_1,
                        potential_savings_2token=savings_2,
                        potential_savings_3token=savings_3
                    ))

        logger.info(f"📊 Padrões minerados: {len(patterns)}")
        return patterns

    def apply_v22_mega_layer(self, text: str) -> Tuple[str, Dict[str, str], Dict]:
        """
        Aplica EXATAMENTE o algoritmo do V22 MEGA como primeira camada
        """
        logger.info("🔨 Aplicando Camada V22 MEGA")

        # Minerar padrões exatamente como V22 MEGA
        patterns = self.mine_all_patterns(text)

        # Ordenar por economia total de 1-token (estratégia V22 MEGA)
        patterns.sort(key=lambda p: p.potential_savings_1token, reverse=True)

        # Construir dicionário usando símbolos de 1-token primeiro
        dictionary = {}
        available_symbols = [s for s in self.symbols_1token if s not in self.symbols_used]

        # Aplicar até 1000 padrões como V22 MEGA
        for pattern in patterns[:1000]:
            if not available_symbols:
                break

            symbol = available_symbols.pop(0)
            dictionary[pattern.text] = symbol
            self.symbols_used.add(symbol)

        # Aplicar substituições
        compressed = text
        total_replacements = 0
        total_savings = 0

        # Ordenar por tamanho (maiores primeiro)
        sorted_patterns = sorted(dictionary.items(), key=lambda x: len(x[0]), reverse=True)

        for pattern, symbol in sorted_patterns:
            if pattern in compressed:
                count = compressed.count(pattern)
                compressed = compressed.replace(pattern, symbol)
                total_replacements += count

                # Calcular economia real
                if self.tiktoken_available:
                    original_tokens = len(self.encoder.encode(pattern))
                    savings = (original_tokens - 1) * count
                    total_savings += savings

        # Calcular estatísticas
        if self.tiktoken_available:
            original_tokens = len(self.encoder.encode(text))
            compressed_tokens = len(self.encoder.encode(compressed))
        else:
            original_tokens = len(text) // 4
            compressed_tokens = len(compressed) // 4

        compression_ratio = 1 - (compressed_tokens / original_tokens)

        stats = {
            'layer': 'V22_MEGA',
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'compression_ratio': compression_ratio,
            'patterns_used': len(dictionary),
            'replacements': total_replacements,
            'token_savings': total_savings
        }

        logger.info(f"✅ Camada V22 MEGA: {compression_ratio:.1%} compressão")
        logger.info(f"   Padrões: {len(dictionary)}, Substituições: {total_replacements:,}")

        return compressed, dictionary, stats

    def apply_additional_layer(self, text: str, layer_num: int) -> Tuple[str, Dict[str, str], Dict]:
        """
        Aplica camadas adicionais após V22 MEGA
        """
        logger.info(f"🔨 Aplicando Camada Adicional {layer_num}")

        # Re-minerar padrões do texto já comprimido
        patterns = self.mine_all_patterns(text)

        # Estratégia: focar em padrões menores que restaram
        patterns.sort(key=lambda p: p.potential_savings_1token, reverse=True)

        # Usar símbolos restantes
        dictionary = {}
        available_symbols = [s for s in self.symbols_1token if s not in self.symbols_used]

        # Se esgotaram símbolos de 1-token, usar 2-token
        if not available_symbols:
            available_symbols = [s for s in self.symbols_2token if s not in self.symbols_used]

        # Aplicar padrões (menos que primeira camada)
        max_patterns = max(200, 800 - layer_num * 150)
        for pattern in patterns[:max_patterns]:
            if not available_symbols:
                break

            symbol = available_symbols.pop(0)
            dictionary[pattern.text] = symbol
            self.symbols_used.add(symbol)

        # Aplicar substituições
        compressed = text
        total_replacements = 0
        total_savings = 0

        sorted_patterns = sorted(dictionary.items(), key=lambda x: len(x[0]), reverse=True)

        for pattern, symbol in sorted_patterns:
            if pattern in compressed:
                count = compressed.count(pattern)
                compressed = compressed.replace(pattern, symbol)
                total_replacements += count

                if self.tiktoken_available:
                    original_tokens = len(self.encoder.encode(pattern))
                    # Ajustar economia se usando símbolos de 2-token
                    replacement_cost = 2 if symbol in self.symbols_2token else 1
                    savings = (original_tokens - replacement_cost) * count
                    total_savings += max(0, savings)

        # Calcular estatísticas
        if self.tiktoken_available:
            original_tokens = len(self.encoder.encode(text))
            compressed_tokens = len(self.encoder.encode(compressed))
        else:
            original_tokens = len(text) // 4
            compressed_tokens = len(compressed) // 4

        compression_ratio = 1 - (compressed_tokens / original_tokens) if original_tokens > 0 else 0

        stats = {
            'layer': layer_num,
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'compression_ratio': compression_ratio,
            'patterns_used': len(dictionary),
            'replacements': total_replacements,
            'token_savings': total_savings
        }

        logger.info(f"✅ Camada {layer_num}: {compression_ratio:.1%} compressão")
        logger.info(f"   Padrões: {len(dictionary)}, Substituições: {total_replacements:,}")

        return compressed, dictionary, stats

    def compress(self, text: str) -> Tuple[str, List[Dict], Dict]:
        """
        Comprime usando V22 MEGA + camadas adicionais
        """
        logger.info("="*60)
        logger.info("🚀 DigiLang V26 MEGA Multi-Layer - Iniciando")
        logger.info("="*60)

        start_time = time.time()

        # Reset state
        self.layers = []
        self.symbols_used = set()
        current_text = text

        # Contar tokens originais
        if self.tiktoken_available:
            initial_tokens = len(self.encoder.encode(text))
        else:
            initial_tokens = len(text) // 4

        logger.info(f"📄 Texto original: {len(text):,} chars, {initial_tokens:,} tokens")

        layer_stats = []

        # CAMADA 1: V22 MEGA completo
        compressed_text, layer_dict, stats = self.apply_v22_mega_layer(current_text)
        self.layers.append(layer_dict)
        layer_stats.append(stats)
        current_text = compressed_text

        # CAMADAS ADICIONAIS: Aplicar até não haver ganho
        for layer in range(2, self.max_layers + 1):
            compressed_text, layer_dict, stats = self.apply_additional_layer(current_text, layer)
            self.layers.append(layer_dict)
            layer_stats.append(stats)

            # Se não houve compressão significativa, parar
            if stats['compression_ratio'] < 0.005:  # Menos de 0.5% de ganho
                logger.info(f"⚠️ Camada {layer} sem ganho significativo, parando")
                break

            current_text = compressed_text

        # Estatísticas finais
        if self.tiktoken_available:
            final_tokens = len(self.encoder.encode(current_text))
        else:
            final_tokens = len(current_text) // 4

        total_compression = 1 - (final_tokens / initial_tokens)

        final_stats = {
            'total_layers': len(self.layers),
            'original_chars': len(text),
            'compressed_chars': len(current_text),
            'original_tokens': initial_tokens,
            'final_tokens': final_tokens,
            'total_compression': total_compression,
            'tokens_saved': initial_tokens - final_tokens,
            'total_patterns': sum(len(layer) for layer in self.layers),
            'processing_time': time.time() - start_time,
            'layers': layer_stats
        }

        logger.info("\n" + "="*60)
        logger.info("🎯 RESULTADOS FINAIS V26 MEGA MULTI-LAYER")
        logger.info("="*60)
        logger.info(f"📊 Compressão Total: {total_compression:.1%}")
        logger.info(f"💾 Tokens: {initial_tokens:,} → {final_tokens:,}")
        logger.info(f"💰 Economia: {initial_tokens - final_tokens:,} tokens")
        logger.info(f"🔢 Padrões totais: {final_stats['total_patterns']:,}")
        logger.info(f"📚 Camadas usadas: {final_stats['total_layers']}")
        logger.info(f"⏱️ Tempo: {final_stats['processing_time']:.2f}s")
        logger.info("="*60)

        return current_text, self.layers, final_stats

    def decompress(self, compressed_text: str, layers: List[Dict] = None) -> str:
        """Descomprime texto - reverso da compressão multi-layer"""
        # Usar layers fornecidas ou self.layers
        layers_to_use = layers if layers is not None else self.layers

        if not layers_to_use:
            return compressed_text

        # Reverter cada camada em ordem reversa
        decompressed = compressed_text

        for layer_dict in reversed(layers_to_use):
            # IMPORTANTE: layer_dict tem pattern -> symbol, precisamos symbol -> pattern
            # Inverter o dicionário para descompressão
            reverse_dict = {symbol: pattern for pattern, symbol in layer_dict.items()}

            # Reverter substituições da camada (ordenar por tamanho do símbolo para evitar conflitos)
            for symbol, pattern in sorted(reverse_dict.items(), key=lambda x: len(x[0]), reverse=True):
                decompressed = decompressed.replace(symbol, pattern)

        # IMPORTANTE: NÃO usar strip() que remove caracteres importantes
        return decompressed


def test_v26_with_dark_knight():
    """Testa V26 MEGA Multi-Layer com The Dark Knight COMPLETO"""
    from pathlib import Path

    # Carregar texto
    txt_path = Path('data/original/The_Dark_Knight_-_Release.txt')
    if not txt_path.exists():
        print("❌ Arquivo não encontrado")
        return

    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Usar texto COMPLETO como V22 MEGA
    print(f"\n{'='*60}")
    print("🎬 TESTE COM THE DARK KNIGHT COMPLETO")
    print(f"{'='*60}")
    print(f"📄 Texto completo: {len(text):,} chars")

    # Comprimir
    compressor = DigiLangV26MegaMultiLayer(max_layers=5)
    compressed, layers, stats = compressor.compress(text)

    # Comparar com outras versões
    print(f"\n🔥 COMPARAÇÃO FINAL:")
    print(f"  V8.1 Supreme: 0.72% compressão")
    print(f"  V19 Personalized: 7.61% compressão")
    print(f"  V22 MEGA: 15.29% compressão (BASELINE)")
    print(f"  V24 Ultimate PT: 4.7% compressão")
    print(f"  V25 Hybrid Ultimate: 7.6% compressão")
    print(f"  V26 MEGA MULTI-LAYER: {stats['total_compression']:.1%} compressão")

    if stats['total_compression'] > 0.30:
        print(f"  🏆 RECORDE MUNDIAL! Superou 30%!")
    elif stats['total_compression'] > 0.25:
        print(f"  🏆 RECORDE ABSOLUTO! Superou 25%!")
    elif stats['total_compression'] > 0.20:
        print(f"  🏆 NOVO RECORDE! Superou 20%!")
    elif stats['total_compression'] > 0.1529:
        print(f"  ✅ MELHOR que V22 MEGA!")
    else:
        diff = (0.1529 - stats['total_compression']) * 100
        print(f"  ⚠️ Ainda {diff:.1f}% abaixo do V22 MEGA")

    return stats


if __name__ == "__main__":
    test_v26_with_dark_knight()