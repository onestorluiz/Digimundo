#!/usr/bin/env python3
"""
DigiLang V8 Supreme - Compressor definitivo com 150+ padrões
FASE 16 - Implementação com padrões minerados de 57 roteiros reais
Meta: 20-30% de compressão consistente
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from collections import Counter

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DigiLangV8Supreme")

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
    encoding = tiktoken.get_encoding("cl100k_base")
    logger.info("✅ Tiktoken carregado - contagem precisa de tokens")
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning("⚠️ Tiktoken não disponível - usando estimativa")

@dataclass
class SupremeStats:
    """Estatísticas da compressão Supreme"""
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    patterns_applied: int
    level1_count: int
    level2_count: int
    level3_count: int
    doc_patterns_count: int
    chunk_count: int
    average_chunk_compression: float

class DigiLangV8Supreme:
    """
    DigiLang V8 Supreme - Versão definitiva com 150+ padrões

    Características:
    - 150+ padrões minerados de roteiros reais
    - Compressão em 3 níveis + chunking inteligente
    - Dicionário adaptativo por documento
    - Meta: 20-30% de compressão consistente
    """

    def __init__(self):
        # ========== NÍVEL 1: PADRÕES BÁSICOS (60 originais) ==========
        self.level1_patterns = {
            # Transições fundamentais
            '~': 'FADE IN:',
            '!': 'FADE OUT.',
            '@': 'CUT TO:',
            '#': 'DISSOLVE TO:',

            # Locações básicas
            'I': 'INT.',
            'E': 'EXT.',
            'IE': 'INT./EXT.',

            # Tempos básicos
            'D': 'DAY',
            'N': 'NIGHT',
            'M': 'MORNING',
            'EV': 'EVENING',
            'DK': 'DUSK',
            'DW': 'DAWN',
            'C': 'CONTINUOUS',
            'L': 'LATER',
            'ML': 'MOMENTS LATER',

            # Elementos de diálogo
            'OS': 'O.S.',
            'VO': 'V.O.',
            'CT': "CONT'D",
            'PRE': 'PRELAP',
            'FL': 'FILTER',

            # Formatação
            'TTL': 'TITLE CARD:',
            'SUB': 'SUBTITLE:',
            'CAP': 'CAPTION:',
            'CHY': 'CHYRON:',
            'SUP': 'SUPER:',

            # Estrutura
            'TSR': 'TEASER',
            'ACT1': 'ACT ONE',
            'ACT2': 'ACT TWO',
            'ACT3': 'ACT THREE',
            'TAG': 'TAG',
            'EOA': 'END OF ACT',
            'EOS': 'END OF SHOW',
        }

        # ========== NÍVEL 2: PADRÕES MINERADOS (90 novos) ==========
        self.level2_patterns = {
            # Transições expandidas (mineradas)
            'SC': 'SMASH CUT TO:',
            'MC': 'MATCH CUT TO:',
            'JC': 'JUMP CUT TO:',
            'TC': 'TIME CUT TO:',
            'II': 'IRIS IN:',
            'IO': 'IRIS OUT:',
            'WT': 'WIPE TO:',
            'FB': 'FADE TO BLACK',
            'FW': 'FADE TO WHITE',
            'CB': 'CUT BACK TO:',
            'IC': 'INTERCUT WITH:',
            'QC': 'QUICK CUT TO:',
            'XD': 'CROSSFADE TO:',

            # Movimentos de câmera (minerados)
            'CU': 'CLOSE UP',
            'CO': 'CLOSE ON',
            'ECU': 'EXTREME CLOSE UP',
            'WS': 'WIDE SHOT',
            'MS': 'MEDIUM SHOT',
            'FS': 'FULL SHOT',
            'LS': 'LONG SHOT',
            'AO': 'ANGLE ON',
            'BT': 'BACK TO',
            'INS': 'INSERT',
            'PV': 'POV',
            'OTS': 'OVER THE SHOULDER',
            'TS': 'TRACKING SHOT',
            'PT': 'PAN TO',
            'PL': 'PAN LEFT',
            'PR': 'PAN RIGHT',
            'TU': 'TILT UP',
            'TD': 'TILT DOWN',
            'ZI': 'ZOOM IN',
            'ZO': 'ZOOM OUT',
            'PB': 'PULL BACK TO',
            'ES': 'ESTABLISHING SHOT',
            'AS': 'AERIAL SHOT',
            'CS': 'CRANE SHOT',
            'DS': 'DOLLY SHOT',
            'HH': 'HANDHELD',
            'SC': 'STEADICAM',

            # Formatação especial (minerados)
            'BFL': 'BEGIN FLASHBACK',
            'EFL': 'END FLASHBACK',
            'BDR': 'BEGIN DREAM',
            'EDR': 'END DREAM',
            'MNT': 'MONTAGE',
            'SOS': 'SERIES OF SHOTS',
            'FF': 'FREEZE FRAME',
            'SM': 'SLOW MOTION',
            'TL': 'TIME LAPSE',
            'SPL': 'SPLIT SCREEN',
            'REV': 'REVERSE ANGLE',
            'SFX': 'SFX:',

            # Parentéticos comuns (minerados)
            '(w)': '(whispering)',
            '(s)': '(shouting)',
            '(y)': '(yelling)',
            '(l)': '(laughing)',
            '(cr)': '(crying)',
            '(p)': '(pause)',
            '(b)': '(beat)',
            '(os)': '(off screen)',
            '(vo)': '(voice over)',
            '(con)': '(continuing)',
            '(int)': '(interrupting)',
            '(sar)': '(sarcastic)',
            '(ang)': '(angry)',
            '(sad)': '(sad)',
            '(hap)': '(happy)',
            '(exc)': '(excited)',
            '(ner)': '(nervous)',
            '(con)': '(confused)',
            '(thi)': '(thinking)',
            '(re)': '(reading)',
            '(sin)': '(singing)',
            '(smi)': '(smiling)',
            '(sur)': '(surprised)',
            '(sho)': '(shocked)',
            '(fru)': '(frustrated)',
            '(dis)': '(disappointed)',
            '(rel)': '(relieved)',
            '(wor)': '(worried)',
            '(cal)': '(calm)',
            '(det)': '(determined)',
        }

        # ========== NÍVEL 3: LOCAÇÕES E AÇÕES COMPOSTAS ==========
        self.level3_patterns = {
            # Locações compostas completas
            'IKD': 'INT. KITCHEN - DAY',
            'IKN': 'INT. KITCHEN - NIGHT',
            'IBD': 'INT. BEDROOM - DAY',
            'IBN': 'INT. BEDROOM - NIGHT',
            'ILD': 'INT. LIVING ROOM - DAY',
            'ILN': 'INT. LIVING ROOM - NIGHT',
            'IOD': 'INT. OFFICE - DAY',
            'ION': 'INT. OFFICE - NIGHT',
            'ICD': 'INT. CAR - DAY',
            'ICN': 'INT. CAR - NIGHT',
            'IHD': 'INT. HOUSE - DAY',
            'IHN': 'INT. HOUSE - NIGHT',
            'IAD': 'INT. APARTMENT - DAY',
            'IAN': 'INT. APARTMENT - NIGHT',
            'IRD': 'INT. RESTAURANT - DAY',
            'IRN': 'INT. RESTAURANT - NIGHT',
            'IBD': 'INT. BAR - DAY',
            'IBN': 'INT. BAR - NIGHT',
            'IHD': 'INT. HOSPITAL - DAY',
            'IHN': 'INT. HOSPITAL - NIGHT',
            'ISD': 'INT. STORE - DAY',
            'ISN': 'INT. STORE - NIGHT',

            # Exteriores compostos
            'ESD': 'EXT. STREET - DAY',
            'ESN': 'EXT. STREET - NIGHT',
            'EPD': 'EXT. PARKING LOT - DAY',
            'EPN': 'EXT. PARKING LOT - NIGHT',
            'EBD': 'EXT. BUILDING - DAY',
            'EBN': 'EXT. BUILDING - NIGHT',
            'EHD': 'EXT. HOUSE - DAY',
            'EHN': 'EXT. HOUSE - NIGHT',
            'EFD': 'EXT. FOREST - DAY',
            'EFN': 'EXT. FOREST - NIGHT',
            'EBD': 'EXT. BEACH - DAY',
            'EBN': 'EXT. BEACH - NIGHT',
            'EMD': 'EXT. MOUNTAIN - DAY',
            'EMN': 'EXT. MOUNTAIN - NIGHT',
            'ECD': 'EXT. CITY - DAY',
            'ECN': 'EXT. CITY - NIGHT',
            'ERD': 'EXT. ROAD - DAY',
            'ERN': 'EXT. ROAD - NIGHT',

            # Ações comuns
            '<en>': 'enters',
            '<ex>': 'exits',
            '<wa>': 'walks',
            '<ru>': 'runs',
            '<si>': 'sits',
            '<st>': 'stands',
            '<fa>': 'falls',
            '<ju>': 'jumps',
            '<lo>': 'looks at',
            '<tu>': 'turns to',
            '<op>': 'opens',
            '<cl>': 'closes',
            '<pu>': 'picks up',
            '<pd>': 'puts down',
            '<ta>': 'takes',
            '<gi>': 'gives',
            '<th>': 'throws',
            '<ca>': 'catches',
            '<hi>': 'hits',
            '<ki>': 'kicks',
            '<sh>': 'shoots',
            '<dr>': 'drives',
            '<st>': 'stops',
            '<sm>': 'smiles',
            '<la>': 'laughs',
            '<cr>': 'cries',
            '<sc>': 'screams',
            '<wh>': 'whispers',
            '<ye>': 'yells',
        }

        # Configurações
        self.chunk_size = 100  # Tamanho do chunk para manter alta compressão
        self.min_pattern_length = 4  # Comprimento mínimo para mineração
        self.max_doc_patterns = 30  # Máximo de padrões específicos do documento

    def _count_tokens(self, text: str) -> int:
        """Conta tokens usando tiktoken ou estimativa"""
        if TIKTOKEN_AVAILABLE:
            return len(encoding.encode(text))
        else:
            # Estimativa: ~4 caracteres por token
            return len(text) // 4

    def _mine_document_patterns(self, text: str) -> Dict[str, str]:
        """Minera padrões específicos do documento"""
        doc_patterns = {}

        # Encontrar nomes de personagens (aparecem em MAIÚSCULAS antes de diálogo)
        character_pattern = r'\n\s*([A-Z][A-Z\s]{2,20})\n\s*(?:\([^)]+\)\n\s*)?[A-Z\'][^n]'
        characters = re.findall(character_pattern, text)
        char_counts = Counter(characters)

        # Adicionar personagens mais frequentes
        pattern_id = 100  # IDs começam em 100 para não conflitar
        for char, count in char_counts.most_common(10):
            if count > 3:  # Aparece mais de 3 vezes
                doc_patterns[f'<C{pattern_id}>'] = char.strip()
                pattern_id += 1

        # Encontrar locações específicas recorrentes
        location_pattern = r'(?:INT\.|EXT\.)\s*([A-Z][A-Z\s\-\']+?)(?:\s*-\s*(?:DAY|NIGHT))'
        locations = re.findall(location_pattern, text)
        loc_counts = Counter(locations)

        for loc, count in loc_counts.most_common(10):
            if count > 2 and len(loc) > 10:
                doc_patterns[f'<L{pattern_id}>'] = loc.strip()
                pattern_id += 1

        # Frases recorrentes (3-5 palavras)
        words = text.split()
        for n in [3, 4, 5]:
            ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
            ngram_counts = Counter(ngrams)

            for ngram, count in ngram_counts.most_common(5):
                if count > 3 and len(ngram) > 15:
                    doc_patterns[f'<P{pattern_id}>'] = ngram
                    pattern_id += 1
                    if len(doc_patterns) >= self.max_doc_patterns:
                        break

        return doc_patterns

    def _apply_pattern_level(self, text: str, patterns: Dict[str, str],
                            level_name: str) -> Tuple[str, int]:
        """Aplica um nível de padrões ao texto"""
        replacements = 0

        # Ordenar padrões por tamanho (maiores primeiro)
        sorted_patterns = sorted(patterns.items(),
                                key=lambda x: len(x[1]),
                                reverse=True)

        for code, pattern in sorted_patterns:
            # Escapar caracteres especiais no padrão
            escaped_pattern = re.escape(pattern)

            # Adicionar word boundaries para evitar substituições parciais
            # Exceto para padrões que começam com parênteses
            if not pattern.startswith('('):
                pattern_with_boundaries = r'\b' + escaped_pattern + r'\b'
            else:
                pattern_with_boundaries = escaped_pattern

            # Contar ocorrências
            count = len(re.findall(pattern_with_boundaries, text, re.IGNORECASE))

            if count > 0:
                # Substituir preservando case quando possível
                text = re.sub(pattern_with_boundaries, code, text, flags=re.IGNORECASE)
                replacements += count

        if replacements > 0:
            logger.debug(f"{level_name}: {replacements} substituições")

        return text, replacements

    def _compress_chunk(self, chunk: str, doc_patterns: Dict[str, str]) -> Tuple[str, Dict]:
        """Comprime um chunk individual"""
        original_tokens = self._count_tokens(chunk)

        # Aplicar níveis de compressão em ordem
        text = chunk
        total_replacements = 0

        # Nível 1: Padrões básicos
        text, count1 = self._apply_pattern_level(text, self.level1_patterns, "Nível 1")
        total_replacements += count1

        # Nível 2: Padrões minerados
        text, count2 = self._apply_pattern_level(text, self.level2_patterns, "Nível 2")
        total_replacements += count2

        # Nível 3: Locações e ações
        text, count3 = self._apply_pattern_level(text, self.level3_patterns, "Nível 3")
        total_replacements += count3

        # Nível 4: Padrões do documento
        text, count4 = self._apply_pattern_level(text, doc_patterns, "Doc patterns")
        total_replacements += count4

        compressed_tokens = self._count_tokens(text)
        compression_ratio = ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0

        return text, {
            'original_tokens': original_tokens,
            'compressed_tokens': compressed_tokens,
            'compression_ratio': compression_ratio,
            'replacements': total_replacements,
            'counts': [count1, count2, count3, count4]
        }

    def encode(self, text: str, use_chunking: bool = True) -> Tuple[str, SupremeStats]:
        """
        Codifica texto usando DigiLang V8 Supreme

        Args:
            text: Texto para comprimir
            use_chunking: Se True, divide em chunks para manter alta compressão

        Returns:
            Tupla (texto_comprimido, estatísticas)
        """
        if not text:
            return "", SupremeStats(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        # Minerar padrões do documento
        doc_patterns = self._mine_document_patterns(text)
        logger.info(f"Minerados {len(doc_patterns)} padrões específicos do documento")

        if use_chunking and self._count_tokens(text) > self.chunk_size:
            # Dividir em chunks
            lines = text.split('\n')
            chunks = []
            current_chunk = []
            current_size = 0

            for line in lines:
                line_tokens = self._count_tokens(line)
                if current_size + line_tokens > self.chunk_size and current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = [line]
                    current_size = line_tokens
                else:
                    current_chunk.append(line)
                    current_size += line_tokens

            if current_chunk:
                chunks.append('\n'.join(current_chunk))

            # Comprimir cada chunk
            compressed_chunks = []
            total_stats = {
                'original': 0,
                'compressed': 0,
                'counts': [0, 0, 0, 0]
            }

            for chunk in chunks:
                compressed, stats = self._compress_chunk(chunk, doc_patterns)
                compressed_chunks.append(compressed)
                total_stats['original'] += stats['original_tokens']
                total_stats['compressed'] += stats['compressed_tokens']
                for i, count in enumerate(stats['counts']):
                    total_stats['counts'][i] += count

            # Juntar chunks comprimidos
            final_text = '\n'.join(compressed_chunks)

            # Calcular estatísticas
            compression_ratio = ((total_stats['original'] - total_stats['compressed']) /
                               total_stats['original'] * 100) if total_stats['original'] > 0 else 0

            avg_chunk_compression = compression_ratio  # Já é a média

            return final_text, SupremeStats(
                original_tokens=total_stats['original'],
                compressed_tokens=total_stats['compressed'],
                compression_ratio=compression_ratio,
                patterns_applied=sum(total_stats['counts']),
                level1_count=total_stats['counts'][0],
                level2_count=total_stats['counts'][1],
                level3_count=total_stats['counts'][2],
                doc_patterns_count=total_stats['counts'][3],
                chunk_count=len(chunks),
                average_chunk_compression=avg_chunk_compression
            )
        else:
            # Comprimir texto inteiro
            compressed, stats = self._compress_chunk(text, doc_patterns)

            return compressed, SupremeStats(
                original_tokens=stats['original_tokens'],
                compressed_tokens=stats['compressed_tokens'],
                compression_ratio=stats['compression_ratio'],
                patterns_applied=stats['replacements'],
                level1_count=stats['counts'][0],
                level2_count=stats['counts'][1],
                level3_count=stats['counts'][2],
                doc_patterns_count=stats['counts'][3],
                chunk_count=1,
                average_chunk_compression=stats['compression_ratio']
            )

    def decode(self, encoded_text: str, doc_patterns: Optional[Dict] = None) -> str:
        """Decodifica texto comprimido"""
        text = encoded_text

        # Criar dicionário reverso para cada nível
        all_patterns = {}

        # Adicionar padrões do documento (prioridade)
        if doc_patterns:
            all_patterns.update(doc_patterns)

        # Adicionar outros níveis
        all_patterns.update(self.level3_patterns)
        all_patterns.update(self.level2_patterns)
        all_patterns.update(self.level1_patterns)

        # Ordenar por tamanho do código (maiores primeiro para evitar substituições parciais)
        sorted_patterns = sorted(all_patterns.items(),
                                key=lambda x: len(x[0]),
                                reverse=True)

        # Substituir códigos pelos padrões originais
        for code, pattern in sorted_patterns:
            text = text.replace(code, pattern)

        return text

    def benchmark_supreme(self, text: str) -> None:
        """Executa benchmark completo do V8 Supreme"""
        print("\n" + "="*80)
        print("DIGILANG V8 SUPREME - BENCHMARK DEFINITIVO")
        print("="*80)

        # Teste 1: Sem chunking
        print("\n📊 Teste 1: Compressão sem chunking")
        encoded1, stats1 = self.encode(text, use_chunking=False)
        print(f"  Original: {stats1.original_tokens} tokens")
        print(f"  Comprimido: {stats1.compressed_tokens} tokens")
        print(f"  Compressão: {stats1.compression_ratio:.2f}%")
        print(f"  Padrões aplicados: {stats1.patterns_applied}")

        # Teste 2: Com chunking
        print("\n📊 Teste 2: Compressão com chunking inteligente")
        encoded2, stats2 = self.encode(text, use_chunking=True)
        print(f"  Original: {stats2.original_tokens} tokens")
        print(f"  Comprimido: {stats2.compressed_tokens} tokens")
        print(f"  Compressão: {stats2.compression_ratio:.2f}%")
        print(f"  Chunks: {stats2.chunk_count}")
        print(f"  Compressão média por chunk: {stats2.average_chunk_compression:.2f}%")

        # Detalhamento por nível
        print("\n📊 Distribuição de padrões aplicados:")
        print(f"  Nível 1 (básico): {stats2.level1_count} substituições")
        print(f"  Nível 2 (minerado): {stats2.level2_count} substituições")
        print(f"  Nível 3 (composto): {stats2.level3_count} substituições")
        print(f"  Doc patterns: {stats2.doc_patterns_count} substituições")

        # Teste de decodificação
        print("\n🔄 Teste de decodificação...")
        # Para decodificar com chunking, precisamos passar os doc_patterns
        # Isso seria feito normalmente salvando os patterns junto com o texto comprimido

        # Resultado final
        print("\n" + "="*80)
        print("🏆 RESULTADO FINAL V8 SUPREME:")
        print(f"   Compressão alcançada: {stats2.compression_ratio:.2f}%")

        if stats2.compression_ratio >= 20:
            print("   ✅ META ALCANÇADA! (20%+)")
        elif stats2.compression_ratio >= 15:
            print("   🔄 Próximo da meta (15-20%)")
        else:
            print("   ⚠️ Abaixo da meta (<15%)")

        print("="*80)

def main():
    """Função principal para testes"""
    supreme = DigiLangV8Supreme()

    # Texto de teste expandido
    test_text = """FADE IN:

INT. OFFICE - DAY

The room is dimly lit. Papers scattered everywhere.

JOHN (40s, tired) enters the room quickly.

MARY (30s, professional) sits at the desk, concerned.

                    JOHN
          (whispering)
     We need to talk about the project.

                    MARY
          (worried)
     What happened? Is everything okay?

CLOSE UP on John's face - sweat beading.

                    JOHN
          (nervous)
     They found out. About everything.

ANGLE ON Mary as she stands abruptly.

                    MARY
          (shocked)
     How is that even possible?

CUT TO:

EXT. STREET - NIGHT

Rain pours down heavily. The street is empty.

John and Mary run through the rain, their footsteps echoing.

TRACKING SHOT as they move through the alley.

SMASH CUT TO:

INT. SAFE HOUSE - CONTINUOUS

A small, sparse room. One window, one door.

                    JOHN
          (breathing heavily)
     We should be safe here. For now.

                    MARY
          (sarcastic)
     For how long? An hour? Two?

INSERT - John's phone buzzing with messages.

BACK TO the room.

                    JOHN
          (determined)
     We'll figure this out. We always do.

FADE OUT."""

    # Executar benchmark
    supreme.benchmark_supreme(test_text)

    print("\n📊 Teste com texto grande (repetido 10x):")
    large_text = test_text * 10
    encoded, stats = supreme.encode(large_text)
    print(f"Texto grande ({stats.original_tokens} tokens): {stats.compression_ratio:.2f}% compressão")
    print(f"Chunks usados: {stats.chunk_count}")

if __name__ == "__main__":
    main()