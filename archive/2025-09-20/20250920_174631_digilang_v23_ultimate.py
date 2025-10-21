#!/usr/bin/env python3
"""
DigiLang V23 ULTIMATE - Sistema Oficial de Compressão Personalizada
=====================================================================

VERSÃO DEFINITIVA - Compressão Personalizada por PDF
Implementa a estratégia comprovada:
- Mineração personalizada por documento
- Priorização por economia de tokens (nunca substitui palavras de 1 token)
- Uso de TODOS os símbolos disponíveis (1,200+ single-token)

Autor: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion
Data: 14/09/2025
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
import re
from collections import Counter
import PyPDF2
import tiktoken

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TokenPattern:
    """Padrão encontrado no texto com análise de tokens"""
    text: str
    frequency: int
    original_tokens: int
    symbol_tokens: int
    total_savings: int
    savings_per_occurrence: int


@dataclass
class CompressionResult:
    """Resultado da compressão"""
    success: bool
    original_text: str
    compressed_text: str
    dictionary: Dict[str, Dict[str, Any]]
    stats: Dict[str, Any]
    metadata: Dict[str, Any]


class DigiLangV23Ultimate:
    """
    Sistema DEFINITIVO de compressão DigiLang

    Características:
    1. Mineração personalizada por PDF
    2. Usa TODOS os símbolos de 1 token disponíveis
    3. NUNCA substitui palavras de 1 token
    4. Prioriza palavras que consomem MAIS tokens
    5. Suporte para interpretação por AI/Ollama/Digimon
    """

    def __init__(self):
        """Inicializar V23 Ultimate"""
        logger.info("🚀 DigiLang V23 ULTIMATE inicializando...")

        # Tokenizer
        self.encoder = tiktoken.get_encoding("cl100k_base")

        # Descobrir TODOS os símbolos disponíveis
        self.symbols_by_tokens = self._discover_all_symbols()

        logger.info("💎 SÍMBOLOS DISPONÍVEIS:")
        for tokens, symbols in self.symbols_by_tokens.items():
            if symbols:
                logger.info(f"   {tokens} token(s): {len(symbols)} símbolos")

        total = sum(len(s) for s in self.symbols_by_tokens.values())
        logger.info(f"   TOTAL: {total} símbolos únicos disponíveis!")

    def _discover_all_symbols(self) -> Dict[int, List[str]]:
        """Descobrir TODOS os símbolos disponíveis organizados por token count"""
        symbols_by_tokens = {1: [], 2: [], 3: []}

        # Ranges extensivos para cobrir TODOS os símbolos Unicode úteis
        ranges = [
            # Pontuação e símbolos ASCII estendidos
            (0x00A1, 0x00FF),  # Latin-1 Supplement

            # Símbolos de moeda e matemática
            (0x20A0, 0x20CF),  # Currency Symbols
            (0x2100, 0x214F),  # Letterlike Symbols
            (0x2190, 0x21FF),  # Arrows
            (0x2200, 0x22FF),  # Mathematical Operators
            (0x2300, 0x23FF),  # Miscellaneous Technical
            (0x2400, 0x243F),  # Control Pictures
            (0x2460, 0x24FF),  # Enclosed Alphanumerics
            (0x2500, 0x257F),  # Box Drawing
            (0x2580, 0x259F),  # Block Elements
            (0x25A0, 0x25FF),  # Geometric Shapes
            (0x2600, 0x26FF),  # Miscellaneous Symbols
            (0x2700, 0x27BF),  # Dingbats

            # Alfabetos não-latinos
            (0x0370, 0x03FF),  # Greek and Coptic
            (0x0400, 0x04FF),  # Cyrillic
            (0x0530, 0x058F),  # Armenian
            (0x0590, 0x05FF),  # Hebrew
            (0x0600, 0x06FF),  # Arabic
            (0x0E00, 0x0E7F),  # Thai

            # CJK (Chinese, Japanese, Korean)
            (0x3040, 0x309F),  # Hiragana
            (0x30A0, 0x30FF),  # Katakana
            (0x4E00, 0x4FFF),  # CJK Ideographs (subset)
            (0xAC00, 0xACFF),  # Hangul Syllables (subset)

            # Símbolos e Emojis
            (0x1F300, 0x1F3FF),  # Miscellaneous Symbols and Pictographs
            (0x1F400, 0x1F4FF),  # Emoticons
            (0x1F600, 0x1F64F),  # Emoticons
            (0x1F680, 0x1F6FF),  # Transport and Map Symbols
            (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        ]

        # Testar cada range
        for start, end in ranges:
            for codepoint in range(start, min(end + 1, 0x110000)):
                try:
                    char = chr(codepoint)
                    tokens = len(self.encoder.encode(char))

                    if tokens <= 3:
                        symbols_by_tokens[tokens].append(char)
                except:
                    continue

        return symbols_by_tokens

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrair texto do PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Erro ao extrair PDF: {e}")
            return ""

        return text

    def _mine_patterns(self, text: str) -> List[TokenPattern]:
        """
        Minerar TODOS os padrões do texto
        Foca em palavras e frases que consomem múltiplos tokens
        """
        patterns = []

        # 1. Palavras individuais (2+ tokens apenas!)
        words = re.findall(r'\b[A-Za-z][A-Za-z0-9]*\b', text)
        word_freq = Counter(words)

        for word, freq in word_freq.items():
            if freq >= 2:  # Mínimo 2 ocorrências
                tokens = len(self.encoder.encode(word))
                if tokens >= 2:  # APENAS palavras multi-token!
                    patterns.append(TokenPattern(
                        text=word,
                        frequency=freq,
                        original_tokens=tokens,
                        symbol_tokens=1,  # Assumindo símbolo de 1 token
                        total_savings=(tokens - 1) * freq,
                        savings_per_occurrence=tokens - 1
                    ))

        # 2. Frases comuns de roteiro (multi-token)
        screenplay_patterns = [
            r'INT\.\s+[A-Z][A-Z\s]+',  # INT. LOCATION
            r'EXT\.\s+[A-Z][A-Z\s]+',  # EXT. LOCATION
            r'--\s+CONTINUOUS',
            r'FADE\s+IN:?',
            r'FADE\s+OUT:?',
            r'CUT\s+TO:?',
            r'DISSOLVE\s+TO:?',
            r'\([A-Z]+\)',  # (CONT'D), (V.O.), etc
            r'[A-Z][A-Z\s]+--\s+CONTINUOUS',  # LOCATION -- CONTINUOUS
        ]

        for pattern in screenplay_patterns:
            matches = re.findall(pattern, text)
            phrase_freq = Counter(matches)

            for phrase, freq in phrase_freq.items():
                if freq >= 2:
                    tokens = len(self.encoder.encode(phrase))
                    if tokens >= 2:
                        patterns.append(TokenPattern(
                            text=phrase,
                            frequency=freq,
                            original_tokens=tokens,
                            symbol_tokens=1,
                            total_savings=(tokens - 1) * freq,
                            savings_per_occurrence=tokens - 1
                        ))

        # 3. Nomes de personagens (MAIÚSCULAS)
        character_names = re.findall(r'\n([A-Z][A-Z]+)\n', text)
        char_freq = Counter(character_names)

        for char_name, freq in char_freq.items():
            if freq >= 5 and len(char_name) >= 3:
                tokens = len(self.encoder.encode(char_name))
                if tokens >= 2:
                    patterns.append(TokenPattern(
                        text=char_name,
                        frequency=freq,
                        original_tokens=tokens,
                        symbol_tokens=1,
                        total_savings=(tokens - 1) * freq,
                        savings_per_occurrence=tokens - 1
                    ))

        # 4. Bigramas e trigramas frequentes
        words_list = text.split()

        # Bigramas
        for i in range(len(words_list) - 1):
            bigram = f"{words_list[i]} {words_list[i+1]}"
            if bigram.count(' ') == 1:  # Exatamente 2 palavras
                freq = text.count(bigram)
                if freq >= 3:
                    tokens = len(self.encoder.encode(bigram))
                    if tokens >= 3:  # Bigramas geralmente são 3+ tokens
                        patterns.append(TokenPattern(
                            text=bigram,
                            frequency=freq,
                            original_tokens=tokens,
                            symbol_tokens=1,
                            total_savings=(tokens - 1) * freq,
                            savings_per_occurrence=tokens - 1
                        ))

        # Trigramas
        for i in range(len(words_list) - 2):
            trigram = f"{words_list[i]} {words_list[i+1]} {words_list[i+2]}"
            if trigram.count(' ') == 2:  # Exatamente 3 palavras
                freq = text.count(trigram)
                if freq >= 3:
                    tokens = len(self.encoder.encode(trigram))
                    if tokens >= 4:  # Trigramas geralmente são 4+ tokens
                        patterns.append(TokenPattern(
                            text=trigram,
                            frequency=freq,
                            original_tokens=tokens,
                            symbol_tokens=1,
                            total_savings=(tokens - 1) * freq,
                            savings_per_occurrence=tokens - 1
                        ))

        return patterns

    def _create_optimized_dictionary(
        self,
        patterns: List[TokenPattern],
        max_symbols: int = 1500
    ) -> Dict[str, Dict[str, Any]]:
        """
        Criar dicionário otimizado usando TODOS os símbolos disponíveis
        Prioriza por economia total de tokens
        """
        # Ordenar por economia total (maior primeiro)
        patterns.sort(key=lambda x: x.total_savings, reverse=True)

        dictionary = {}
        used_patterns = set()
        symbol_index = 0

        # Usar primeiro TODOS os símbolos de 1 token
        available_1token = self.symbols_by_tokens[1].copy()

        for pattern in patterns:
            if len(dictionary) >= max_symbols:
                break

            if pattern.text in used_patterns:
                continue

            # Verificar se ainda temos símbolos de 1 token
            if symbol_index < len(available_1token):
                symbol = available_1token[symbol_index]
                symbol_tokens = 1
                symbol_index += 1
            else:
                # Se acabaram os de 1 token, usar de 2 tokens
                idx = symbol_index - len(available_1token)
                if idx < len(self.symbols_by_tokens[2]):
                    symbol = self.symbols_by_tokens[2][idx]
                    symbol_tokens = 2
                    symbol_index += 1
                else:
                    break  # Sem mais símbolos disponíveis

            # Só adicionar se realmente economiza tokens
            actual_savings = pattern.original_tokens - symbol_tokens
            if actual_savings > 0:
                dictionary[symbol] = {
                    'text': pattern.text,
                    'frequency': pattern.frequency,
                    'original_tokens': pattern.original_tokens,
                    'symbol_tokens': symbol_tokens,
                    'total_savings': actual_savings * pattern.frequency,
                    'savings_per_occurrence': actual_savings
                }
                used_patterns.add(pattern.text)

        return dictionary

    def _apply_compression(self, text: str, dictionary: Dict[str, Dict]) -> Tuple[str, int]:
        """Aplicar compressão ao texto"""
        compressed = text
        substitutions = 0

        # Ordenar por tamanho do texto (maior primeiro) para evitar substituições parciais
        sorted_items = sorted(
            dictionary.items(),
            key=lambda x: len(x[1]['text']),
            reverse=True
        )

        for symbol, info in sorted_items:
            pattern_text = info['text']
            # Usar word boundaries quando apropriado
            if pattern_text.isalpha():
                # Para palavras, usar word boundaries
                pattern = r'\b' + re.escape(pattern_text) + r'\b'
                count = len(re.findall(pattern, compressed))
                compressed = re.sub(pattern, symbol, compressed)
            else:
                # Para outros padrões, substituição direta
                count = compressed.count(pattern_text)
                compressed = compressed.replace(pattern_text, symbol)

            substitutions += count

        return compressed, substitutions

    def process_pdf(self, pdf_path: str) -> CompressionResult:
        """
        Processar PDF com compressão V23 ULTIMATE

        Args:
            pdf_path: Caminho para o arquivo PDF

        Returns:
            CompressionResult com todos os dados da compressão
        """
        logger.info(f"\n🔥 PROCESSAMENTO V23 ULTIMATE: {Path(pdf_path).name}")
        logger.info("=" * 70)

        # Extrair texto
        text = self._extract_text_from_pdf(pdf_path)
        if not text:
            return CompressionResult(
                success=False,
                original_text="",
                compressed_text="",
                dictionary={},
                stats={'error': 'Failed to extract text'},
                metadata={}
            )

        # Calcular tokens originais
        original_tokens = len(self.encoder.encode(text))
        logger.info(f"📄 Texto original: {len(text):,} chars, {original_tokens:,} tokens")

        # Minerar padrões
        logger.info("⛏️ Minerando padrões personalizados do documento...")
        patterns = self._mine_patterns(text)
        logger.info(f"⛏️ Minerados {len(patterns):,} padrões únicos")

        # Criar dicionário otimizado
        logger.info("📚 Criando dicionário personalizado com priorização inteligente...")
        dictionary = self._create_optimized_dictionary(patterns)

        # Estatísticas do dicionário
        total_1token = sum(1 for s in dictionary.values() if s['symbol_tokens'] == 1)
        total_2token = sum(1 for s in dictionary.values() if s['symbol_tokens'] == 2)
        total_savings = sum(s['total_savings'] for s in dictionary.values())

        logger.info("📊 Dicionário personalizado criado:")
        logger.info(f"   ✅ Padrões totais: {len(dictionary)}")
        logger.info(f"   💎 Símbolos de 1 token: {total_1token}")
        logger.info(f"   💎 Símbolos de 2 tokens: {total_2token}")
        logger.info(f"   💰 Economia estimada: {total_savings:,} tokens")

        # Top padrões
        top_patterns = sorted(
            dictionary.items(),
            key=lambda x: x[1]['total_savings'],
            reverse=True
        )[:10]

        logger.info("\n🏆 TOP 10 PADRÕES POR ECONOMIA:")
        for i, (symbol, info) in enumerate(top_patterns, 1):
            logger.info(
                f"   {i}. '{info['text']}' ({info['frequency']}x, "
                f"{info['original_tokens']}→{info['symbol_tokens']} tokens) "
                f"= {info['total_savings']} tokens salvos"
            )

        # Aplicar compressão
        start_time = time.time()
        compressed_text, substitutions = self._apply_compression(text, dictionary)
        compression_time = time.time() - start_time

        # Calcular tokens finais
        compressed_tokens = len(self.encoder.encode(compressed_text))
        tokens_saved = original_tokens - compressed_tokens
        compression_rate = (tokens_saved / original_tokens) * 100

        # Preparar resultado
        stats = {
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'tokens_saved': tokens_saved,
            'token_compression': compression_rate,
            'original_chars': len(text),
            'compressed_chars': len(compressed_text),
            'char_compression': ((len(text) - len(compressed_text)) / len(text)) * 100,
            'substitutions_made': substitutions,
            'dictionary_size': len(dictionary),
            'compression_time': compression_time
        }

        metadata = {
            'version': 'V23_ULTIMATE',
            'pdf_path': pdf_path,
            'pdf_name': Path(pdf_path).name,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'symbols_available': {
                '1_token': len(self.symbols_by_tokens[1]),
                '2_token': len(self.symbols_by_tokens[2])
            }
        }

        logger.info("\n" + "=" * 70)
        logger.info("🎯 RESULTADOS V23 ULTIMATE:")
        logger.info(f"   📊 Tokens: {original_tokens:,} → {compressed_tokens:,}")
        logger.info(f"   💾 Compressão: {compression_rate:.2f}%")
        logger.info(f"   🎯 Tokens salvos: {tokens_saved:,}")
        logger.info(f"   📚 Dicionário: {len(dictionary)} padrões")
        logger.info(f"   🔄 Substituições: {substitutions:,}")
        logger.info(f"   ⏱️ Tempo: {compression_time:.2f}s")

        return CompressionResult(
            success=True,
            original_text=text,
            compressed_text=compressed_text,
            dictionary=dictionary,
            stats=stats,
            metadata=metadata
        )

    def save_compression_package(self, result: CompressionResult, output_dir: str = "./output/v23_ultimate"):
        """
        Salvar pacote completo de compressão para interpretação por AI/Ollama

        Estrutura:
        - compressed_text.txt: Texto comprimido
        - dictionary.json: Dicionário de substituições
        - metadata.json: Metadados e instruções
        - README.md: Instruções de uso
        """
        output_path = Path(output_dir) / Path(result.metadata['pdf_name']).stem
        output_path.mkdir(parents=True, exist_ok=True)

        # 1. Salvar texto comprimido
        with open(output_path / "compressed_text.txt", 'w', encoding='utf-8') as f:
            f.write(result.compressed_text)

        # 2. Salvar dicionário
        with open(output_path / "dictionary.json", 'w', encoding='utf-8') as f:
            json.dump(result.dictionary, f, ensure_ascii=False, indent=2)

        # 3. Salvar metadados com instruções
        metadata_complete = {
            **result.metadata,
            'stats': result.stats,
            'instructions': {
                'decompression': 'Para descomprimir, substitua cada símbolo pelo texto correspondente no dicionário',
                'format': 'UTF-8 com símbolos Unicode',
                'priority': 'Símbolos representam palavras/frases multi-token frequentes',
                'optimization': 'Focado em economia de tokens, não em compressão de caracteres'
            }
        }

        with open(output_path / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata_complete, f, ensure_ascii=False, indent=2)

        # 4. Criar README interpretável
        readme_content = f"""# DigiLang V23 ULTIMATE - {result.metadata['pdf_name']}

## 📊 Estatísticas de Compressão
- **Tokens originais**: {result.stats['original_tokens']:,}
- **Tokens comprimidos**: {result.stats['compressed_tokens']:,}
- **Taxa de compressão**: {result.stats['token_compression']:.2f}%
- **Tokens economizados**: {result.stats['tokens_saved']:,}

## 🔤 Como Interpretar

### Para AI/Ollama/Digimon:
1. Leia `compressed_text.txt` - texto com símbolos Unicode
2. Leia `dictionary.json` - mapeamento símbolo→texto
3. Para descomprimir: substitua cada símbolo pelo texto original

### Exemplo de Decodificação:
```python
# Pseudocódigo
compressed = read('compressed_text.txt')
dictionary = read('dictionary.json')

decompressed = compressed
for symbol, info in dictionary:
    decompressed = decompressed.replace(symbol, info['text'])
```

## 💡 Princípios da Compressão
1. **Personalizada por documento**: Dicionário único para cada PDF
2. **Priorização inteligente**: Substitui palavras que consomem MAIS tokens
3. **Nunca substitui palavras de 1 token**: Foco em economia real
4. **Símbolos Unicode de 1 token**: Máxima eficiência

## 🎯 Otimizado Para
- Redução de custos em APIs de LLM (OpenAI, Anthropic, etc)
- Processamento eficiente de roteiros e documentos longos
- Manutenção da estrutura e formatação original

---
*DigiLang V23 ULTIMATE - Sistema Oficial ScriptureMon Champion*
"""

        with open(output_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)

        logger.info(f"\n📦 Pacote de compressão salvo em: {output_path}")

        return str(output_path)


def main():
    """Função principal para testes"""
    v23 = DigiLangV23Ultimate()

    # Testar com Dark Knight
    pdf_path = "./digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf"

    if Path(pdf_path).exists():
        result = v23.process_pdf(pdf_path)

        if result.success:
            # Salvar pacote completo
            output_path = v23.save_compression_package(result)

            print(f"\n✅ Compressão V23 ULTIMATE concluída!")
            print(f"📦 Pacote salvo em: {output_path}")
    else:
        print(f"❌ PDF não encontrado: {pdf_path}")


if __name__ == "__main__":
    main()