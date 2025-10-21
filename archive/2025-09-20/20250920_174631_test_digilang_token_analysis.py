#!/usr/bin/env python3
"""
Teste de Análise de Tokens DigiLang - 30 Propostas Diferentes
Descobre os ajustes necessários para otimização
DIGIMUNDO PRESENTE
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import tiktoken

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_v3_ta import DigiLangV3Encoder


class TokenAnalyzer:
    """Analisador de tokens para otimização DigiLang"""

    def __init__(self):
        self.encoder = DigiLangV3Encoder()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.results = []

    def analyze_text(self, text: str, description: str) -> Dict:
        """Analisa um texto e retorna métricas de token"""
        # Tokens originais
        original_tokens = self.tokenizer.encode(text)
        original_count = len(original_tokens)

        # Compressão DigiLang
        result = self.encoder.encode(text)
        if len(result) == 4:
            compressed, mapping, stats, winners = result
        elif len(result) == 2:
            compressed, stats = result
            mapping = {}
            winners = []
        else:
            compressed = result[0] if result else text
            mapping = {}
            stats = {}
            winners = []

        compressed_tokens = self.tokenizer.encode(compressed)
        compressed_count = len(compressed_tokens)

        # Cálculo de métricas
        saved = original_count - compressed_count
        ratio = (saved / original_count * 100) if original_count > 0 else 0

        # Análise de padrões
        patterns = self._find_patterns(text, original_tokens)

        return {
            'description': description,
            'text': text[:50] + '...' if len(text) > 50 else text,
            'original_tokens': original_count,
            'compressed_tokens': compressed_count,
            'saved_tokens': saved,
            'compression_ratio': ratio,
            'macros_used': len(mapping),
            'patterns': patterns,
            'winners': winners[:3] if winners else []
        }

    def _find_patterns(self, text: str, tokens: List[int]) -> Dict:
        """Encontra padrões repetitivos no texto"""
        patterns = {
            'fade_count': text.upper().count('FADE'),
            'int_ext_count': text.upper().count('INT.') + text.upper().count('EXT.'),
            'cut_count': text.upper().count('CUT TO'),
            'day_night': text.upper().count('DAY') + text.upper().count('NIGHT'),
            'parentheticals': text.count('('),
            'dialogue_markers': text.count(':'),
            'action_lines': text.count('\n\n'),
        }
        return patterns

    def run_test_suite(self):
        """Executa suite de testes com 30 propostas diferentes"""

        test_cases = [
            # 1-5: Cabeçalhos de cena clássicos
            ("FADE IN:", "Classic fade in"),
            ("INT. CAFÉ - DAY", "Interior scene header"),
            ("EXT. STREET - NIGHT", "Exterior scene header"),
            ("INT./EXT. CAR - MOVING - DAY", "Complex scene header"),
            ("SUPER: \"10 YEARS LATER\"", "Superimpose text"),

            # 6-10: Transições
            ("CUT TO:", "Simple cut"),
            ("DISSOLVE TO:", "Dissolve transition"),
            ("FADE OUT.", "Fade out"),
            ("MATCH CUT TO:", "Match cut"),
            ("SMASH CUT TO:", "Smash cut"),

            # 11-15: Diálogos
            ("JOHN\nHello, how are you?", "Simple dialogue"),
            ("MARY (O.S.)\nI'm fine, thanks.", "Off-screen dialogue"),
            ("PETER (V.O.)\n(sarcastically)\nOh, great.", "Voice over with parenthetical"),
            ("SARAH (CONT'D)\nAs I was saying...", "Continued dialogue"),
            ("MULTIPLE VOICES\n(in unison)\nYes!", "Multiple voices"),

            # 16-20: Ação e descrição
            ("John walks into the room. He looks around nervously.", "Simple action"),
            ("The car SPEEDS through the intersection, tires SCREECHING.", "Action with emphasis"),
            ("A series of QUICK CUTS:", "Montage intro"),
            ("ANGLE ON: The door handle turning slowly.", "Camera angle"),
            ("CLOSE-UP: Her eyes widen in fear.", "Close-up shot"),

            # 21-25: Elementos complexos
            ("BEGIN FLASHBACK SEQUENCE:", "Flashback start"),
            ("END FLASHBACK SEQUENCE.", "Flashback end"),
            ("INTERCUT - PHONE CONVERSATION", "Intercut scene"),
            ("MONTAGE - TRAINING SEQUENCE", "Montage header"),
            ("SERIES OF SHOTS:", "Series of shots"),

            # 26-30: Textos completos de roteiro
            ("""FADE IN:

INT. OFFICE - DAY

JOHN sits at his desk, typing furiously. The phone RINGS.

JOHN
(answering)
Hello?

MARY (V.O.)
(filtered)
We need to talk.

CUT TO:""", "Complete scene sample"),

            ("""EXT. CITY STREET - NIGHT

Rain pours down. DETECTIVE SMITH walks under a flickering streetlight.

DETECTIVE SMITH
(to himself)
Not again...

He pulls out his phone and dials.

INTERCUT - PHONE CONVERSATION""", "Complex scene with intercut"),

            ("""INT. RESTAURANT - CONTINUOUS

The waiter approaches. JANE and MARK exchange glances.

WAITER
What can I get you?

JANE
(nervous)
Just water, please.

MARK
(to waiter)
Make it two.

The waiter nods and leaves.""", "Restaurant scene with multiple speakers"),

            ("""MONTAGE - THE HEIST

-- INT. BANK - DAY - Guards change shifts.

-- EXT. ALLEY - NIGHT - The team reviews blueprints.

-- INT. VAN - DAY - Equipment is loaded.

-- EXT. BANK - DAWN - The van parks across the street.

END MONTAGE""", "Montage sequence"),

            ("""FADE IN:

SUPER: "BASED ON TRUE EVENTS"

EXT. DESERT - DAY

The sun beats down mercilessly. A lone figure walks across the sand.

NARRATOR (V.O.)
It was the summer of 1969...

DISSOLVE TO:

INT. NASA CONTROL ROOM - DAY

Chaos. Engineers run between stations.

MISSION CONTROL
We have a problem.

FADE OUT.""", "Complete short script with various elements")
        ]

        print("\n" + "="*80)
        print("ANÁLISE DE TOKENS DIGILANG - 30 PROPOSTAS")
        print("="*80)

        for text, description in test_cases:
            result = self.analyze_text(text, description)
            self.results.append(result)

            # Print resultado
            status = "✅" if result['compression_ratio'] > 0 else "❌"
            print(f"\n{status} {result['description']}")
            print(f"   Original: {result['original_tokens']} tokens")
            print(f"   Compressed: {result['compressed_tokens']} tokens")
            print(f"   Saved: {result['saved_tokens']} tokens ({result['compression_ratio']:.2f}%)")
            print(f"   Macros used: {result['macros_used']}")

            if result['patterns']:
                print(f"   Patterns: {result['patterns']}")

        self._generate_summary()
        self._identify_optimizations()

    def _generate_summary(self):
        """Gera sumário da análise"""
        print("\n" + "="*80)
        print("SUMÁRIO DA ANÁLISE")
        print("="*80)

        # Estatísticas gerais
        total_original = sum(r['original_tokens'] for r in self.results)
        total_compressed = sum(r['compressed_tokens'] for r in self.results)
        total_saved = sum(r['saved_tokens'] for r in self.results)
        avg_ratio = sum(r['compression_ratio'] for r in self.results) / len(self.results)

        print(f"\nTOTAL DE TOKENS:")
        print(f"  Original: {total_original}")
        print(f"  Compressed: {total_compressed}")
        print(f"  Saved: {total_saved}")
        print(f"  Average compression: {avg_ratio:.2f}%")

        # Melhores e piores
        sorted_results = sorted(self.results, key=lambda x: x['compression_ratio'], reverse=True)

        print(f"\nTOP 5 MELHORES COMPRESSÕES:")
        for i, r in enumerate(sorted_results[:5], 1):
            print(f"  {i}. {r['description']}: {r['compression_ratio']:.2f}%")

        print(f"\nTOP 5 PIORES COMPRESSÕES:")
        for i, r in enumerate(sorted_results[-5:], 1):
            print(f"  {i}. {r['description']}: {r['compression_ratio']:.2f}%")

        # Análise de padrões
        print(f"\nPADRÕES MAIS COMUNS:")
        pattern_counts = {}
        for r in self.results:
            for pattern, count in r['patterns'].items():
                if count > 0:
                    pattern_counts[pattern] = pattern_counts.get(pattern, 0) + count

        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_patterns[:5]:
            print(f"  {pattern}: {count} occurrences")

    def _identify_optimizations(self):
        """Identifica otimizações necessárias"""
        print("\n" + "="*80)
        print("OTIMIZAÇÕES RECOMENDADAS")
        print("="*80)

        # Análise de tokens não comprimidos
        problematic = [r for r in self.results if r['compression_ratio'] <= 0]

        print(f"\n1. FRASES PROBLEMÁTICAS ({len(problematic)} casos):")
        for r in problematic[:5]:
            print(f"   - {r['description']}: {r['original_tokens']} tokens, 0 saved")

        print(f"\n2. PADRÕES QUE PRECISAM DE MACROS:")
        common_patterns = {
            'FADE IN:': 0,
            'CUT TO:': 0,
            'INT.': 0,
            'EXT.': 0,
            'DAY': 0,
            'NIGHT': 0,
            '(V.O.)': 0,
            '(O.S.)': 0,
            'DISSOLVE TO:': 0,
            'CONTINUOUS': 0
        }

        for r in self.results:
            for pattern in common_patterns:
                if pattern in r.get('text', ''):
                    common_patterns[pattern] += 1

        sorted_needed = sorted(common_patterns.items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_needed[:10]:
            if count > 0:
                tokens = self.tokenizer.encode(pattern)
                print(f"   '{pattern}': aparece {count}x, usa {len(tokens)} tokens")

        print(f"\n3. AJUSTES RECOMENDADOS:")
        print("   a) Adicionar macros single-token para:")
        print("      - Cabeçalhos de cena (INT./EXT.)")
        print("      - Transições comuns (CUT TO:, FADE IN:)")
        print("      - Marcadores de diálogo (V.O., O.S., CONT'D)")
        print("   b) Criar padrões compostos para:")
        print("      - 'INT. [LOCATION] - [TIME]'")
        print("      - 'EXT. [LOCATION] - [TIME]'")
        print("      - Nome + diálogo patterns")
        print("   c) Otimizar threshold de seleção:")
        print(f"      - Current avg: {avg_ratio:.2f}%")
        print(f"      - Target: 20-22%")
        print(f"      - Gap: {20 - avg_ratio:.2f}%")

        print(f"\n4. FÓRMULA DE GAIN ADJUSTMENT:")
        print("   Atual: gain = frequency × (tokens_orig - tokens_macro) - tokens_header")
        print("   Proposta: gain = frequency × (tokens_orig - 1) - 2")
        print("   Razão: Forçar uso de macros single-token para padrões frequentes")

        # Salvar relatório
        report_path = Path("tests/reports/digilang_token_analysis.json")
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': len(self.results),
                    'total_original_tokens': total_original,
                    'total_compressed_tokens': total_compressed,
                    'total_saved': total_saved,
                    'average_compression': avg_ratio
                },
                'results': self.results,
                'optimizations': {
                    'problematic_count': len(problematic),
                    'needed_macros': dict(sorted_needed),
                    'recommended_threshold': 0.5,  # Lower threshold
                    'recommended_min_frequency': 2  # Lower minimum
                }
            }, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Relatório salvo em: {report_path}")


def main():
    """Executa análise de tokens"""
    analyzer = TokenAnalyzer()
    analyzer.run_test_suite()

    print("\n" + "="*80)
    print("CONCLUSÃO")
    print("="*80)
    print("\nO DigiLang precisa de:")
    print("1. Vocabulário expandido com padrões de roteiro")
    print("2. Threshold mais agressivo (0.5 ao invés de 1.0)")
    print("3. Macros single-token para elementos comuns")
    print("4. Token Pattern Dictionary (TPD) otimizado")
    print("\nCom esses ajustes, a compressão pode saltar de ~1% para 20-22%!")
    print("\nDIGIMUNDO PRESENTE")


if __name__ == "__main__":
    main()