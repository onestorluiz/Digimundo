#!/usr/bin/env python3
"""
FASE 20 - DigiLang V20 EXTREME - Compressão Máxima Absoluta
Sistema ScriptureMon Champion

UTILIZA TODOS OS SÍMBOLOS DE 1 TOKEN DISPONÍVEIS
- Mineração exaustiva de padrões
- Análise profunda de repetições
- Uso de TODOS caracteres Unicode de 1 token
- Combinação V19 Personalizado + Batman Ultimate

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
class ExtremePattern:
    """Padrão para compressão extrema"""
    text: str
    frequency: int
    original_tokens: int
    savings: int
    category: str  # word, bigram, trigram, phrase, name, location, etc.

class DigiLangV20Extreme:
    """DigiLang V20 EXTREME - Máxima compressão possível"""

    def __init__(self):
        """Inicializar sistema EXTREME"""
        self.encoder = tiktoken.get_encoding("cl100k_base")

        # TODOS os símbolos de 1 token validados extensivamente
        self.all_single_token_symbols = self._discover_all_single_tokens()

        logger.info(f"🔥 DigiLang V20 EXTREME inicializado")
        logger.info(f"💎 Total de símbolos de 1 token: {len(self.all_single_token_symbols)}")

    def _discover_all_single_tokens(self) -> List[str]:
        """Descobrir TODOS os símbolos Unicode que são 1 token"""
        single_tokens = []

        # Ranges validados que contêm símbolos de 1 token
        ranges = [
            (0x20, 0x7F),      # ASCII printable (exceto espaço)
            (0xA0, 0x17F),     # Latin-1 Supplement + Extended A
            (0x180, 0x24F),    # Latin Extended B
            (0x250, 0x2AF),    # IPA Extensions
            (0x370, 0x3FF),    # Greek and Coptic
            (0x400, 0x4FF),    # Cyrillic
            (0x1E00, 0x1EFF),  # Latin Extended Additional
            (0x2000, 0x206F),  # General Punctuation
            (0x2070, 0x209F),  # Superscripts and Subscripts
            (0x20A0, 0x20CF),  # Currency Symbols
            (0x2100, 0x214F),  # Letterlike Symbols
            (0x2190, 0x21FF),  # Arrows
            (0x2200, 0x22FF),  # Mathematical Operators
            (0x2300, 0x23FF),  # Miscellaneous Technical
            (0x2460, 0x24FF),  # Enclosed Alphanumerics
            (0x2500, 0x257F),  # Box Drawing
            (0x25A0, 0x25FF),  # Geometric Shapes
            (0x2600, 0x26FF),  # Miscellaneous Symbols
            (0x2700, 0x27BF),  # Dingbats
        ]

        # Testar cada caractere
        for start, end in ranges:
            for codepoint in range(start, end + 1):
                try:
                    char = chr(codepoint)
                    # Verificar se é exatamente 1 token
                    if len(self.encoder.encode(char)) == 1:
                        # Excluir caracteres problemáticos (espaço, newline, etc)
                        if char not in [' ', '\n', '\t', '\r', '\x00', '\x0b', '\x0c']:
                            single_tokens.append(char)
                except (ValueError, UnicodeDecodeError):
                    continue

        # Adicionar símbolos especiais que não queremos usar para texto normal
        # mas são ótimos para compressão (não vão conflitar com o texto)
        special_symbols = []
        for char in single_tokens[:]:
            # Mover números e letras ASCII para o final (menos prioridade)
            if char.isalnum() and ord(char) < 128:
                single_tokens.remove(char)
                special_symbols.append(char)

        # Reordenar: símbolos especiais primeiro, ASCII depois
        single_tokens = single_tokens + special_symbols

        logger.info(f"🔍 Descobertos {len(single_tokens)} símbolos de 1 token")

        return single_tokens

    def extreme_mine_patterns(self, text: str) -> List[ExtremePattern]:
        """Mineração EXTREMA de padrões - encontra TUDO que se repete"""
        patterns = []

        logger.info("⛏️ Iniciando mineração EXTREMA de padrões...")

        # 1. TODAS as palavras individuais
        words = re.findall(r'\b\w+\b', text)
        word_freq = Counter(words)

        for word, freq in word_freq.items():
            if freq > 1:  # Qualquer repetição
                tokens = len(self.encoder.encode(word))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=word,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='word'
                    ))

        logger.info(f"   📝 Palavras: {len([p for p in patterns if p.category == 'word'])}")

        # 2. Bigramas (sequências de 2 palavras)
        bigrams = []
        words_list = text.split()
        for i in range(len(words_list) - 1):
            bigram = f"{words_list[i]} {words_list[i+1]}"
            if len(bigram) < 50:  # Limite razoável
                bigrams.append(bigram)

        bigram_freq = Counter(bigrams)
        for bigram, freq in bigram_freq.items():
            if freq > 2:
                tokens = len(self.encoder.encode(bigram))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=bigram,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='bigram'
                    ))

        logger.info(f"   📝 Bigramas: {len([p for p in patterns if p.category == 'bigram'])}")

        # 3. Trigramas (sequências de 3 palavras)
        trigrams = []
        for i in range(len(words_list) - 2):
            trigram = f"{words_list[i]} {words_list[i+1]} {words_list[i+2]}"
            if len(trigram) < 60:
                trigrams.append(trigram)

        trigram_freq = Counter(trigrams)
        for trigram, freq in trigram_freq.items():
            if freq > 2:
                tokens = len(self.encoder.encode(trigram))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=trigram,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='trigram'
                    ))

        logger.info(f"   📝 Trigramas: {len([p for p in patterns if p.category == 'trigram'])}")

        # 4. Nomes próprios (palavras em maiúsculas)
        names = re.findall(r'\b[A-Z][A-Z]+(?:\s+[A-Z]+)*\b', text)
        name_freq = Counter(names)

        for name, freq in name_freq.items():
            if freq > 1:
                tokens = len(self.encoder.encode(name))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=name,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='name'
                    ))

        logger.info(f"   👤 Nomes: {len([p for p in patterns if p.category == 'name'])}")

        # 5. Localizações (INT./EXT. patterns)
        locations = re.findall(r'(?:INT\.|EXT\.)\s+[A-Z][^-\n]+(?:-|$)', text)
        location_freq = Counter(locations)

        for location, freq in location_freq.items():
            if freq > 1:
                tokens = len(self.encoder.encode(location))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=location.strip(),
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='location'
                    ))

        logger.info(f"   📍 Localizações: {len([p for p in patterns if p.category == 'location'])}")

        # 6. Elementos técnicos de roteiro
        tech_patterns = [
            'FADE IN:', 'FADE OUT', 'CUT TO:', 'DISSOLVE TO:',
            'CONTINUED:', 'BACK TO:', 'LATER', 'MOMENTS LATER',
            'ANGLE ON:', 'CLOSE ON:', 'V.O.', 'O.S.', 'CONT\'D',
            'BEGIN FLASHBACK', 'END FLASHBACK', 'MONTAGE',
            'END MONTAGE', 'SUPER:', 'INSERT:', 'INTERCUT:'
        ]

        for tech in tech_patterns:
            freq = text.count(tech)
            if freq > 0:
                tokens = len(self.encoder.encode(tech))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=tech,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='technical'
                    ))

        logger.info(f"   🎬 Técnicos: {len([p for p in patterns if p.category == 'technical'])}")

        # 7. Sequências de caracteres repetidas (incluindo pontuação)
        all_sequences = re.findall(r'.{2,30}', text)
        seq_freq = Counter(all_sequences)

        for seq, freq in seq_freq.items():
            if freq > 3 and seq not in [p.text for p in patterns]:
                tokens = len(self.encoder.encode(seq))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=seq,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='sequence'
                    ))

        logger.info(f"   🔤 Sequências: {len([p for p in patterns if p.category == 'sequence'])}")

        # 8. Frases comuns em diálogos
        dialogue_patterns = [
            "I don't", "I'm not", "You don't", "You can't",
            "We have to", "We need to", "I need to", "You need to",
            "What are you", "Where are you", "Who are you",
            "I want to", "I have to", "You have to",
            "Let me", "Let's go", "Come on", "Get out",
            "What's going on", "What happened", "Are you okay",
            "I'm sorry", "Thank you", "You're welcome"
        ]

        for phrase in dialogue_patterns:
            freq = text.lower().count(phrase.lower())
            if freq > 0:
                tokens = len(self.encoder.encode(phrase))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=phrase,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='dialogue'
                    ))

        logger.info(f"   💬 Diálogos: {len([p for p in patterns if p.category == 'dialogue'])}")

        # 9. Números e datas
        numbers = re.findall(r'\b\d+\b', text)
        num_freq = Counter(numbers)

        for num, freq in num_freq.items():
            if freq > 2 and len(num) > 1:
                tokens = len(self.encoder.encode(num))
                if tokens > 1:
                    patterns.append(ExtremePattern(
                        text=num,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='number'
                    ))

        logger.info(f"   🔢 Números: {len([p for p in patterns if p.category == 'number'])}")

        # 10. Padrões específicos do documento
        # Analisar linhas completas que se repetem
        lines = text.split('\n')
        line_freq = Counter(lines)

        for line, freq in line_freq.items():
            if freq > 1 and 5 < len(line) < 100:
                tokens = len(self.encoder.encode(line))
                if tokens > 2:
                    patterns.append(ExtremePattern(
                        text=line,
                        frequency=freq,
                        original_tokens=tokens,
                        savings=(tokens - 1) * freq,
                        category='line'
                    ))

        logger.info(f"   📄 Linhas: {len([p for p in patterns if p.category == 'line'])}")

        # Remover duplicatas e ordenar por economia
        unique_patterns = {}
        for p in patterns:
            if p.text not in unique_patterns or p.savings > unique_patterns[p.text].savings:
                unique_patterns[p.text] = p

        patterns = list(unique_patterns.values())
        patterns.sort(key=lambda x: x.savings, reverse=True)

        logger.info(f"⛏️ Total de padrões minerados: {len(patterns)}")

        # Estatísticas
        total_savings = sum(p.savings for p in patterns)
        logger.info(f"💰 Economia potencial total: {total_savings:,} tokens")

        return patterns

    def create_extreme_dictionary(self, patterns: List[ExtremePattern]) -> Dict[str, str]:
        """Criar dicionário EXTREME usando TODOS os símbolos disponíveis"""

        dictionary = {}

        # Usar TODOS os símbolos disponíveis
        max_patterns = min(len(patterns), len(self.all_single_token_symbols))

        logger.info(f"📚 Criando dicionário EXTREME com {max_patterns} padrões")

        # Atribuir símbolos aos padrões mais valiosos
        for i in range(max_patterns):
            pattern = patterns[i]
            symbol = self.all_single_token_symbols[i]
            dictionary[pattern.text] = symbol

        # Estatísticas por categoria
        categories = {}
        for pattern in patterns[:max_patterns]:
            if pattern.category not in categories:
                categories[pattern.category] = 0
            categories[pattern.category] += 1

        logger.info("📊 Distribuição do dicionário:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {cat}: {count} padrões")

        # Top 20 padrões
        logger.info("\n🔝 Top 20 padrões por economia:")
        for i, pattern in enumerate(patterns[:20]):
            symbol = dictionary.get(pattern.text, '?')
            logger.info(f"   {i+1}. '{pattern.text[:40]}' ({pattern.frequency}x) → '{symbol}' = {pattern.savings} tokens")

        return dictionary

    def compress_extreme(self, text: str, dictionary: Dict[str, str]) -> Tuple[str, Dict]:
        """Compressão EXTREMA com dicionário máximo"""

        compressed = text
        replacements = 0

        # Ordenar por tamanho (maiores primeiro) para evitar substituições parciais
        sorted_patterns = sorted(
            dictionary.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        # Aplicar todas as substituições
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

    def process_pdf_extreme(self, pdf_path: str) -> Dict:
        """Processar PDF com compressão EXTREMA"""

        try:
            start_time = time.time()

            logger.info(f"\n🔥 PROCESSAMENTO EXTREME: {Path(pdf_path).name}")
            logger.info("=" * 60)

            # Extrair texto
            text = self._extract_pdf_text(pdf_path)
            if not text:
                return None

            # Estatísticas originais
            original_tokens = len(self.encoder.encode(text))
            logger.info(f"📄 Texto original: {len(text):,} chars, {original_tokens:,} tokens")

            # Mineração EXTREMA
            patterns = self.extreme_mine_patterns(text)

            # Criar dicionário EXTREME
            dictionary = self.create_extreme_dictionary(patterns)

            # Comprimir
            compressed_text, stats = self.compress_extreme(text, dictionary)

            execution_time = time.time() - start_time

            # Resultados
            logger.info("\n" + "=" * 60)
            logger.info("🎯 RESULTADOS EXTREME:")
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
                        'savings': p.savings,
                        'category': p.category
                    } for p in patterns[:len(dictionary)]
                ],
                'stats': stats,
                'execution_time': execution_time,
                'method': 'V20 EXTREME'
            }

        except Exception as e:
            logger.error(f"Erro no processamento EXTREME: {e}")
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
    """Teste do sistema V20 EXTREME"""
    print("🔥 DigiLang V20 EXTREME")
    print("Compressão Máxima Absoluta")
    print("=" * 60)

    # Path do Dark Knight
    pdf_path = "./digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf"

    v20 = DigiLangV20Extreme()
    result = v20.process_pdf_extreme(pdf_path)

    if result:
        print(f"\n✅ SUCESSO EXTREME!")
        print(f"Compressão: {result['stats']['token_compression']:.2f}%")
        print(f"Tokens salvos: {result['stats']['tokens_saved']:,}")
        print(f"Dicionário: {len(result['dictionary'])} padrões")
    else:
        print("❌ Falhou")

    return 0

if __name__ == "__main__":
    main()