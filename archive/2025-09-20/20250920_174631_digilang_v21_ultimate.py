#!/usr/bin/env python3
"""
FASE 21 - DigiLang V21 ULTIMATE - Priorização por Economia Máxima
Sistema ScriptureMon Champion

REGRAS FUNDAMENTAIS:
1. NUNCA substituir palavras que já são 1 token
2. Priorizar palavras que gastam MAIS tokens (maior economia)
3. Usar TODOS os símbolos de 1 token disponíveis
4. Depois usar símbolos de 2 tokens
5. Mineração exaustiva de TODAS as palavras

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
class TokenPattern:
    """Padrão com análise de tokens"""
    text: str
    frequency: int
    original_tokens: int
    symbol_tokens: int  # Tokens do símbolo substituto
    total_savings: int  # Economia total (frequency * (original - symbol))
    savings_per_occurrence: int  # Economia por ocorrência

class DigiLangV21Ultimate:
    """DigiLang V21 ULTIMATE - Economia máxima por priorização inteligente"""

    def __init__(self):
        """Inicializar sistema V21 ULTIMATE"""
        self.encoder = tiktoken.get_encoding("cl100k_base")

        # Descobrir TODOS os símbolos disponíveis
        self.single_token_symbols = self._get_all_single_token_symbols()
        self.double_token_symbols = self._get_double_token_symbols()

        logger.info(f"🚀 DigiLang V21 ULTIMATE inicializado")
        logger.info(f"💎 Símbolos de 1 token: {len(self.single_token_symbols)}")
        logger.info(f"💎 Símbolos de 2 tokens: {len(self.double_token_symbols)}")

    def _get_all_single_token_symbols(self) -> List[str]:
        """Obter TODOS os símbolos de 1 token disponíveis"""
        symbols = []

        # Não usar letras e números ASCII comuns (preservar legibilidade básica)
        # Mas usar TODOS os símbolos especiais
        ranges = [
            # Símbolos ASCII especiais (exceto letras e números)
            (0x21, 0x2F),   # ! " # $ % & ' ( ) * + , - . /
            (0x3A, 0x40),   # : ; < = > ? @
            (0x5B, 0x60),   # [ \ ] ^ _ `
            (0x7B, 0x7E),   # { | } ~

            # Latin-1 Supplement (símbolos especiais)
            (0xA1, 0xFF),   # ¡ ¢ £ ¤ ¥ ¦ § ¨ © ª « ¬ ­ ® ¯ etc.

            # Latin Extended
            (0x100, 0x17F),
            (0x180, 0x24F),

            # Símbolos especiais diversos
            (0x250, 0x2AF),  # IPA Extensions
            (0x370, 0x3FF),  # Greek
            (0x400, 0x4FF),  # Cyrillic
            (0x1E00, 0x1EFF), # Latin Extended Additional

            # Símbolos matemáticos e técnicos
            (0x2000, 0x206F),  # General Punctuation
            (0x2070, 0x209F),  # Superscripts
            (0x20A0, 0x20CF),  # Currency
            (0x2100, 0x214F),  # Letterlike
            (0x2190, 0x21FF),  # Arrows
            (0x2200, 0x22FF),  # Math Operators
            (0x2300, 0x23FF),  # Misc Technical
            (0x2460, 0x24FF),  # Enclosed Alphanumerics
            (0x2500, 0x257F),  # Box Drawing
            (0x25A0, 0x25FF),  # Geometric Shapes
            (0x2600, 0x26FF),  # Misc Symbols
            (0x2700, 0x27BF),  # Dingbats
        ]

        for start, end in ranges:
            for codepoint in range(start, end + 1):
                try:
                    char = chr(codepoint)
                    if len(self.encoder.encode(char)) == 1:
                        # Excluir espaço e caracteres de controle
                        if char not in [' ', '\n', '\t', '\r', '\x00']:
                            symbols.append(char)
                except:
                    pass

        return symbols

    def _get_double_token_symbols(self) -> List[str]:
        """Obter símbolos de 2 tokens para usar depois"""
        symbols = []

        # Testar combinações comuns que são 2 tokens
        test_chars = ['##', '@@', '$$', '%%', '&&', '**', '++', '--', '//', '::',
                      '<<', '>>', '==', '!=', '<=', '>=', '||', '&&', '~~', '``',
                      '""', "''", '()', '[]', '{}', '<>', '/*', '*/', '//', '\\\\']

        for char_combo in test_chars:
            if len(self.encoder.encode(char_combo)) == 2:
                symbols.append(char_combo)

        # Adicionar emojis comuns que são 2 tokens
        emojis = ['😀', '😃', '😄', '😁', '😅', '😂', '🤣', '😊', '😇', '🙂',
                  '🔥', '💯', '✨', '💫', '⭐', '🌟', '💥', '💢', '💤', '💨']

        for emoji in emojis:
            token_count = len(self.encoder.encode(emoji))
            if token_count == 2:
                symbols.append(emoji)
            elif token_count == 1:
                # Se for 1 token, adicionar aos símbolos de 1 token!
                if emoji not in self.single_token_symbols:
                    self.single_token_symbols.append(emoji)

        return symbols

    def analyze_all_patterns(self, text: str) -> List[TokenPattern]:
        """Analisar TODOS os padrões e calcular economia de tokens"""
        patterns = []
        analyzed = {}

        logger.info("🔍 Analisando TODOS os padrões do texto...")

        # 1. Analisar TODAS as palavras
        words = re.findall(r'\b[\w\']+\b', text)
        word_freq = Counter(words)

        for word, freq in word_freq.items():
            if freq > 1:  # Só vale a pena se repetir
                original_tokens = len(self.encoder.encode(word))

                # REGRA FUNDAMENTAL: Nunca substituir palavras de 1 token!
                if original_tokens > 1:
                    # Calcular economia com símbolo de 1 token
                    savings_1_token = (original_tokens - 1) * freq

                    patterns.append(TokenPattern(
                        text=word,
                        frequency=freq,
                        original_tokens=original_tokens,
                        symbol_tokens=1,
                        total_savings=savings_1_token,
                        savings_per_occurrence=original_tokens - 1
                    ))
                    analyzed[word] = True

        logger.info(f"   📝 Palavras multi-token: {len(patterns)}")

        # 2. Analisar frases comuns (2-5 palavras)
        for n in range(2, 6):  # Bigrams até 5-grams
            ngrams = []
            words_list = text.split()

            for i in range(len(words_list) - n + 1):
                ngram = ' '.join(words_list[i:i+n])
                if len(ngram) < 100:  # Limite razoável
                    ngrams.append(ngram)

            ngram_freq = Counter(ngrams)

            for ngram, freq in ngram_freq.items():
                if freq > 2 and ngram not in analyzed:
                    original_tokens = len(self.encoder.encode(ngram))

                    if original_tokens > 2:  # Só vale a pena para 3+ tokens
                        savings_1_token = (original_tokens - 1) * freq

                        patterns.append(TokenPattern(
                            text=ngram,
                            frequency=freq,
                            original_tokens=original_tokens,
                            symbol_tokens=1,
                            total_savings=savings_1_token,
                            savings_per_occurrence=original_tokens - 1
                        ))
                        analyzed[ngram] = True

        logger.info(f"   📝 Frases multi-token: {len([p for p in patterns if ' ' in p.text])}")

        # 3. Elementos técnicos de roteiro (sempre multi-token)
        tech_patterns = [
            'FADE IN:', 'FADE OUT', 'CUT TO:', 'DISSOLVE TO:', 'CONTINUED:',
            'BACK TO:', 'LATER', 'MOMENTS LATER', 'ANGLE ON:', 'CLOSE ON:',
            'BEGIN FLASHBACK', 'END FLASHBACK', 'MONTAGE', 'END MONTAGE',
            'SUPER:', 'INSERT:', 'INTERCUT:', 'TIME CUT:', 'MATCH CUT:',
            'JUMP CUT:', 'SMASH CUT:', 'FREEZE FRAME:', 'SLOW MOTION:',
            'INT.', 'EXT.', 'INT/EXT', 'I/E', 'V.O.', 'O.S.', 'O.C.',
            'CONT\'D', '(CONT\'D)', '(V.O.)', '(O.S.)', '(O.C.)',
            'DAY', 'NIGHT', 'DAWN', 'DUSK', 'MORNING', 'AFTERNOON',
            'EVENING', 'CONTINUOUS', 'SAME', 'LATER', 'MOMENTS LATER'
        ]

        for tech in tech_patterns:
            freq = text.count(tech)
            if freq > 0 and tech not in analyzed:
                original_tokens = len(self.encoder.encode(tech))

                if original_tokens > 1:
                    savings_1_token = (original_tokens - 1) * freq

                    patterns.append(TokenPattern(
                        text=tech,
                        frequency=freq,
                        original_tokens=original_tokens,
                        symbol_tokens=1,
                        total_savings=savings_1_token,
                        savings_per_occurrence=original_tokens - 1
                    ))
                    analyzed[tech] = True

        # 4. Nomes completos (sempre multi-token)
        full_names = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text)
        name_freq = Counter(full_names)

        for name, freq in name_freq.items():
            if freq > 2 and name not in analyzed:
                original_tokens = len(self.encoder.encode(name))

                if original_tokens > 1:
                    savings_1_token = (original_tokens - 1) * freq

                    patterns.append(TokenPattern(
                        text=name,
                        frequency=freq,
                        original_tokens=original_tokens,
                        symbol_tokens=1,
                        total_savings=savings_1_token,
                        savings_per_occurrence=original_tokens - 1
                    ))

        # 5. Localizações completas
        locations = re.findall(r'(?:INT\.|EXT\.)\s+[A-Z][^-\n]+', text)
        loc_freq = Counter(locations)

        for loc, freq in loc_freq.items():
            if freq > 1 and loc not in analyzed:
                original_tokens = len(self.encoder.encode(loc))

                if original_tokens > 2:
                    savings_1_token = (original_tokens - 1) * freq

                    patterns.append(TokenPattern(
                        text=loc.strip(),
                        frequency=freq,
                        original_tokens=original_tokens,
                        symbol_tokens=1,
                        total_savings=savings_1_token,
                        savings_per_occurrence=original_tokens - 1
                    ))

        # ORDENAR POR ECONOMIA TOTAL (mais economia primeiro)
        patterns.sort(key=lambda x: x.total_savings, reverse=True)

        # Estatísticas
        total_potential_savings = sum(p.total_savings for p in patterns)
        patterns_over_5_tokens = [p for p in patterns if p.original_tokens >= 5]
        patterns_over_10_tokens = [p for p in patterns if p.original_tokens >= 10]

        logger.info(f"📊 Análise completa:")
        logger.info(f"   Total de padrões: {len(patterns)}")
        logger.info(f"   Padrões de 5+ tokens: {len(patterns_over_5_tokens)}")
        logger.info(f"   Padrões de 10+ tokens: {len(patterns_over_10_tokens)}")
        logger.info(f"   Economia potencial total: {total_potential_savings:,} tokens")

        return patterns

    def create_ultimate_dictionary(self, patterns: List[TokenPattern]) -> Dict[str, str]:
        """Criar dicionário ULTIMATE usando todos os símbolos disponíveis"""
        dictionary = {}

        # Usar TODOS os símbolos de 1 token primeiro
        symbol_index = 0
        patterns_used = 0

        logger.info(f"📚 Criando dicionário ULTIMATE...")

        for pattern in patterns:
            if symbol_index < len(self.single_token_symbols):
                dictionary[pattern.text] = self.single_token_symbols[symbol_index]
                symbol_index += 1
                patterns_used += 1
            else:
                break

        logger.info(f"   ✅ Usados {patterns_used} símbolos de 1 token")

        # Se acabaram os símbolos de 1 token, usar os de 2 tokens
        if symbol_index >= len(self.single_token_symbols) and self.double_token_symbols:
            double_index = 0

            for pattern in patterns[patterns_used:]:
                if double_index < len(self.double_token_symbols):
                    # Só vale a pena se economizar pelo menos 1 token
                    if pattern.original_tokens > 2:
                        dictionary[pattern.text] = self.double_token_symbols[double_index]
                        double_index += 1
                else:
                    break

            logger.info(f"   ✅ Usados {double_index} símbolos de 2 tokens")

        # Mostrar top padrões
        logger.info("\n🏆 TOP 20 PADRÕES POR ECONOMIA:")
        for i, pattern in enumerate(patterns[:20]):
            symbol = dictionary.get(pattern.text, '❌')
            logger.info(
                f"   {i+1}. '{pattern.text[:30]}' "
                f"({pattern.frequency}x, {pattern.original_tokens} tokens) → '{symbol}' "
                f"= {pattern.total_savings} tokens salvos"
            )

        return dictionary

    def compress_ultimate(self, text: str, dictionary: Dict[str, str]) -> Tuple[str, Dict]:
        """Compressão ULTIMATE com priorização inteligente"""
        compressed = text
        replacements = 0
        tokens_saved = 0

        # Ordenar por tamanho (maiores primeiro) para evitar substituições parciais
        sorted_patterns = sorted(
            dictionary.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        # Aplicar substituições
        for pattern, symbol in sorted_patterns:
            count = compressed.count(pattern)
            if count > 0:
                # Calcular economia real
                original_tokens = len(self.encoder.encode(pattern))
                symbol_tokens = len(self.encoder.encode(symbol))
                saved = (original_tokens - symbol_tokens) * count

                compressed = compressed.replace(pattern, symbol)
                replacements += count
                tokens_saved += saved

        # Estatísticas finais
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
            'tokens_saved': original_tokens - compressed_tokens,
            'theoretical_savings': tokens_saved
        }

        return compressed, stats

    def process_pdf_ultimate(self, pdf_path: str) -> Dict:
        """Processar PDF com compressão V21 ULTIMATE"""
        try:
            start_time = time.time()

            logger.info(f"\n💪 PROCESSAMENTO V21 ULTIMATE: {Path(pdf_path).name}")
            logger.info("=" * 70)

            # Extrair texto
            text = self._extract_pdf_text(pdf_path)
            if not text:
                return None

            # Estatísticas originais
            original_tokens = len(self.encoder.encode(text))
            logger.info(f"📄 Texto original: {len(text):,} chars, {original_tokens:,} tokens")

            # Análise completa de padrões
            patterns = self.analyze_all_patterns(text)

            # Criar dicionário ultimate
            dictionary = self.create_ultimate_dictionary(patterns)

            # Comprimir
            compressed_text, stats = self.compress_ultimate(text, dictionary)

            execution_time = time.time() - start_time

            # Resultados
            logger.info("\n" + "=" * 70)
            logger.info("🎯 RESULTADOS V21 ULTIMATE:")
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
                'patterns': [
                    {
                        'text': p.text,
                        'frequency': p.frequency,
                        'original_tokens': p.original_tokens,
                        'total_savings': p.total_savings
                    } for p in patterns[:len(dictionary)]
                ],
                'stats': stats,
                'execution_time': execution_time,
                'method': 'V21 ULTIMATE'
            }

        except Exception as e:
            logger.error(f"Erro no processamento V21: {e}")
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
    """Teste do sistema V21 ULTIMATE"""
    print("💪 DigiLang V21 ULTIMATE")
    print("Priorização por Economia Máxima")
    print("=" * 70)

    # Path do Dark Knight
    pdf_path = "./digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf"

    v21 = DigiLangV21Ultimate()
    result = v21.process_pdf_ultimate(pdf_path)

    if result:
        print(f"\n✅ SUCESSO V21 ULTIMATE!")
        print(f"Compressão: {result['stats']['token_compression']:.2f}%")
        print(f"Tokens salvos: {result['stats']['tokens_saved']:,}")
        print(f"Dicionário: {len(result['dictionary'])} padrões")
    else:
        print("❌ Falhou")

    return 0

if __name__ == "__main__":
    main()