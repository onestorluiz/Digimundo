#!/usr/bin/env python3
"""
🚀 DigiLang V25 Hybrid Ultimate - Sistema Definitivo
Combina as melhores técnicas de todos os sistemas:
- Mining personalizado do V22 MEGA (15.29% compressão)
- Símbolos abundantes (1,218 símbolos)
- Multi-layer do TPD
- Otimização token-aware
"""

import logging
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter
import re
import json
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DigiLangV25HybridUltimate:
    """
    DigiLang V25 - Sistema híbrido definitivo
    Combina V22 MEGA + TPD Multi-layer + mining personalizado
    """

    def __init__(self, max_layers: int = 3):
        self.max_layers = max_layers
        self.layers = []  # Lista de dicionários por camada
        self.symbols_used = set()

        # Importar tiktoken PRIMEIRO
        try:
            import tiktoken
            self.encoder = tiktoken.get_encoding("cl100k_base")
            self.tiktoken_available = True
        except ImportError:
            logger.warning("⚠️ tiktoken não disponível")
            self.tiktoken_available = False
            self.encoder = None

        # DEPOIS descobrir símbolos
        self.all_symbols = self._discover_all_1token_symbols()

    def _discover_all_1token_symbols(self) -> List[str]:
        """Descobre TODOS os símbolos Unicode de 1 token - baseado no V22 MEGA"""
        symbols = []

        # Ranges expandidos do V22 MEGA
        ranges = [
            # Basic Unicode ranges
            (0x2500, 0x257F),   # Box Drawing
            (0x2580, 0x259F),   # Block Elements
            (0x25A0, 0x25FF),   # Geometric Shapes
            (0x2600, 0x26FF),   # Miscellaneous Symbols
            (0x2700, 0x27BF),   # Dingbats
            (0x2800, 0x28FF),   # Braille
            (0x2900, 0x297F),   # Supplemental Arrows-B
            (0x2B00, 0x2BFF),   # Miscellaneous Symbols and Arrows

            # Emoji ranges
            (0x1F300, 0x1F5FF), # Miscellaneous Symbols and Pictographs
            (0x1F600, 0x1F64F), # Emoticons
            (0x1F680, 0x1F6FF), # Transport and Map
            (0x1F900, 0x1F9FF), # Supplemental Symbols

            # CJK ranges (many are 1 token)
            (0x4E00, 0x9FFF),   # CJK Unified Ideographs
            (0x3400, 0x4DBF),   # CJK Extension A
            (0x3040, 0x309F),   # Hiragana
            (0x30A0, 0x30FF),   # Katakana

            # Other scripts
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
                        try:
                            if len(self.encoder.encode(char)) == 1:
                                # Excluir apenas espaço e controles básicos
                                if char not in [' ', '\n', '\t', '\r', '\x00']:
                                    symbols.append(char)
                        except:
                            pass
                    else:
                        symbols.append(char)  # Assumir que é 1 token
                except ValueError:
                    continue

        logger.info(f"💎 Descobertos {len(symbols)} símbolos de 1 token")
        return symbols

    def _mine_personalized_patterns(self, text: str) -> Dict[str, int]:
        """
        Mining personalizado baseado no V22 MEGA
        Foca em padrões específicos do documento
        """
        patterns = Counter()

        # 1. Extrair nomes de personagens (CAPS seguido de diálogo)
        character_names = re.findall(r'\n([A-Z][A-Z\s]{2,25})\n', text)
        for name in character_names:
            name = name.strip()
            if name and not any(skip in name for skip in ['INT', 'EXT', 'FADE', 'CUT', 'CLOSE', 'WIDE']):
                patterns[name] += 10  # High priority for character names

        # 2. Locações (INT./EXT. patterns)
        locations = re.findall(r'((?:INT|EXT)\.\s+[A-Z\s\-]+)', text)
        for location in locations:
            if len(location) > 10:
                patterns[location.strip()] += 8

        # 3. Direções de cena entre parênteses
        directions = re.findall(r'\(([A-Za-z\s,]+)\)', text)
        for direction in directions:
            if len(direction) > 5 and len(direction) < 30:
                patterns[f"({direction})"] += 5

        # 4. Palavras frequentes de 2+ tokens
        words = re.findall(r'\b[A-Za-z]+\b', text)
        word_counts = Counter(words)

        for word, freq in word_counts.items():
            if self.tiktoken_available:
                tokens = self.encoder.encode(word)
                if len(tokens) >= 2 and freq >= 3:  # Multi-token words
                    patterns[word] += freq
            else:
                if len(word) >= 6 and freq >= 3:  # Approximation
                    patterns[word] += freq

        # 5. Frases comuns específicas do roteiro
        common_phrases = [
            'FADE IN:', 'FADE OUT.', 'CUT TO:', 'CLOSE UP', 'WIDE SHOT',
            'LATER', 'MEANWHILE', 'SUDDENLY', 'CONTINUING:'
        ]

        for phrase in common_phrases:
            count = text.count(phrase)
            if count > 0:
                patterns[phrase] += count * 3

        # 6. Bigramas e trigramas de alta frequência
        words_clean = [w for w in words if len(w) > 2]
        for i in range(len(words_clean) - 1):
            if i < len(words_clean) - 1:
                bigram = f"{words_clean[i]} {words_clean[i+1]}"
                if word_counts[words_clean[i]] >= 2 and word_counts[words_clean[i+1]] >= 2:
                    patterns[bigram] += 1

        logger.info(f"⛏️ Mining personalizado: {len(patterns)} padrões únicos")
        return patterns

    def _calculate_token_savings(self, pattern: str, frequency: int) -> int:
        """Calcula economia real em tokens"""
        if self.tiktoken_available:
            original_tokens = len(self.encoder.encode(pattern))
            replacement_tokens = 1  # Substituído por 1 símbolo
            savings = (original_tokens - replacement_tokens) * frequency
        else:
            # Estimativa: 1 token ≈ 4 chars
            original_tokens = len(pattern) // 4
            savings = max(0, (original_tokens - 1) * frequency)

        return max(0, savings)

    def _select_optimal_patterns(self, patterns: Dict[str, int], max_patterns: int = 1500) -> Dict[str, str]:
        """
        Seleção ótima de padrões baseada em economia total de tokens
        Similar ao V22 MEGA mas com limite ajustável
        """
        # Calcular economia total para cada padrão
        pattern_economics = []
        for pattern, freq in patterns.items():
            savings = self._calculate_token_savings(pattern, freq)
            if savings > 0:  # Só incluir padrões que economizam tokens
                pattern_economics.append((pattern, freq, savings))

        # Ordenar por economia total (descending)
        pattern_economics.sort(key=lambda x: x[2], reverse=True)

        # Selecionar os melhores padrões
        selected = {}
        available_symbols = [s for s in self.all_symbols if s not in self.symbols_used]

        for pattern, freq, savings in pattern_economics[:max_patterns]:
            if not available_symbols:
                logger.warning(f"⚠️ Sem símbolos disponíveis, parando em {len(selected)} padrões")
                break

            symbol = available_symbols.pop(0)
            selected[pattern] = symbol
            self.symbols_used.add(symbol)

        logger.info(f"✅ Selecionados {len(selected)} padrões ótimos")
        return selected

    def _apply_substitutions(self, text: str, dictionary: Dict[str, str]) -> Tuple[str, int, int]:
        """
        Aplica substituições ordenadas por tamanho
        Retorna: (texto_comprimido, substituições_feitas, tokens_economizados)
        """
        compressed = text
        total_replacements = 0
        total_savings = 0

        # Ordenar por tamanho (maiores primeiro) para evitar sobreposição
        sorted_patterns = sorted(dictionary.items(), key=lambda x: len(x[0]), reverse=True)

        for pattern, symbol in sorted_patterns:
            if pattern in compressed:
                count = compressed.count(pattern)
                compressed = compressed.replace(pattern, symbol)
                total_replacements += count

                # Calcular economia real
                savings = self._calculate_token_savings(pattern, count)
                total_savings += savings

        return compressed, total_replacements, total_savings

    def build_layer(self, text: str, layer_num: int) -> Tuple[Dict[str, str], str, Dict]:
        """
        Constrói uma camada de compressão
        """
        logger.info(f"\n🔨 Construindo Camada {layer_num + 1}")

        # Contar tokens originais
        if self.tiktoken_available:
            original_tokens = len(self.encoder.encode(text))
        else:
            original_tokens = len(text) // 4

        logger.info(f"📊 Tokens originais: {original_tokens:,}")

        # Mining personalizado de padrões
        patterns = self._mine_personalized_patterns(text)

        # Ajustar número de padrões por camada
        max_patterns = max(500, 2000 - layer_num * 300)  # Reduzir em camadas posteriores

        # Selecionar padrões ótimos
        dictionary = self._select_optimal_patterns(patterns, max_patterns)

        # Aplicar substituições
        compressed, replacements, token_savings = self._apply_substitutions(text, dictionary)

        # Calcular estatísticas
        if self.tiktoken_available:
            compressed_tokens = len(self.encoder.encode(compressed))
        else:
            compressed_tokens = len(compressed) // 4

        compression_ratio = 1 - (compressed_tokens / original_tokens) if original_tokens > 0 else 0

        stats = {
            'layer': layer_num + 1,
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'compression_ratio': compression_ratio,
            'patterns_used': len(dictionary),
            'replacements': replacements,
            'token_savings': token_savings
        }

        logger.info(f"✅ Camada {layer_num + 1}: {compression_ratio:.1%} compressão")
        logger.info(f"   Substituições: {replacements:,}")
        logger.info(f"   Economia: {token_savings:,} tokens")

        return dictionary, compressed, stats

    def compress(self, text: str) -> Tuple[str, List[Dict], Dict]:
        """
        Comprime texto usando múltiplas camadas
        """
        logger.info("="*60)
        logger.info("🚀 DigiLang V25 Hybrid Ultimate - Iniciando compressão")
        logger.info("="*60)

        start_time = time.time()

        self.layers = []
        layer_stats = []
        current_text = text

        # Contar tokens originais
        if self.tiktoken_available:
            initial_tokens = len(self.encoder.encode(text))
        else:
            initial_tokens = len(text) // 4

        logger.info(f"📄 Texto original: {len(text):,} chars, {initial_tokens:,} tokens")

        for layer in range(self.max_layers):
            # Construir camada
            dictionary, compressed_text, stats = self.build_layer(current_text, layer)
            self.layers.append(dictionary)
            layer_stats.append(stats)

            # Se não houve compressão significativa, parar
            if stats['compression_ratio'] < 0.005:  # Menos de 0.5% de ganho
                logger.info(f"⚠️ Camada {layer + 1} sem ganho significativo, parando")
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
        logger.info("🎯 RESULTADOS FINAIS V25 HYBRID ULTIMATE")
        logger.info("="*60)
        logger.info(f"📊 Compressão Total: {total_compression:.1%}")
        logger.info(f"💾 Tokens: {initial_tokens:,} → {final_tokens:,}")
        logger.info(f"💰 Economia: {initial_tokens - final_tokens:,} tokens")
        logger.info(f"🔢 Padrões totais: {final_stats['total_patterns']:,}")
        logger.info(f"📚 Camadas usadas: {final_stats['total_layers']}")
        logger.info(f"⏱️ Tempo: {final_stats['processing_time']:.2f}s")
        logger.info("="*60)

        return current_text, self.layers, final_stats


def test_v25_with_dark_knight():
    """Testa V25 Hybrid Ultimate com The Dark Knight"""
    from pathlib import Path

    # Carregar texto
    txt_path = Path('data/original/The_Dark_Knight_-_Release.txt')
    if not txt_path.exists():
        print("❌ Arquivo não encontrado")
        return

    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Testar com amostra
    sample_size = 50000  # 50k chars
    sample = text[:sample_size]

    print(f"\n{'='*60}")
    print("🎬 TESTE COM THE DARK KNIGHT")
    print(f"{'='*60}")
    print(f"📄 Texto completo: {len(text):,} chars")
    print(f"📄 Amostra para teste: {len(sample):,} chars")

    # Comprimir
    compressor = DigiLangV25HybridUltimate(max_layers=4)
    compressed, layers, stats = compressor.compress(sample)

    # Comparar com outras versões
    print(f"\n🔥 COMPARAÇÃO FINAL:")
    print(f"  V8.1 Supreme: 0.72% compressão")
    print(f"  V19 Personalized: 7.61% compressão")
    print(f"  V22 MEGA: 15.29% compressão")
    print(f"  V24 Ultimate PT: 4.7% compressão")
    print(f"  V25 HYBRID ULTIMATE: {stats['total_compression']:.1%} compressão")

    if stats['total_compression'] > 0.25:
        print(f"  🏆 NOVO RECORDE ABSOLUTO! Superou 25%!")
    elif stats['total_compression'] > 0.20:
        print(f"  🏆 NOVO RECORDE! Superou 20%!")
    elif stats['total_compression'] > 0.1529:
        print(f"  ✅ MELHOR que V22 MEGA!")
    else:
        diff = (0.1529 - stats['total_compression']) * 100
        print(f"  ⚠️ Ainda {diff:.1f}% abaixo do V22 MEGA")

    return stats


if __name__ == "__main__":
    test_v25_with_dark_knight()