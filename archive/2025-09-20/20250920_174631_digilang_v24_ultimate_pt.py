#!/usr/bin/env python3
"""
🚀 DigiLang V24 Ultimate PT - Sistema Híbrido Definitivo
Combina o melhor de todos os mundos:
- Mining personalizado do V19/V22
- Multi-layer do TPD
- Todos os símbolos Unicode disponíveis
- Otimização em português
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

class DigiLangV24UltimatePT:
    """
    DigiLang V24 - Versão definitiva em português
    Combina todas as técnicas aprendidas
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
        self.all_symbols = self._discover_all_symbols()

    def _discover_all_symbols(self) -> List[str]:
        """Descobre TODOS os símbolos Unicode de 1 token"""
        symbols = []

        # Ranges expandidos baseados no V22 MEGA
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

            # Emoji and pictograph ranges
            (0x1F300, 0x1F5FF), # Miscellaneous Symbols and Pictographs
            (0x1F600, 0x1F64F), # Emoticons
            (0x1F680, 0x1F6FF), # Transport and Map
            (0x1F700, 0x1F77F), # Alchemical Symbols
            (0x1F780, 0x1F7FF), # Geometric Shapes Extended
            (0x1F800, 0x1F8FF), # Supplemental Arrows-C

            # CJK ranges (many are 1 token)
            (0x4E00, 0x9FFF),   # CJK Unified Ideographs (main)
            (0x3400, 0x4DBF),   # CJK Extension A
            (0x3040, 0x309F),   # Hiragana
            (0x30A0, 0x30FF),   # Katakana
            (0x31F0, 0x31FF),   # Katakana Extensions
            (0x3200, 0x32FF),   # Enclosed CJK

            # Other scripts
            (0x0590, 0x05FF),   # Hebrew
            (0x0600, 0x06FF),   # Arabic
            (0x0700, 0x074F),   # Syriac
            (0x0750, 0x077F),   # Arabic Supplement
            (0x0780, 0x07BF),   # Thaana
            (0x0900, 0x097F),   # Devanagari
            (0x0980, 0x09FF),   # Bengali
            (0x0A00, 0x0A7F),   # Gurmukhi
            (0x0A80, 0x0AFF),   # Gujarati
            (0x0B00, 0x0B7F),   # Oriya
            (0x0B80, 0x0BFF),   # Tamil
            (0x0C00, 0x0C7F),   # Telugu
            (0x0C80, 0x0CFF),   # Kannada
            (0x0D00, 0x0D7F),   # Malayalam
            (0x0D80, 0x0DFF),   # Sinhala
            (0x0E00, 0x0E7F),   # Thai
            (0x0E80, 0x0EFF),   # Lao
            (0x0F00, 0x0FFF),   # Tibetan
        ]

        for start, end in ranges:
            # Testar todos os símbolos no range
            for codepoint in range(start, min(end + 1, 0x110000)):
                try:
                    char = chr(codepoint)
                    # Verificar se é realmente 1 token
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
                    # Codepoint inválido
                    continue

        logger.info(f"💎 Descobertos {len(symbols)} símbolos de 1 token")
        return symbols

    def _mine_patterns(self, text: str, min_freq: int = 3) -> Dict[str, int]:
        """
        Minera padrões do texto (palavras e frases)
        Similar ao V19/V22 mas melhorado
        """
        patterns = Counter()

        # 1. Palavras individuais (2+ tokens)
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            if self.tiktoken_available:
                tokens = self.encoder.encode(word)
                if len(tokens) >= 2:  # Só vale a pena se gastar 2+ tokens
                    patterns[word] += 1
            else:
                if len(word) >= 8:  # Aproximação: palavras grandes
                    patterns[word] += 1

        # 2. Bigramas e trigramas de palavras comuns
        words_clean = [w for w in words if len(w) > 2]
        for i in range(len(words_clean) - 1):
            bigram = f"{words_clean[i]} {words_clean[i+1]}"
            if len(bigram) <= 30:  # Limitar tamanho
                patterns[bigram] += 1

            if i < len(words_clean) - 2:
                trigram = f"{words_clean[i]} {words_clean[i+1]} {words_clean[i+2]}"
                if len(trigram) <= 40:
                    patterns[trigram] += 1

        # 3. Padrões específicos de roteiro
        screenplay_patterns = [
            r'INT\.\s+[\w\s\-]+',  # Locações internas
            r'EXT\.\s+[\w\s\-]+',  # Locações externas
            r'FADE\s+(IN|OUT)',
            r'CUT\s+TO:',
            r'\([A-Z\s]+\)',  # Direções de cena
            r'[A-Z][A-Z\s]+\n',  # Nomes de personagens
        ]

        for pattern in screenplay_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) > 3:
                    patterns[match.strip()] += 1

        # 4. Minerar nomes de personagens (aparecem em CAPS)
        character_names = re.findall(r'\n([A-Z][A-Z\s]{2,20})\n', text)
        for name in character_names:
            name = name.strip()
            if name and not name.startswith(('INT', 'EXT', 'FADE', 'CUT')):
                patterns[name] += 5  # Boost para nomes de personagens

        # Filtrar por frequência mínima
        filtered = {p: f for p, f in patterns.items() if f >= min_freq}

        logger.info(f"⛏️ Minerados {len(filtered)} padrões únicos (de {len(patterns)} totais)")
        return filtered

    def _calculate_savings(self, pattern: str, frequency: int) -> int:
        """Calcula economia em tokens para um padrão"""
        if self.tiktoken_available:
            original_tokens = len(self.encoder.encode(pattern))
            replacement_tokens = 1  # Será substituído por 1 símbolo
            savings = (original_tokens - replacement_tokens) * frequency
        else:
            # Estimativa: 1 token = 4 chars
            original_tokens = len(pattern) // 4
            savings = max(0, (original_tokens - 1) * frequency)

        return savings

    def _select_best_patterns(self,
                              patterns: Dict[str, int],
                              max_patterns: int = 1000) -> Dict[str, str]:
        """
        Seleciona os melhores padrões e atribui símbolos
        """
        # Calcular economia para cada padrão
        pattern_savings = []
        for pattern, freq in patterns.items():
            savings = self._calculate_savings(pattern, freq)
            if savings > 0:
                pattern_savings.append((pattern, freq, savings))

        # Ordenar por economia total
        pattern_savings.sort(key=lambda x: x[2], reverse=True)

        # Selecionar top padrões
        selected = {}
        available_symbols = [s for s in self.all_symbols if s not in self.symbols_used]

        for pattern, freq, savings in pattern_savings[:max_patterns]:
            if not available_symbols:
                break

            symbol = available_symbols.pop(0)
            selected[pattern] = symbol
            self.symbols_used.add(symbol)

        logger.info(f"✅ Selecionados {len(selected)} padrões ótimos")
        return selected

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

        # Minerar padrões - frequência mais baixa = mais padrões
        min_freq = max(1, 3 - layer_num)  # Frequência muito baixa para capturar mais
        patterns = self._mine_patterns(text, min_freq)

        # Selecionar melhores padrões - mais padrões = melhor compressão
        max_patterns = 2000 - layer_num * 100  # Mais padrões por camada
        dictionary = self._select_best_patterns(patterns, max_patterns)

        # Aplicar substituições
        compressed = text
        replacements = 0
        total_savings = 0

        # Ordenar por tamanho (maiores primeiro) para evitar sobreposição
        sorted_patterns = sorted(dictionary.items(),
                               key=lambda x: len(x[0]),
                               reverse=True)

        for pattern, symbol in sorted_patterns:
            if pattern in compressed:
                count = compressed.count(pattern)
                compressed = compressed.replace(pattern, symbol)
                replacements += count

                # Calcular economia real
                if self.tiktoken_available:
                    savings = self._calculate_savings(pattern, count)
                    total_savings += savings

        # Calcular compressão
        if self.tiktoken_available:
            compressed_tokens = len(self.encoder.encode(compressed))
        else:
            compressed_tokens = len(compressed) // 4

        compression_ratio = 1 - (compressed_tokens / original_tokens)

        stats = {
            'layer': layer_num + 1,
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'compression_ratio': compression_ratio,
            'patterns_used': len(dictionary),
            'replacements': replacements,
            'total_savings': total_savings
        }

        logger.info(f"✅ Camada {layer_num + 1}: {compression_ratio:.1%} compressão")
        logger.info(f"   Substituições: {replacements:,}")
        logger.info(f"   Economia: {total_savings:,} tokens")

        return dictionary, compressed, stats

    def compress(self, text: str) -> Tuple[str, List[Dict], Dict]:
        """
        Comprime texto usando múltiplas camadas
        """
        logger.info("="*60)
        logger.info("🚀 DigiLang V24 Ultimate PT - Iniciando compressão")
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
            if stats['compression_ratio'] < 0.01:  # Menos de 1% de ganho
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
        logger.info("🎯 RESULTADOS FINAIS V24 ULTIMATE PT")
        logger.info("="*60)
        logger.info(f"📊 Compressão Total: {total_compression:.1%}")
        logger.info(f"💾 Tokens: {initial_tokens:,} → {final_tokens:,}")
        logger.info(f"💰 Economia: {initial_tokens - final_tokens:,} tokens")
        logger.info(f"🔢 Padrões totais: {final_stats['total_patterns']:,}")
        logger.info(f"📚 Camadas usadas: {final_stats['total_layers']}")
        logger.info(f"⏱️ Tempo: {final_stats['processing_time']:.2f}s")
        logger.info("="*60)

        return current_text, self.layers, final_stats


def test_v24_with_dark_knight():
    """Testa V24 com The Dark Knight"""
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
    compressor = DigiLangV24UltimatePT(max_layers=3)
    compressed, layers, stats = compressor.compress(sample)

    # Comparar com outras versões
    print(f"\n🔥 COMPARAÇÃO FINAL:")
    print(f"  V8.1 Supreme: 0.72% compressão")
    print(f"  V19 Personalized: 7.61% compressão")
    print(f"  V22 MEGA: 15.29% compressão")
    print(f"  V24 ULTIMATE PT: {stats['total_compression']:.1%} compressão")

    if stats['total_compression'] > 0.20:
        print(f"  🏆 NOVO RECORDE! Superou 20%!")
    elif stats['total_compression'] > 0.1529:
        print(f"  ✅ MELHOR que V22 MEGA!")
    else:
        diff = (0.1529 - stats['total_compression']) * 100
        print(f"  ⚠️ Ainda {diff:.1f}% abaixo do V22 MEGA")

    return stats


if __name__ == "__main__":
    test_v24_with_dark_knight()