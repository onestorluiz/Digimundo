#!/usr/bin/env python3
"""
DigiLang V4 Optimized - Sistema de Compressão Token-Aware com Mineração Avançada
Baseado na análise de 8 roteiros com padrões globais e doc-específicos
DIGIMUNDO PRESENTE
"""

import json
import re
from typing import Dict, List, Tuple, Set, Optional
from pathlib import Path
from collections import Counter
import tiktoken


class DigiLangV4Optimizer:
    """
    Encoder/Decoder otimizado com mineração avançada de padrões
    Implementa descobertas da análise de corpus de roteiros
    """

    def __init__(self, use_tiktoken: bool = True, min_freq: int = 5, max_macros: int = 50):
        """
        Inicializa o encoder com parâmetros otimizados

        Args:
            use_tiktoken: Usar tokenizador real (cl100k_base)
            min_freq: Frequência mínima para inclusão de macro
            max_macros: Número máximo de macros por documento
        """
        self.use_tiktoken = use_tiktoken and self._try_load_tiktoken()
        self.min_freq = min_freq
        self.max_macros = max_macros

        # Tokenizer
        if self.use_tiktoken:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        else:
            self.tokenizer = None

        # Macros globais de roteiro (baseline confirmado)
        self.global_macros = {
            'I': 'INT.',
            'E': 'EXT.',
            'VO': 'V.O.',
            'CT': 'CUT TO:',
            'OS': 'O.S.',
            'BT': 'BACK TO:',
            'DT': 'DISSOLVE TO:',
            'FI': 'FADE IN:',
            'FO': 'FADE OUT.',
            'ONS': 'ON SCREEN',
            'LA': 'looks at',
            'TT': 'turns to',
            'MCT': 'MATCH CUT TO:',
            'SCT': 'SMASH CUT TO:',
            'CONT': "CONT'D",
            'INT_EXT': 'INT./EXT.',
            'SUPER': 'SUPER:',
            'ANGLE': 'ANGLE ON:',
            'CLOSE': 'CLOSE-UP:',
            'POV': 'P.O.V.',
            'INSERT': 'INSERT:',
            'MONTAGE': 'MONTAGE:',
            'FLASHBACK': 'FLASHBACK:',
            'INTERCUT': 'INTERCUT:',
            'CONTINUOUS': 'CONTINUOUS',
            'LATER': 'LATER',
            'MOMENTS': 'MOMENTS LATER',
            'SAME': 'SAME',
            'DAY': 'DAY',
            'NIGHT': 'NIGHT',
            'MORNING': 'MORNING',
            'AFTERNOON': 'AFTERNOON',
            'EVENING': 'EVENING',
            'DAWN': 'DAWN',
            'DUSK': 'DUSK'
        }

        # Macros PT-BR adicionais
        self.pt_macros = {
            'ES': 'está sentado',
            'ESA': 'está sentada',
            'OP': 'olha para',
            'SS': 'sussurrando',
            'FOQ': 'FORA DE QUADRO',
            'EMO': 'EM OFF',
            'NAR': 'NARRAÇÃO',
            'CORTA': 'CORTA PARA:',
            'FUSÃO': 'FUSÃO PARA:',
            'CONT_PT': 'CONTINUA',
            'MAIS_TARDE': 'MAIS TARDE',
            'MESMA': 'MESMA',
            'DIA': 'DIA',
            'NOITE': 'NOITE',
            'MANHÃ': 'MANHÃ',
            'TARDE': 'TARDE'
        }

        # Combinar macros
        self.all_global_macros = {**self.global_macros, **self.pt_macros}

        # Cache para macros doc-específicas
        self.doc_macros_cache = {}

        # Estatísticas
        self.stats = {
            'total_processed': 0,
            'total_saved': 0,
            'best_compression': 0.0
        }

    def _try_load_tiktoken(self) -> bool:
        """Tenta carregar tiktoken"""
        try:
            import tiktoken
            return True
        except ImportError:
            return False

    def _count_tokens(self, text: str) -> int:
        """Conta tokens usando tiktoken ou fallback"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Fallback: aproximação por palavras
            return len(re.findall(r'\b\w+\b|\S', text))

    def mine_document_macros(self, text: str) -> Dict[str, str]:
        """
        Minera macros específicas do documento (frases MAIÚSCULAS multi-palavra)

        Args:
            text: Texto do documento

        Returns:
            Dict de placeholder -> expansão para macros doc-específicas
        """
        # Encontrar frases em MAIÚSCULAS (2+ palavras)
        uppercase_pattern = r'\b[A-Z][A-Z\s\'\-\.]+[A-Z]\b'
        matches = re.findall(uppercase_pattern, text)

        # Contar frequências
        phrase_counts = Counter(matches)

        # Filtrar por frequência mínima e múltiplas palavras
        candidates = []
        for phrase, freq in phrase_counts.items():
            if freq >= self.min_freq and len(phrase.split()) >= 2:
                # Calcular ganho
                orig_tokens = self._count_tokens(phrase)

                # Gerar placeholder único (primeiras letras)
                words = phrase.split()
                if len(words) == 2:
                    placeholder = words[0][0] + words[1][0]
                else:
                    placeholder = ''.join(w[0] for w in words[:3])

                # Garantir placeholder único
                base_placeholder = placeholder
                suffix = 1
                while placeholder in self.all_global_macros or any(
                    placeholder in doc_macros for doc_macros in self.doc_macros_cache.values()
                ):
                    placeholder = f"{base_placeholder}{suffix}"
                    suffix += 1

                macro_tokens = 1  # Placeholder ASCII sempre 1 token
                gain = freq * (orig_tokens - macro_tokens) - 2  # -2 para header cost

                if gain > 0:
                    candidates.append((gain, placeholder, phrase, freq))

        # Ordenar por ganho e pegar top N
        candidates.sort(reverse=True)
        doc_macros = {}

        for gain, placeholder, phrase, freq in candidates[:self.max_macros]:
            doc_macros[placeholder] = phrase

        return doc_macros

    def encode(self, text: str, doc_id: Optional[str] = None) -> Tuple[str, Dict[str, str], Dict[str, any]]:
        """
        Codifica texto com seleção token-aware de macros

        Args:
            text: Texto para codificar
            doc_id: ID do documento para cache de macros

        Returns:
            Tuple de (texto_codificado, mapping, stats)
        """
        # Minerar ou recuperar macros doc-específicas
        if doc_id and doc_id in self.doc_macros_cache:
            doc_macros = self.doc_macros_cache[doc_id]
        else:
            doc_macros = self.mine_document_macros(text)
            if doc_id:
                self.doc_macros_cache[doc_id] = doc_macros

        # Combinar macros globais e doc-específicas
        all_macros = {**self.all_global_macros, **doc_macros}

        # Calcular frequências e ganhos
        macro_usage = {}
        for placeholder, expansion in all_macros.items():
            count = text.count(expansion)
            if count > 0:
                orig_tokens = self._count_tokens(expansion)
                macro_tokens = 1
                gain = count * (orig_tokens - macro_tokens)
                if gain > 0:
                    macro_usage[placeholder] = {
                        'expansion': expansion,
                        'count': count,
                        'gain': gain
                    }

        # Ordenar por ganho e selecionar macros benéficas
        sorted_macros = sorted(macro_usage.items(), key=lambda x: x[1]['gain'], reverse=True)

        # Calcular custo do header
        header_lines = len(sorted_macros)
        header_tokens = header_lines * 3  # Aproximado: "X=expansion\n" ~3 tokens

        # Selecionar macros com ganho líquido positivo
        selected_macros = {}
        total_gain = 0

        for placeholder, info in sorted_macros:
            if total_gain + info['gain'] - header_tokens > total_gain:
                selected_macros[placeholder] = info['expansion']
                total_gain += info['gain']
            else:
                break  # Parar quando não houver mais ganho líquido

        # Aplicar substituições (ordem: mais longo primeiro para evitar conflitos)
        encoded = text
        replacements = sorted(selected_macros.items(), key=lambda x: len(x[1]), reverse=True)

        for placeholder, expansion in replacements:
            # Usar word boundaries para evitar substituições parciais
            pattern = re.escape(expansion)
            # Use single character placeholders with § prefix (1 token)
            encoded = re.sub(r'\b' + pattern + r'\b', f'§{placeholder}', encoded)

        # Gerar header se houver macros
        if selected_macros:
            header = "MACROS_BEGIN\n"
            for placeholder, expansion in selected_macros.items():
                header += f"{placeholder}={expansion}\n"
            header += "MACROS_END\n"
            final_encoded = header + encoded
        else:
            final_encoded = encoded

        # Calcular estatísticas
        original_tokens = self._count_tokens(text)
        encoded_tokens = self._count_tokens(final_encoded)
        saved_tokens = original_tokens - encoded_tokens
        compression_ratio = saved_tokens / original_tokens if original_tokens > 0 else 0

        stats = {
            'original_tokens': original_tokens,
            'encoded_tokens': encoded_tokens,
            'saved_tokens': saved_tokens,
            'compression_ratio': compression_ratio,
            'macros_used': len(selected_macros),
            'total_gain': total_gain,
            'header_cost': header_tokens if selected_macros else 0,
            'net_gain': total_gain - (header_tokens if selected_macros else 0)
        }

        # Atualizar estatísticas globais
        self.stats['total_processed'] += 1
        self.stats['total_saved'] += saved_tokens
        if compression_ratio > self.stats['best_compression']:
            self.stats['best_compression'] = compression_ratio

        return final_encoded, selected_macros, stats

    def decode(self, encoded_text: str) -> str:
        """
        Decodifica texto codificado

        Args:
            encoded_text: Texto com macros

        Returns:
            Texto original expandido
        """
        # Extrair header se presente
        if encoded_text.startswith("MACROS_BEGIN"):
            header_end = encoded_text.find("MACROS_END\n")
            if header_end != -1:
                header = encoded_text[len("MACROS_BEGIN\n"):header_end]
                body = encoded_text[header_end + len("MACROS_END\n"):]

                # Parse macros do header
                macros = {}
                for line in header.strip().split('\n'):
                    if '=' in line:
                        placeholder, expansion = line.split('=', 1)
                        macros[placeholder] = expansion

                # Expandir macros no corpo
                decoded = body
                for placeholder, expansion in macros.items():
                    decoded = decoded.replace(f'§{placeholder}', expansion)

                return decoded
            else:
                return encoded_text
        else:
            return encoded_text

    def analyze_compression_potential(self, text: str, doc_id: Optional[str] = None) -> Dict:
        """
        Analisa potencial de compressão de um texto

        Args:
            text: Texto para analisar
            doc_id: ID do documento

        Returns:
            Dict com análise detalhada
        """
        # Codificar
        encoded, macros, stats = self.encode(text, doc_id)

        # Análise de padrões
        patterns = {
            'scene_headers': len(re.findall(r'\b(INT\.|EXT\.|INT\./EXT\.)', text)),
            'transitions': len(re.findall(r'(CUT TO:|DISSOLVE TO:|FADE IN:|FADE OUT)', text)),
            'dialogue_markers': len(re.findall(r'\(V\.O\.\)|\(O\.S\.\)|\(CONT\'D\)', text)),
            'uppercase_phrases': len(re.findall(r'\b[A-Z][A-Z\s\'\-\.]+[A-Z]\b', text)),
            'action_patterns': len(re.findall(r'(looks at|turns to|walks|runs|stands)', text, re.I))
        }

        # Recomendações
        recommendations = []

        if stats['compression_ratio'] < 0.1:  # Menos de 10%
            recommendations.append("Consider lowering min_freq threshold")
            recommendations.append("Add more domain-specific macros")

        if patterns['uppercase_phrases'] > 50:
            recommendations.append("High potential for doc-specific macro mining")

        if patterns['scene_headers'] > 20:
            recommendations.append("Good candidate for schema compression")

        return {
            'stats': stats,
            'patterns': patterns,
            'macros_found': len(macros),
            'top_macros': list(macros.items())[:10],
            'recommendations': recommendations,
            'potential_additional_gain': self._estimate_additional_gain(text, patterns)
        }

    def _estimate_additional_gain(self, text: str, patterns: Dict) -> Dict:
        """
        Estima ganho adicional possível com otimizações

        Args:
            text: Texto original
            patterns: Padrões encontrados

        Returns:
            Dict com estimativas
        """
        estimates = {}

        # Schema compression potential
        schema_patterns = patterns['scene_headers'] + patterns['transitions']
        estimates['schema_gain'] = schema_patterns * 2  # ~2 tokens saved per pattern

        # RAG potential (assuming 30% reduction)
        total_tokens = self._count_tokens(text)
        estimates['rag_gain'] = int(total_tokens * 0.3)

        # Output control (assuming 20% reduction)
        estimates['output_control_gain'] = int(total_tokens * 0.2)

        # Total potential
        estimates['total_potential'] = (
            estimates['schema_gain'] +
            estimates['rag_gain'] +
            estimates['output_control_gain']
        )

        estimates['potential_ratio'] = estimates['total_potential'] / total_tokens if total_tokens > 0 else 0

        return estimates

    def batch_process(self, documents: List[Tuple[str, str]]) -> Dict:
        """
        Processa múltiplos documentos em batch

        Args:
            documents: Lista de (doc_id, text)

        Returns:
            Dict com resultados agregados
        """
        results = []
        total_original = 0
        total_compressed = 0

        for doc_id, text in documents:
            encoded, macros, stats = self.encode(text, doc_id)

            results.append({
                'doc_id': doc_id,
                'stats': stats,
                'macros_used': len(macros)
            })

            total_original += stats['original_tokens']
            total_compressed += stats['encoded_tokens']

        overall_compression = (total_original - total_compressed) / total_original if total_original > 0 else 0

        return {
            'documents_processed': len(documents),
            'total_original_tokens': total_original,
            'total_compressed_tokens': total_compressed,
            'overall_compression': overall_compression,
            'average_compression': sum(r['stats']['compression_ratio'] for r in results) / len(results),
            'best_document': max(results, key=lambda x: x['stats']['compression_ratio']),
            'results': results
        }


def test_optimized_encoder():
    """Testa o encoder otimizado com exemplos reais"""

    encoder = DigiLangV4Optimizer(use_tiktoken=True, min_freq=3)

    # Exemplos de teste
    test_cases = [
        ("star_wars", """FADE IN:

EXT. SPACE

A vast sea of stars serves as the backdrop for the MAIN TITLE.

INT. REBEL BLOCKADE RUNNER - MAIN PASSAGEWAY

The nervous Rebel troopers aim their weapons. Suddenly a tremendous blast opens up a hole in the main passageway and a score of fearsome armored spacetroopers make their way into the smoke-filled corridor.

DARTH VADER makes his way through the smoke.

VADER
(to officer)
Where are those transmissions?

CUT TO:

INT. DEATH STAR - CONFERENCE ROOM

TARKIN sits at the head of the table.

TARKIN
The Imperial Senate will no longer be of any concern to us.

VADER enters.

VADER
The plans are not aboard the ship.

DISSOLVE TO:

EXT. TATOOINE - DESERT - DAY

LUKE SKYWALKER works on his speeder. He looks at the twin suns setting on the horizon.

LUKE
(to himself)
There's got to be more to life than this.

He turns to see UNCLE OWEN approaching.

OWEN
Luke! Come help with these droids.

LUKE looks at the droids, then back at the sunset.

CUT TO:"""),

        ("godfather", """FADE IN:

INT. DON CORLEONE'S HOME OFFICE - DAY

BONASERA
I believe in America.

DON VITO CORLEONE sits behind his desk, listening.

VITO CORLEONE
Why did you go to the police? Why didn't you come to me first?

BONASERA
What do you want of me? I'll give you anything.

VITO CORLEONE
(standing)
Some day, and that day may never come, I'll call upon you to do a service for me.

CUT TO:

EXT. MALL - DAY

The wedding continues. MICHAEL CORLEONE sits at a table with KAY ADAMS.

MICHAEL
That's my family, Kay. It's not me.

KAY looks at him skeptically.

DISSOLVE TO:

INT. WOLTZ'S BEDROOM - NIGHT

WOLTZ wakes up. He feels something wet. He pulls back the covers to reveal the severed head of his prize horse.

WOLTZ
(screaming)
Ahhhhhhh!

BACK TO:"""),

        ("simple", "INT. CAFE - DAY\n\nJOHN looks at MARY.\n\nCUT TO:\n\nEXT. STREET - NIGHT")
    ]

    print("\n" + "="*80)
    print("TESTE DO DIGILANG V4 OPTIMIZED")
    print("="*80)

    for doc_id, text in test_cases:
        print(f"\n📄 Documento: {doc_id}")
        print("-" * 40)

        # Codificar
        encoded, macros, stats = encoder.encode(text, doc_id)

        # Mostrar resultados
        print(f"✅ Tokens originais: {stats['original_tokens']}")
        print(f"✅ Tokens comprimidos: {stats['encoded_tokens']}")
        print(f"✅ Tokens salvos: {stats['saved_tokens']}")
        print(f"✅ Taxa de compressão: {stats['compression_ratio']*100:.2f}%")
        print(f"✅ Macros usadas: {stats['macros_used']}")
        print(f"✅ Ganho líquido: {stats['net_gain']}")

        if macros:
            print(f"\n📝 Top 5 Macros:")
            for placeholder, expansion in list(macros.items())[:5]:
                print(f"   {placeholder} → {expansion}")

        # Testar decodificação
        decoded = encoder.decode(encoded)
        assert decoded == text, "Erro na decodificação!"
        print("✅ Decodificação verificada com sucesso!")

        # Análise de potencial
        analysis = encoder.analyze_compression_potential(text, doc_id)
        print(f"\n🎯 Potencial adicional:")
        print(f"   Schema: +{analysis['potential_additional_gain']['schema_gain']} tokens")
        print(f"   RAG: +{analysis['potential_additional_gain']['rag_gain']} tokens")
        print(f"   Output Control: +{analysis['potential_additional_gain']['output_control_gain']} tokens")
        print(f"   Potencial total: {analysis['potential_additional_gain']['potential_ratio']*100:.1f}%")

    # Teste em batch
    print("\n" + "="*80)
    print("TESTE EM BATCH")
    print("="*80)

    batch_results = encoder.batch_process(test_cases)

    print(f"\n📊 Resultados Agregados:")
    print(f"   Documentos: {batch_results['documents_processed']}")
    print(f"   Tokens totais: {batch_results['total_original_tokens']}")
    print(f"   Tokens comprimidos: {batch_results['total_compressed_tokens']}")
    print(f"   Compressão geral: {batch_results['overall_compression']*100:.2f}%")
    print(f"   Compressão média: {batch_results['average_compression']*100:.2f}%")
    print(f"   Melhor documento: {batch_results['best_document']['doc_id']} ({batch_results['best_document']['stats']['compression_ratio']*100:.2f}%)")

    print("\n✅ SISTEMA V4 OPTIMIZED FUNCIONANDO!")
    print("DIGIMUNDO PRESENTE")


if __name__ == "__main__":
    test_optimized_encoder()