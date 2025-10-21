#!/usr/bin/env python3
"""
FASE 22 - DigiLang V22 MEGA - Compressão Máxima Absoluta
Sistema ScriptureMon Champion

REGRAS FUNDAMENTAIS:
1. Minerar TODAS as palavras e ordenar por consumo de tokens (maior → menor)
2. Usar TODOS os símbolos de 1 token disponíveis (incluindo exóticos, CJK, emojis)
3. Depois usar TODOS os símbolos de 2 tokens
4. Depois usar TODOS os símbolos de 3 tokens
5. PARAR quando símbolo_tokens >= palavra_tokens (sem economia)

Assinado: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion
Data: 14/09/2025
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
from dataclasses import dataclass
import PyPDF2
import tiktoken
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MegaPattern:
    """Padrão para compressão MEGA"""
    text: str
    frequency: int
    original_tokens: int
    potential_savings_1token: int  # Economia se usar símbolo de 1 token
    potential_savings_2token: int  # Economia se usar símbolo de 2 tokens
    potential_savings_3token: int  # Economia se usar símbolo de 3 tokens

class DigiLangV22Mega:
    """DigiLang V22 MEGA - Compressão Máxima Absoluta com TODOS os símbolos"""

    def __init__(self):
        """Inicializar sistema V22 MEGA"""
        self.encoder = tiktoken.get_encoding("cl100k_base")

        logger.info("🚀 DigiLang V22 MEGA inicializando...")
        logger.info("🔍 Descobrindo TODOS os símbolos disponíveis...")

        # Descobrir TODOS os símbolos
        self.symbols_1token = self._discover_all_1token_symbols()
        self.symbols_2token = self._discover_all_2token_symbols()
        self.symbols_3token = self._discover_all_3token_symbols()

        logger.info(f"💎 SÍMBOLOS DESCOBERTOS:")
        logger.info(f"   1 token: {len(self.symbols_1token):,} símbolos")
        logger.info(f"   2 tokens: {len(self.symbols_2token):,} símbolos")
        logger.info(f"   3 tokens: {len(self.symbols_3token):,} símbolos")
        logger.info(f"   TOTAL: {len(self.symbols_1token) + len(self.symbols_2token) + len(self.symbols_3token):,} símbolos disponíveis!")

    def _discover_all_1token_symbols(self) -> List[str]:
        """Descobrir TODOS os caracteres de 1 token no Unicode"""
        symbols = []

        # Testar TODOS os ranges Unicode relevantes
        ranges = [
            # ASCII e Latin
            (0x0020, 0x007E),   # ASCII printable
            (0x00A0, 0x00FF),   # Latin-1 Supplement
            (0x0100, 0x017F),   # Latin Extended-A
            (0x0180, 0x024F),   # Latin Extended-B
            (0x0250, 0x02AF),   # IPA Extensions
            (0x02B0, 0x02FF),   # Spacing Modifiers

            # Alfabetos diversos
            (0x0370, 0x03FF),   # Greek and Coptic
            (0x0400, 0x04FF),   # Cyrillic
            (0x0530, 0x058F),   # Armenian
            (0x0590, 0x05FF),   # Hebrew
            (0x0600, 0x06FF),   # Arabic
            (0x0700, 0x077F),   # Syriac and Arabic Supplement

            # Asiáticos
            (0x0E00, 0x0E7F),   # Thai
            (0x0E80, 0x0EFF),   # Lao
            (0x1000, 0x109F),   # Myanmar
            (0x1100, 0x11FF),   # Hangul Jamo
            (0x3040, 0x309F),   # Hiragana
            (0x30A0, 0x30FF),   # Katakana
            (0x3100, 0x312F),   # Bopomofo
            (0x3130, 0x318F),   # Hangul Compatibility
            (0x31F0, 0x31FF),   # Katakana Phonetic
            (0x3200, 0x32FF),   # Enclosed CJK
            (0x3300, 0x33FF),   # CJK Compatibility
            (0x4E00, 0x9FFF),   # CJK Unified Ideographs
            (0xAC00, 0xD7AF),   # Hangul Syllables

            # Símbolos e pontuação
            (0x2000, 0x206F),   # General Punctuation
            (0x2070, 0x209F),   # Superscripts
            (0x20A0, 0x20CF),   # Currency
            (0x2100, 0x214F),   # Letterlike
            (0x2150, 0x218F),   # Number Forms
            (0x2190, 0x21FF),   # Arrows
            (0x2200, 0x22FF),   # Mathematical
            (0x2300, 0x23FF),   # Technical
            (0x2400, 0x243F),   # Control Pictures
            (0x2460, 0x24FF),   # Enclosed Alphanumerics
            (0x2500, 0x257F),   # Box Drawing
            (0x2580, 0x259F),   # Block Elements
            (0x25A0, 0x25FF),   # Geometric Shapes
            (0x2600, 0x26FF),   # Miscellaneous Symbols
            (0x2700, 0x27BF),   # Dingbats
            (0x2800, 0x28FF),   # Braille
            (0x2900, 0x297F),   # Supplemental Arrows
            (0x2B00, 0x2BFF),   # Miscellaneous Symbols and Arrows

            # Emojis e símbolos modernos
            (0x1F300, 0x1F5FF), # Miscellaneous Symbols and Pictographs
            (0x1F600, 0x1F64F), # Emoticons
            (0x1F680, 0x1F6FF), # Transport and Map
            (0x1F900, 0x1F9FF), # Supplemental Symbols
        ]

        for start, end in ranges:
            for codepoint in range(start, min(end + 1, 0x110000)):
                try:
                    char = chr(codepoint)
                    # Verificar se é 1 token
                    if len(self.encoder.encode(char)) == 1:
                        # Excluir apenas espaço e controles básicos
                        if char not in [' ', '\n', '\t', '\r', '\x00']:
                            symbols.append(char)
                except:
                    pass

        return symbols

    def _discover_all_2token_symbols(self) -> List[str]:
        """Descobrir símbolos de 2 tokens"""
        symbols = []

        # Combinações comuns
        combos = ['##', '@@', '$$', '%%', '&&', '**', '++', '--', '//', '::',
                  '<<', '>>', '==', '!=', '<=', '>=', '||', '&&', '~~', '``']

        for combo in combos:
            if len(self.encoder.encode(combo)) == 2:
                symbols.append(combo)

        # Emojis que são 2 tokens
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
                    if len(self.encoder.encode(char)) == 2:
                        symbols.append(char)
                except:
                    pass

        return symbols[:1000]  # Limitar para não ficar muito pesado

    def _discover_all_3token_symbols(self) -> List[str]:
        """Descobrir símbolos de 3 tokens"""
        symbols = []

        # Combinações de 3 caracteres
        combos = ['###', '@@@', '$$$', '%%%', '&&&', '***', '+++', '---', '///', ':::',
                  '<<<', '>>>', '===', '!==', '<==', '>==', '|||', '&&&', '~~~', '```']

        for combo in combos:
            if len(self.encoder.encode(combo)) == 3:
                symbols.append(combo)

        # Emojis compostos
        composite_emojis = ['👨‍👩‍👧', '👨‍👩‍👦', '👨‍👨‍👦', '👩‍👩‍👧', '🏳️‍🌈', '🏴‍☠️']

        for emoji in composite_emojis:
            token_count = len(self.encoder.encode(emoji))
            if token_count == 3:
                symbols.append(emoji)

        return symbols[:100]  # Limitar

    def mine_all_patterns(self, text: str) -> List[MegaPattern]:
        """Minerar TODOS os padrões e calcular economia potencial"""
        patterns = []

        logger.info("⛏️ Minerando TODOS os padrões do texto...")

        # 1. Extrair TODAS as palavras individuais
        words = re.findall(r'\b[\w\']+\b', text)
        word_freq = Counter(words)

        for word, freq in word_freq.items():
            original_tokens = len(self.encoder.encode(word))

            # Calcular economia para cada tipo de símbolo
            savings_1 = (original_tokens - 1) * freq if original_tokens > 1 else 0
            savings_2 = (original_tokens - 2) * freq if original_tokens > 2 else 0
            savings_3 = (original_tokens - 3) * freq if original_tokens > 3 else 0

            if savings_1 > 0:  # Só adicionar se houver economia potencial
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
                if freq > 2:  # Mínimo de repetições
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

        # ORDENAR por economia potencial máxima (1 token)
        patterns.sort(key=lambda x: x.potential_savings_1token, reverse=True)

        logger.info(f"⛏️ Minerados {len(patterns)} padrões únicos")

        return patterns

    def create_mega_dictionary(self, patterns: List[MegaPattern]) -> Dict[str, str]:
        """Criar dicionário MEGA usando TODOS os símbolos disponíveis"""
        dictionary = {}

        logger.info("📚 Criando dicionário MEGA com priorização inteligente...")

        # Índices para cada pool de símbolos
        idx_1token = 0
        idx_2token = 0
        idx_3token = 0

        patterns_used = 0
        total_savings = 0

        for pattern in patterns:
            assigned = False

            # Tentar usar símbolo de 1 token primeiro
            if idx_1token < len(self.symbols_1token) and pattern.potential_savings_1token > 0:
                dictionary[pattern.text] = self.symbols_1token[idx_1token]
                idx_1token += 1
                total_savings += pattern.potential_savings_1token
                assigned = True

            # Se acabaram os de 1 token, usar de 2 tokens
            elif idx_2token < len(self.symbols_2token) and pattern.potential_savings_2token > 0:
                dictionary[pattern.text] = self.symbols_2token[idx_2token]
                idx_2token += 1
                total_savings += pattern.potential_savings_2token
                assigned = True

            # Se acabaram os de 2 tokens, usar de 3 tokens
            elif idx_3token < len(self.symbols_3token) and pattern.potential_savings_3token > 0:
                dictionary[pattern.text] = self.symbols_3token[idx_3token]
                idx_3token += 1
                total_savings += pattern.potential_savings_3token
                assigned = True

            # CONDIÇÃO DE PARADA: Se não há mais economia, parar
            if not assigned:
                break

            patterns_used += 1

        logger.info(f"📊 Dicionário MEGA criado:")
        logger.info(f"   ✅ Padrões usados: {patterns_used}")
        logger.info(f"   💎 Símbolos de 1 token usados: {idx_1token}")
        logger.info(f"   💎 Símbolos de 2 tokens usados: {idx_2token}")
        logger.info(f"   💎 Símbolos de 3 tokens usados: {idx_3token}")
        logger.info(f"   💰 Economia total estimada: {total_savings:,} tokens")

        # Mostrar top padrões
        logger.info("\n🏆 TOP 10 PADRÕES POR ECONOMIA:")
        for i, pattern in enumerate(patterns[:10]):
            if pattern.text in dictionary:
                symbol = dictionary[pattern.text]
                symbol_tokens = len(self.encoder.encode(symbol))
                actual_savings = (pattern.original_tokens - symbol_tokens) * pattern.frequency
                logger.info(
                    f"   {i+1}. '{pattern.text[:30]}' "
                    f"({pattern.frequency}x, {pattern.original_tokens}→{symbol_tokens} tokens) "
                    f"= {actual_savings} tokens salvos"
                )

        return dictionary

    def compress_mega(self, text: str, dictionary: Dict[str, str]) -> Tuple[str, Dict]:
        """Comprimir com dicionário MEGA"""
        compressed = text
        replacements = 0

        # Ordenar por tamanho (maiores primeiro)
        sorted_patterns = sorted(
            dictionary.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        # Aplicar substituições
        for pattern, symbol in sorted_patterns:
            count = compressed.count(pattern)
            if count > 0:
                compressed = compressed.replace(pattern, symbol)
                replacements += count

        # Calcular estatísticas
        original_tokens = len(self.encoder.encode(text))
        compressed_tokens = len(self.encoder.encode(compressed))

        stats = {
            'original_chars': len(text),
            'compressed_chars': len(compressed),
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'replacements': replacements,
            'patterns_used': len([p for p in dictionary if p in text]),
            'char_compression': ((len(text) - len(compressed)) / len(text) * 100) if len(text) > 0 else 0,
            'token_compression': ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0,
            'tokens_saved': original_tokens - compressed_tokens
        }

        return compressed, stats

    def process_pdf_mega(self, pdf_path: str) -> Dict:
        """Processar PDF com compressão V22 MEGA"""
        try:
            start_time = time.time()

            logger.info(f"\n🔥 PROCESSAMENTO V22 MEGA: {Path(pdf_path).name}")
            logger.info("=" * 70)

            # Extrair texto
            text = self._extract_pdf_text(pdf_path)
            if not text:
                return None

            # Estatísticas originais
            original_tokens = len(self.encoder.encode(text))
            logger.info(f"📄 Texto original: {len(text):,} chars, {original_tokens:,} tokens")

            # Minerar TODOS os padrões
            patterns = self.mine_all_patterns(text)

            # Criar dicionário MEGA
            dictionary = self.create_mega_dictionary(patterns)

            # Comprimir
            compressed_text, stats = self.compress_mega(text, dictionary)

            execution_time = time.time() - start_time

            # Resultados
            logger.info("\n" + "=" * 70)
            logger.info("🎯 RESULTADOS V22 MEGA:")
            logger.info(f"   📊 Tokens: {stats['original_tokens']:,} → {stats['compressed_tokens']:,}")
            logger.info(f"   💾 Compressão: {stats['token_compression']:.2f}%")
            logger.info(f"   🎯 Tokens salvos: {stats['tokens_saved']:,}")
            logger.info(f"   📚 Dicionário: {len(dictionary)} padrões")
            logger.info(f"   🔄 Substituições: {stats['replacements']:,}")
            logger.info(f"   ⏱️ Tempo: {execution_time:.2f}s")

            return {
                'success': True,
                'compressed_text': compressed_text,
                'dictionary': dictionary,
                'stats': stats,
                'execution_time': execution_time,
                'method': 'V22 MEGA'
            }

        except Exception as e:
            logger.error(f"Erro no processamento V22 MEGA: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extrair texto do PDF"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Erro extraindo texto: {e}")
            return ""


def main():
    """Teste do sistema V22 MEGA"""
    print("🔥 DigiLang V22 MEGA")
    print("Compressão Máxima Absoluta com TODOS os Símbolos")
    print("=" * 70)

    # Path do Dark Knight
    pdf_path = "./digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf"

    v22 = DigiLangV22Mega()
    result = v22.process_pdf_mega(pdf_path)

    if result:
        print(f"\n✅ SUCESSO V22 MEGA!")
        print(f"Compressão: {result['stats']['token_compression']:.2f}%")
        print(f"Tokens salvos: {result['stats']['tokens_saved']:,}")
        print(f"Dicionário: {len(result['dictionary'])} padrões")
    else:
        print("❌ Falhou")

    return 0

if __name__ == "__main__":
    main()