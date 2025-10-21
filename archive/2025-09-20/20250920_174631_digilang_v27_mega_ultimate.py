#!/usr/bin/env python3
"""
🚀 DigiLang V27 MEGA Ultimate - Implementação das Regras Definitivas do Usuário
Implementa EXATAMENTE as 5 regras fundamentais para otimização máxima:

1. Calcular todas as palavras do roteiro e listar de maior a menor o uso de token
2. Usar tudo que usa 1 token para traduzir essas palavras de trás pra frente
3. Ao acabar tudo que gasta apenas um token disponível, começar a usar tudo que usa 2 token disponível
4. Quando acabar de 2 token, usar tudo que gasta 3 token disponível
5. Nunca traduzir uma palavra por algo que gasta mais tokens que a palavra original

TUDO = caracteres exóticos, emojis, TUDO que estiver disponível
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
class WordTokenInfo:
    """Informação completa sobre tokens de uma palavra"""
    word: str
    frequency: int
    token_cost: int
    total_tokens_used: int  # frequency * token_cost

@dataclass
class ReplacementSymbol:
    """Símbolo disponível para substituição"""
    symbol: str
    token_cost: int

class DigiLangV27MegaUltimate:
    """
    DigiLang V27 - Implementação das regras definitivas do usuário
    Sistema que garante eficiência máxima seguindo as 5 regras fundamentais
    """

    def __init__(self):
        self.word_stats = []
        self.available_symbols = []
        self.used_symbols = set()
        self.replacement_map = {}

        # Importar tiktoken OBRIGATÓRIO para cálculos precisos
        try:
            import tiktoken
            self.encoder = tiktoken.get_encoding("cl100k_base")
            self.tiktoken_available = True
        except ImportError:
            raise ImportError("❌ tiktoken é OBRIGATÓRIO para V27 MEGA Ultimate")

        # Descobrir TODOS os símbolos disponíveis
        self._discover_all_available_symbols()

        logger.info(f"💎 V27 MEGA Ultimate inicializado com {len(self.available_symbols)} símbolos")

    def _discover_all_available_symbols(self):
        """
        Descobre TODOS os símbolos Unicode disponíveis classificados por custo de token
        TUDO = caracteres exóticos, emojis, TUDO que estiver disponível
        """
        symbols_by_cost = {1: [], 2: [], 3: []}

        # Ranges COMPLETOS baseados na pesquisa sistemática
        comprehensive_ranges = [
            # Basic Unicode ranges com alta taxa de 1-token
            (0x0080, 0x024F),   # Latin Extended (114/464 = 25%)
            (0x0250, 0x02AF),   # IPA Extensions
            (0x0300, 0x036F),   # Combining Diacritical Marks
            (0x0370, 0x03FF),   # Greek and Coptic (27/144 = 19%)
            (0x0400, 0x04FF),   # Cyrillic (58/256 = 23%)
            (0x0590, 0x05FF),   # Hebrew (14/112 = 12%)
            (0x0600, 0x06FF),   # Arabic (42/256 = 16%)
            (0x0900, 0x097F),   # Devanagari (17/128 = 13%)
            (0x0980, 0x09FF),   # Bengali (6/128 = 5%)
            (0x0E00, 0x0E7F),   # Thai (41/128 = 32%)

            # Symbol ranges com boa taxa de 1-token
            (0x2000, 0x206F),   # General Punctuation (22/112 = 20%)
            (0x2070, 0x209F),   # Superscripts and Subscripts
            (0x20A0, 0x20CF),   # Currency Symbols
            (0x2100, 0x214F),   # Letterlike Symbols
            (0x2150, 0x218F),   # Number Forms
            (0x2190, 0x21FF),   # Arrows
            (0x2200, 0x22FF),   # Mathematical Operators
            (0x2300, 0x23FF),   # Miscellaneous Technical
            (0x2400, 0x243F),   # Control Pictures
            (0x2440, 0x245F),   # Optical Character Recognition
            (0x2460, 0x24FF),   # Enclosed Alphanumerics
            (0x2500, 0x257F),   # Box Drawing (7/128 = 5%)
            (0x2580, 0x259F),   # Block Elements (2/32 = 6%)
            (0x25A0, 0x25FF),   # Geometric Shapes (3/96 = 3%)
            (0x2600, 0x26FF),   # Miscellaneous Symbols (6/256 = 2%)
            (0x2700, 0x27BF),   # Dingbats (1/192 = 0.5%)
            (0x27C0, 0x27EF),   # Miscellaneous Mathematical Symbols-A
            (0x27F0, 0x27FF),   # Supplemental Arrows-A
            (0x2800, 0x28FF),   # Braille Patterns (1/256 = 0.4%)

            # CJK ranges com EXCELENTE taxa de 1-token
            (0x3000, 0x303F),   # CJK Symbols and Punctuation (12/64 = 19%)
            (0x3040, 0x309F),   # Hiragana (47/96 = 49%)
            (0x30A0, 0x30FF),   # Katakana (51/96 = 53%)
            (0x4E00, 0x4F00),   # CJK Unified Ideographs (sample) (45/257 = 18%)
        ]

        # Ranges extras para EXPANDIR busca se necessário
        extra_cjk_ranges = [
            (0x4F00, 0x5000),   # CJK Unified Ideographs (expansion 1)
            (0x5000, 0x5100),   # CJK Unified Ideographs (expansion 2)
            (0x5100, 0x5200),   # CJK Unified Ideographs (expansion 3)
            (0x5200, 0x5300),   # CJK Unified Ideographs (expansion 4)
            (0x5300, 0x5400),   # CJK Unified Ideographs (expansion 5)
        ]

        logger.info("🔍 Descobrindo símbolos usando pesquisa sistemática completa...")

        # Processar TODOS os ranges identificados como eficientes
        total_tested = 0
        for start, end in comprehensive_ranges:
            for codepoint in range(start, min(end + 1, 0x110000)):
                try:
                    char = chr(codepoint)
                    total_tested += 1

                    # Excluir espaços e controles básicos
                    if char in [' ', '\n', '\t', '\r', '\x00']:
                        continue

                    # Calcular custo em tokens COM PRECISÃO
                    try:
                        tokens = self.encoder.encode(char)
                        token_cost = len(tokens)

                        # Só incluir símbolos até 3 tokens
                        if 1 <= token_cost <= 3:
                            symbol = ReplacementSymbol(char, token_cost)
                            symbols_by_cost[token_cost].append(symbol)

                    except Exception:
                        continue

                except ValueError:
                    continue

        # Se ainda precisarmos de mais símbolos de 1-token, expandir para CJK
        if len(symbols_by_cost[1]) < 1000:
            logger.info(f"🔍 Descobertos {len(symbols_by_cost[1])} símbolos 1-token. Expandindo busca CJK...")
            for start, end in extra_cjk_ranges:
                if len(symbols_by_cost[1]) >= 1000:  # Parar quando tivermos o suficiente
                    break

                for codepoint in range(start, min(end + 1, 0x110000)):
                    try:
                        char = chr(codepoint)
                        total_tested += 1

                        if char in [' ', '\n', '\t', '\r', '\x00']:
                            continue

                        try:
                            tokens = self.encoder.encode(char)
                            if len(tokens) == 1:  # Só 1-token nesta fase
                                symbol = ReplacementSymbol(char, 1)
                                symbols_by_cost[1].append(symbol)

                        except Exception:
                            continue

                    except ValueError:
                        continue

        # Organizar por custo de token (1-token primeiro, depois 2-token, depois 3-token)
        self.available_symbols = []
        for cost in [1, 2, 3]:
            self.available_symbols.extend(symbols_by_cost[cost])
            logger.info(f"📊 Símbolos de {cost} token: {len(symbols_by_cost[cost]):,}")

        logger.info(f"💎 Total de símbolos descobertos: {len(self.available_symbols):,}")
        logger.info(f"🧪 Caracteres testados: {total_tested:,}")

        # Validar alguns símbolos de 1-token para debug
        if symbols_by_cost[1]:
            logger.info(f"🔍 Exemplos de símbolos 1-token: {symbols_by_cost[1][:10]}")
            for symbol in symbols_by_cost[1][:5]:
                test_tokens = self.encoder.encode(symbol.symbol)
                logger.info(f"   '{symbol.symbol}': {len(test_tokens)} tokens (validado)")

    def _analyze_words_by_token_usage(self, text: str) -> List[WordTokenInfo]:
        """
        REGRA 1: Calcular todas as palavras do roteiro e listar de maior a menor o uso de token
        """
        logger.info("📊 REGRA 1: Analisando palavras por uso de token...")

        # Extrair todas as palavras (incluindo padrões específicos de roteiro)
        words = re.findall(r'\b[A-Za-zÀ-ÿ]+\b', text)

        # Adicionar padrões específicos de roteiro
        script_patterns = [
            r'FADE IN:', r'FADE OUT\.', r'CUT TO:', r'CLOSE UP', r'WIDE SHOT',
            r'INT\. [A-Z\s\-]+', r'EXT\. [A-Z\s\-]+',
            r'\([A-Za-z\s,]+\)',  # Direções entre parênteses
        ]

        for pattern in script_patterns:
            matches = re.findall(pattern, text)
            words.extend(matches)

        # Contar frequência
        word_freq = Counter(words)

        word_stats = []
        for word, frequency in word_freq.items():
            if len(word) > 1:  # Só palavras com mais de 1 char
                tokens = self.encoder.encode(word)
                token_cost = len(tokens)
                total_tokens_used = frequency * token_cost

                word_info = WordTokenInfo(
                    word=word,
                    frequency=frequency,
                    token_cost=token_cost,
                    total_tokens_used=total_tokens_used
                )
                word_stats.append(word_info)

        # Ordenar por uso total de tokens (de maior para menor)
        word_stats.sort(key=lambda x: x.total_tokens_used, reverse=True)

        logger.info(f"✅ Analisadas {len(word_stats):,} palavras únicas")
        logger.info(f"🔥 Top 5 por uso de tokens:")
        for i, info in enumerate(word_stats[:5]):
            logger.info(f"   {i+1}. '{info.word}': {info.total_tokens_used} tokens totais "
                       f"({info.frequency}x × {info.token_cost} tokens)")

        return word_stats

    def _apply_replacement_rules(self, word_stats: List[WordTokenInfo]) -> Dict[str, str]:
        """
        REGRAS 2-5: Aplicar as regras de substituição seguindo a lógica exata do usuário
        """
        logger.info("🔄 REGRAS 2-5: Aplicando substituições por custo de token...")

        replacement_map = {}
        symbols_used = 0
        tokens_saved = 0

        # Organizar símbolos por custo
        symbols_1_token = [s for s in self.available_symbols if s.token_cost == 1]
        symbols_2_token = [s for s in self.available_symbols if s.token_cost == 2]
        symbols_3_token = [s for s in self.available_symbols if s.token_cost == 3]

        logger.info(f"📦 Símbolos disponíveis: {len(symbols_1_token)} de 1-token, "
                   f"{len(symbols_2_token)} de 2-token, {len(symbols_3_token)} de 3-token")

        # Criar filas de símbolos por custo
        available_1 = symbols_1_token.copy()
        available_2 = symbols_2_token.copy()
        available_3 = symbols_3_token.copy()

        # Processar palavras de trás pra frente (maior uso de token primeiro)
        for word_info in word_stats:
            word = word_info.word
            word_token_cost = word_info.token_cost

            # REGRA 5: Nunca traduzir por algo que gasta mais tokens
            # REGRAS 2-4: Usar 1-token primeiro, depois 2-token, depois 3-token
            best_symbol = None
            best_cost = float('inf')

            # Tentar símbolos em ordem de custo APENAS se economizam tokens
            if word_token_cost >= 2 and available_1:  # Só vale a pena se palavra tem 2+ tokens
                best_symbol = available_1.pop(0)
                best_cost = 1
            elif word_token_cost >= 3 and available_2:  # Só vale a pena se palavra tem 3+ tokens
                best_symbol = available_2.pop(0)
                best_cost = 2
            elif word_token_cost >= 4 and available_3:  # Só vale a pena se palavra tem 4+ tokens
                best_symbol = available_3.pop(0)
                best_cost = 3

            # Verificar se a substituição realmente economiza tokens
            if best_symbol and best_cost < word_token_cost:
                replacement_map[word] = best_symbol.symbol
                self.used_symbols.add(best_symbol.symbol)
                symbols_used += 1

                # Calcular economia real
                savings = (word_token_cost - best_cost) * word_info.frequency
                tokens_saved += savings

                logger.debug(f"✅ '{word}' ({word_token_cost}t) → '{best_symbol.symbol}' ({best_cost}t) "
                           f"= {savings} tokens economizados")
            else:
                # Sem economia ou sem símbolos disponíveis
                if word_token_cost >= 2:  # Só registrar palavras que poderiam ser otimizadas
                    logger.debug(f"⚠️ '{word}' ({word_token_cost}t) - sem substituição econômica")

        logger.info(f"✅ Substituições criadas: {len(replacement_map):,}")
        logger.info(f"🔢 Símbolos utilizados: {symbols_used:,}")
        logger.info(f"💰 Tokens economizados estimados: {tokens_saved:,}")

        return replacement_map

    def _apply_replacements(self, text: str, replacement_map: Dict[str, str]) -> Tuple[str, int, int]:
        """
        Aplica as substituições no texto ordenadas por tamanho
        """
        compressed = text
        total_replacements = 0
        total_savings = 0

        # Ordenar por tamanho (maiores primeiro) para evitar sobreposição
        sorted_replacements = sorted(replacement_map.items(),
                                   key=lambda x: len(x[0]),
                                   reverse=True)

        for word, symbol in sorted_replacements:
            if word in compressed:
                count = compressed.count(word)
                compressed = compressed.replace(word, symbol)
                total_replacements += count

                # Calcular economia
                original_tokens = len(self.encoder.encode(word))
                symbol_tokens = len(self.encoder.encode(symbol))
                savings = (original_tokens - symbol_tokens) * count
                total_savings += savings

        return compressed, total_replacements, total_savings

    def compress(self, text: str) -> Tuple[str, Dict[str, str], Dict]:
        """
        Comprime texto seguindo EXATAMENTE as 5 regras do usuário
        """
        logger.info("="*60)
        logger.info("🚀 DigiLang V27 MEGA Ultimate - Regras Definitivas")
        logger.info("="*60)

        start_time = time.time()

        # Contar tokens originais
        original_tokens = len(self.encoder.encode(text))
        logger.info(f"📄 Texto original: {len(text):,} chars, {original_tokens:,} tokens")

        # REGRA 1: Analisar palavras por uso de token
        self.word_stats = self._analyze_words_by_token_usage(text)

        # REGRAS 2-5: Aplicar substituições seguindo as regras
        replacement_map = self._apply_replacement_rules(self.word_stats)

        # Aplicar substituições
        compressed, replacements, token_savings = self._apply_replacements(text, replacement_map)

        # Calcular estatísticas finais
        final_tokens = len(self.encoder.encode(compressed))
        compression_ratio = 1 - (final_tokens / original_tokens)

        stats = {
            'original_chars': len(text),
            'compressed_chars': len(compressed),
            'original_tokens': original_tokens,
            'final_tokens': final_tokens,
            'compression_ratio': compression_ratio,
            'tokens_saved': original_tokens - final_tokens,
            'replacements_made': replacements,
            'patterns_used': len(replacement_map),
            'symbols_discovered': len(self.available_symbols),
            'processing_time': time.time() - start_time
        }

        logger.info("\n" + "="*60)
        logger.info("🎯 RESULTADOS V27 MEGA Ultimate")
        logger.info("="*60)
        logger.info(f"📊 Compressão Total: {compression_ratio:.1%}")
        logger.info(f"💾 Tokens: {original_tokens:,} → {final_tokens:,}")
        logger.info(f"💰 Economia: {stats['tokens_saved']:,} tokens")
        logger.info(f"🔢 Substituições: {replacements:,}")
        logger.info(f"📚 Padrões usados: {len(replacement_map):,}")
        logger.info(f"💎 Símbolos descobertos: {len(self.available_symbols):,}")
        logger.info(f"⏱️ Tempo: {stats['processing_time']:.2f}s")
        logger.info("="*60)

        return compressed, replacement_map, stats


def test_v27_mega_ultimate():
    """Testa V27 MEGA Ultimate com The Dark Knight"""
    from pathlib import Path

    # Carregar texto
    txt_path = Path('data/original/The_Dark_Knight_-_Release.txt')
    if not txt_path.exists():
        print("❌ Arquivo não encontrado")
        return

    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Testar com amostra
    sample_size = 50000  # 50k chars como nos testes anteriores
    sample = text[:sample_size]

    print(f"\n{'='*60}")
    print("🎬 TESTE V27 MEGA ULTIMATE - REGRAS DEFINITIVAS")
    print(f"{'='*60}")
    print(f"📄 Texto completo: {len(text):,} chars")
    print(f"📄 Amostra para teste: {len(sample):,} chars")

    # Comprimir
    compressor = DigiLangV27MegaUltimate()
    compressed, replacement_map, stats = compressor.compress(sample)

    # Comparar com versões anteriores
    print(f"\n🔥 COMPARAÇÃO HISTÓRICA:")
    print(f"  V8.1 Supreme: 0.72% compressão")
    print(f"  V19 Personalized: 7.61% compressão")
    print(f"  V22 MEGA: 15.29% compressão")
    print(f"  V24 Ultimate PT: 4.7% compressão")
    print(f"  V25 Hybrid Ultimate: 7.6% compressão")
    print(f"  V26 MEGA Multi-Layer: 10.8% compressão")
    print(f"  V27 MEGA ULTIMATE: {stats['compression_ratio']:.1%} compressão")

    if stats['compression_ratio'] > 0.30:
        print(f"  🏆 RECORDE HISTÓRICO ABSOLUTO! Superou 30%!")
    elif stats['compression_ratio'] > 0.25:
        print(f"  🏆 NOVO RECORDE ABSOLUTO! Superou 25%!")
    elif stats['compression_ratio'] > 0.20:
        print(f"  🏆 NOVO RECORDE! Superou 20%!")
    elif stats['compression_ratio'] > 0.1529:
        print(f"  ✅ MELHOR que V22 MEGA original!")
    else:
        diff = (0.1529 - stats['compression_ratio']) * 100
        print(f"  ⚠️ Ainda {diff:.1f}% abaixo do V22 MEGA")

    # Verificar eficiência das regras
    print(f"\n📋 VERIFICAÇÃO DAS REGRAS:")
    print(f"  ✅ REGRA 1: {len(compressor.word_stats):,} palavras analisadas")
    print(f"  ✅ REGRA 2-4: {len([s for s in compressor.available_symbols if s.token_cost == 1]):,} símbolos 1-token")
    print(f"  ✅ REGRA 2-4: {len([s for s in compressor.available_symbols if s.token_cost == 2]):,} símbolos 2-token")
    print(f"  ✅ REGRA 2-4: {len([s for s in compressor.available_symbols if s.token_cost == 3]):,} símbolos 3-token")
    print(f"  ✅ REGRA 5: Zero substituições com custo maior que original")

    return stats


if __name__ == "__main__":
    test_v27_mega_ultimate()