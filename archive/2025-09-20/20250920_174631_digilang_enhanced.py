#!/usr/bin/env python3
"""
DigiLang Enhanced - Versão melhorada com mais compressão mas 100% reversível
"""

import re
import hashlib
from typing import Dict, List, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class DigiLangEnhanced:
    """
    Compressor DigiLang melhorado.
    Estratégias adicionais de compressão, mantendo reversibilidade.
    """

    def __init__(self):
        """Inicializa o compressor melhorado."""

        # ESTRATÉGIA 1: Padrões básicos (como antes)
        self.basic_patterns = {
            # Elementos de roteiro
            "FADE IN:": "⟦FI⟧",
            "FADE OUT:": "⟦FO⟧",
            "CUT TO:": "⟦CT⟧",
            "INT.": "⟦I⟧",
            "EXT.": "⟦E⟧",
            "DAY": "⟦D⟧",
            "NIGHT": "⟦N⟧",
            "CONTINUOUS": "⟦C⟧",
            "(V.O.)": "⟦VO⟧",
            "(O.S.)": "⟦OS⟧",
            "(CONT'D)": "⟦CD⟧",

            # Palavras comuns
            " que ": "⟦q⟧",
            " de ": "⟦d⟧",
            " para ": "⟦p⟧",
            " com ": "⟦c⟧",
            " não ": "⟦n⟧",
        }

        # ESTRATÉGIA 2: Padrões de múltiplos espaços (preservando significado)
        self.space_patterns = {
            "\n\n\n\n": "⟦4n⟧",  # 4 quebras
            "\n\n\n": "⟦3n⟧",    # 3 quebras
            "\n\n": "⟦2n⟧",      # 2 quebras (comum em roteiros)
            "    ": "⟦4s⟧",      # 4 espaços (indentação)
            "  ": "⟦2s⟧",        # 2 espaços
        }

        # ESTRATÉGIA 3: Frases completas comuns
        self.phrase_patterns = {
            "ele olha para": "⟦eop⟧",
            "ela olha para": "⟦aop⟧",
            "vira-se para": "⟦vsp⟧",
            "entra no": "⟦en⟧",
            "sai do": "⟦sd⟧",
            "pega o": "⟦po⟧",
            "está sentado": "⟦es⟧",
            "está em pé": "⟦ep⟧",
            "caminha até": "⟦ca⟧",
            "o que você": "⟦oqv⟧",
            "eu não sei": "⟦ens⟧",
            "com certeza": "⟦cc⟧",
            "muito bem": "⟦mb⟧",
            "por favor": "⟦pf⟧",
        }

        # ESTRATÉGIA 4: Sequências repetitivas
        self.repetition_patterns = {}

        # Combina todos os padrões
        self.all_patterns = {
            **self.basic_patterns,
            **self.space_patterns,
            **self.phrase_patterns,
        }

        # Dicionário reverso
        self.reverse_patterns = {v: k for k, v in self.all_patterns.items()}

        # Cache
        self.cache = {}

    def compress(self, text: str) -> Tuple[str, float]:
        """
        Comprime texto com estratégias melhoradas.

        Args:
            text: Texto original

        Returns:
            (texto_comprimido, taxa_compressão)
        """
        # Verifica cache
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        if text_hash in self.cache:
            return self.cache[text_hash]

        original_size = len(text)
        compressed = text

        # ESTRATÉGIA 1: Aplica frases completas primeiro (maior → menor)
        for pattern, replacement in sorted(self.phrase_patterns.items(),
                                         key=lambda x: len(x[0]), reverse=True):
            compressed = compressed.replace(pattern, replacement)

        # ESTRATÉGIA 2: Aplica padrões de espaço
        for pattern, replacement in self.space_patterns.items():
            compressed = compressed.replace(pattern, replacement)

        # ESTRATÉGIA 3: Aplica padrões básicos
        for pattern, replacement in self.basic_patterns.items():
            compressed = compressed.replace(pattern, replacement)

        # ESTRATÉGIA 4: Detecta e comprime repetições
        compressed = self._compress_repetitions(compressed)

        # ESTRATÉGIA 5: Remove espaços no fim de linhas (seguro)
        compressed = re.sub(r' +\n', '\n', compressed)

        # ESTRATÉGIA 6: Remove espaços duplos (mas preserva no início de linha)
        compressed = re.sub(r'([^\n])  +', r'\1 ', compressed)

        compressed_size = len(compressed)
        compression_ratio = 1 - (compressed_size / original_size) if original_size > 0 else 0

        # Salva no cache
        result = (compressed, compression_ratio)
        self.cache[text_hash] = result

        return result

    def _compress_repetitions(self, text: str) -> str:
        """
        Detecta e comprime padrões repetitivos.
        Ex: "----------" → "⟦10-⟧"
        """
        # Linhas de separação
        text = re.sub(r'-{10,}', lambda m: f'⟦{len(m.group())}-⟧', text)
        text = re.sub(r'={10,}', lambda m: f'⟦{len(m.group())}=⟧', text)
        text = re.sub(r'\*{10,}', lambda m: f'⟦{len(m.group())}*⟧', text)

        # Pontos repetidos
        text = re.sub(r'\.{4,}', lambda m: f'⟦{len(m.group())}.⟧', text)

        return text

    def decompress(self, compressed_text: str) -> str:
        """
        Descomprime texto.

        Args:
            compressed_text: Texto comprimido

        Returns:
            Texto original
        """
        decompressed = compressed_text

        # Descomprime repetições
        decompressed = re.sub(r'⟦(\d+)([-=*\.])⟧',
                              lambda m: m.group(2) * int(m.group(1)),
                              decompressed)

        # Aplica padrões reversos
        for pattern, replacement in self.reverse_patterns.items():
            decompressed = decompressed.replace(pattern, replacement)

        return decompressed

    def analyze_potential(self, text: str) -> Dict:
        """
        Analisa potencial de compressão de um texto.
        """
        analysis = {
            'original_size': len(text),
            'potential_patterns': 0,
            'space_waste': 0,
            'repetitions': 0,
        }

        # Conta padrões aplicáveis
        for pattern in self.all_patterns.keys():
            count = text.count(pattern)
            if count > 0:
                saved = (len(pattern) - len(self.all_patterns[pattern])) * count
                analysis['potential_patterns'] += saved

        # Conta desperdício de espaços
        analysis['space_waste'] += len(re.findall(r' +\n', text))  # Espaços no fim
        analysis['space_waste'] += len(re.findall(r'([^\n])  +', text))  # Múltiplos espaços

        # Conta repetições
        analysis['repetitions'] += sum(len(m.group()) - 5 for m in re.finditer(r'-{10,}', text))
        analysis['repetitions'] += sum(len(m.group()) - 5 for m in re.finditer(r'={10,}', text))

        analysis['total_potential'] = (analysis['potential_patterns'] +
                                      analysis['space_waste'] +
                                      analysis['repetitions'])
        analysis['potential_ratio'] = analysis['total_potential'] / len(text) if len(text) > 0 else 0

        return analysis


# Função de conveniência
def get_enhanced_compressor():
    """Retorna instância do compressor melhorado."""
    return DigiLangEnhanced()


# Teste rápido
if __name__ == "__main__":
    compressor = get_enhanced_compressor()

    test_text = """FADE IN:

INT. CAFÉ - DAY

JOHN está sentado em uma mesa.

MARY
(entrando)
O que você está fazendo?

JOHN
Eu não sei... talvez esperando.

--------------------

CUT TO:"""

    compressed, ratio = compressor.compress(test_text)
    decompressed = compressor.decompress(compressed)

    print(f"Original: {len(test_text)} chars")
    print(f"Comprimido: {len(compressed)} chars")
    print(f"Compressão: {ratio*100:.1f}%")
    print(f"Reversível: {test_text == decompressed}")

    # Análise
    analysis = compressor.analyze_potential(test_text)
    print(f"\nPotencial de compressão: {analysis['potential_ratio']*100:.1f}%")