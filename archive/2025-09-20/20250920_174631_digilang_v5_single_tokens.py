#!/usr/bin/env python3
"""
DigiLang V5 - Single Token Compression
Implementação com caracteres ASCII simples que são exatamente 1 token
DIGIMUNDO PRESENTE
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter

class DigiLangV5SingleToken:
    """
    DigiLang V5 - Usa caracteres ASCII simples como placeholders de 1 token
    """

    def __init__(self):
        # Caracteres ASCII disponíveis para uso como macros (todos são 1 token)
        self.available_chars = list('~!@#$%^&*ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # Macros globais pré-definidas com mapeamento otimizado
        self.global_macros = {
            '~': 'FADE IN:',
            '!': 'FADE OUT.',
            '@': 'CUT TO:',
            '#': 'INT.',
            '$': 'EXT.',
            '%': 'DISSOLVE TO:',
            '^': 'CONTINUOUS',
            '&': 'DAY',
            '*': 'NIGHT',
            'A': 'V.O.',
            'B': 'O.S.',
            'C': 'CONT\'D',
            'D': 'BACK TO:',
            'E': 'MATCH CUT TO:',
            'F': 'SMASH CUT TO:',
            'G': 'BEGIN',
            'H': 'END',
            'I': 'INTERCUT',
            'J': 'MONTAGE',
            'K': 'SERIES OF SHOTS',
            'L': 'ANGLE ON',
            'M': 'CLOSE UP',
            'N': 'WIDE SHOT',
            'O': 'POV',
            'P': 'INSERT',
            'Q': 'FLASHBACK',
            'R': 'LATER',
            'S': 'SUPER:',
            'T': 'TITLE CARD:',
            'U': 'THE END',
            'V': 'BLACK SCREEN',
            'W': 'WHITE SCREEN',
            'X': 'BEAT',
            'Y': 'PAUSE',
            'Z': 'SILENCE'
        }

        # Reverse mapping for quick lookup
        self.reverse_global = {v: k for k, v in self.global_macros.items()}

        # Characters still available for doc-specific macros
        self.remaining_chars = [c for c in self.available_chars
                                if c not in self.global_macros]

        # Try importing tiktoken if available
        self.tokenizer = None
        try:
            import tiktoken
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except ImportError:
            pass

    def _count_tokens(self, text: str) -> int:
        """Conta tokens usando tiktoken ou estimativa"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Estimativa: ~4 caracteres por token
            return len(text) // 4

    def mine_doc_macros(self, text: str, max_macros: int = 10) -> Dict[str, str]:
        """
        Minera macros específicas do documento
        Procura por frases em CAPS que aparecem frequentemente
        """
        if not self.remaining_chars:
            return {}

        # Encontrar palavras/frases em CAPS (nomes de personagens, locais)
        caps_pattern = r'\b[A-Z][A-Z\s\.\-\']+\b'
        matches = re.findall(caps_pattern, text)

        # Contar frequências
        freq_counter = Counter(matches)

        # Filtrar apenas frases que aparecem múltiplas vezes
        # e que valem a pena comprimir (mais de 3 caracteres)
        candidates = []
        for phrase, count in freq_counter.items():
            if count >= 3 and len(phrase) > 3:
                # Calcular ganho
                orig_tokens = self._count_tokens(phrase)
                if orig_tokens > 1:  # Só vale a pena se economizar tokens
                    gain = count * (orig_tokens - 1)
                    candidates.append((phrase, count, gain))

        # Ordenar por ganho
        candidates.sort(key=lambda x: x[2], reverse=True)

        # Selecionar os melhores até o limite
        doc_macros = {}
        for phrase, count, gain in candidates[:max_macros]:
            if self.remaining_chars:
                char = self.remaining_chars.pop(0)
                doc_macros[char] = phrase

        return doc_macros

    def encode(self, text: str, mine_doc_macros: bool = True) -> Tuple[str, Dict[str, str], Dict]:
        """
        Codifica texto usando macros de 1 token

        Args:
            text: Texto para codificar
            mine_doc_macros: Se deve minerar macros específicas do documento

        Returns:
            Tuple de (texto_codificado, macros_usadas, estatísticas)
        """
        # Começar com macros globais
        macros_to_use = {}

        # Verificar quais macros globais estão presentes no texto
        for phrase, char in self.reverse_global.items():
            if phrase in text:
                count = text.count(phrase)
                if count > 0:
                    orig_tokens = self._count_tokens(phrase)
                    gain = count * (orig_tokens - 1)  # char é sempre 1 token
                    if gain > 0:
                        macros_to_use[char] = phrase

        # Minerar macros específicas do documento se solicitado
        doc_macros = {}
        if mine_doc_macros:
            doc_macros = self.mine_doc_macros(text)
            macros_to_use.update(doc_macros)

        # Aplicar substituições (mais longo primeiro para evitar conflitos)
        encoded = text
        replacements = sorted(macros_to_use.items(),
                            key=lambda x: len(x[1]), reverse=True)

        for char, phrase in replacements:
            # Usar word boundaries quando possível
            if phrase.isalpha():
                pattern = r'\b' + re.escape(phrase) + r'\b'
            else:
                pattern = re.escape(phrase)
            encoded = re.sub(pattern, char, encoded)

        # Calcular estatísticas
        original_tokens = self._count_tokens(text)
        encoded_tokens = self._count_tokens(encoded)

        # Adicionar custo do header se houver macros
        header_cost = 0
        if macros_to_use:
            # Estimar custo do header
            header_lines = len(macros_to_use)
            header_cost = header_lines * 4  # Aproximado: "X=phrase\n" ~4 tokens
            encoded_tokens += header_cost

        saved_tokens = original_tokens - encoded_tokens
        compression_ratio = (saved_tokens / original_tokens * 100) if original_tokens > 0 else 0

        stats = {
            'original_tokens': original_tokens,
            'encoded_tokens': encoded_tokens,
            'saved_tokens': saved_tokens,
            'compression_ratio': compression_ratio,
            'macros_used': len(macros_to_use),
            'header_cost': header_cost
        }

        # Adicionar header ao texto codificado se houver macros
        if macros_to_use:
            header = "===MACROS===\n"
            for char, phrase in sorted(macros_to_use.items()):
                header += f"{char}={phrase}\n"
            header += "===TEXT===\n"
            final_encoded = header + encoded
        else:
            final_encoded = encoded

        return final_encoded, macros_to_use, stats

    def decode(self, encoded_text: str) -> str:
        """
        Decodifica texto codificado

        Args:
            encoded_text: Texto com macros

        Returns:
            Texto original expandido
        """
        # Verificar se tem header de macros
        if "===MACROS===" in encoded_text and "===TEXT===" in encoded_text:
            # Extrair header
            macro_start = encoded_text.find("===MACROS===\n") + len("===MACROS===\n")
            macro_end = encoded_text.find("===TEXT===")
            text_start = macro_end + len("===TEXT===\n")

            # Parse macros
            macro_section = encoded_text[macro_start:macro_end]
            body = encoded_text[text_start:]

            macros = {}
            for line in macro_section.strip().split('\n'):
                if '=' in line:
                    char, phrase = line.split('=', 1)
                    macros[char] = phrase

            # Expandir macros
            decoded = body
            # Ordenar por tamanho do char (não importa muito aqui)
            for char, phrase in sorted(macros.items(), key=lambda x: len(x[0]), reverse=True):
                decoded = decoded.replace(char, phrase)

            return decoded
        else:
            # Sem macros, retornar como está
            return encoded_text

    def test_compression(self, text: str) -> None:
        """
        Testa e exibe resultados de compressão

        Args:
            text: Texto para testar
        """
        print("="*60)
        print("DIGILANG V5 - SINGLE TOKEN COMPRESSION TEST")
        print("="*60)

        # Encode
        encoded, macros, stats = self.encode(text)

        print(f"\nOriginal ({stats['original_tokens']} tokens):")
        print(text[:200] + "..." if len(text) > 200 else text)

        print(f"\nEncoded ({stats['encoded_tokens']} tokens):")
        print(encoded[:200] + "..." if len(encoded) > 200 else encoded)

        print(f"\nMacros used ({len(macros)}):")
        for char, phrase in sorted(macros.items())[:10]:
            print(f"  {char} = {phrase}")

        print(f"\nStatistics:")
        print(f"  Original tokens: {stats['original_tokens']}")
        print(f"  Encoded tokens: {stats['encoded_tokens']}")
        print(f"  Saved tokens: {stats['saved_tokens']}")
        print(f"  Compression ratio: {stats['compression_ratio']:.1f}%")
        print(f"  Header cost: {stats['header_cost']} tokens")

        # Test decode
        decoded = self.decode(encoded)
        if decoded == text:
            print("  ✅ Decode successful - matches original")
        else:
            print("  ❌ Decode failed - mismatch!")

        print("="*60)


def main():
    """Teste do DigiLang V5"""

    # Criar instância
    compressor = DigiLangV5SingleToken()

    # Teste 1: Texto simples
    test1 = "FADE IN: INT. OFFICE - DAY CUT TO: EXT. STREET - NIGHT"
    compressor.test_compression(test1)

    # Teste 2: Texto de roteiro mais complexo
    test2 = """FADE IN:

INT. COFFEE SHOP - DAY

JOHN enters, looking around nervously.

JOHN
(to barista)
Just a coffee, black.

CUT TO:

EXT. STREET - CONTINUOUS

John exits with his coffee.

FADE OUT."""

    compressor.test_compression(test2)

    print("\nDIGIMUNDO PRESENTE")


if __name__ == "__main__":
    main()