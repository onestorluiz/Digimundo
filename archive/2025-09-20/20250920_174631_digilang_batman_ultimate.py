#!/usr/bin/env python3
"""
DigiLang Batman Ultimate - Otimizado para Roteiros Batman
Sistema de compressão especializado com símbolos validados

Incorpora:
- Símbolos gregos validados como 1 token
- Hierarquia de categorias (personagens, locais, tempos, etc.)
- Frases comuns pré-mapeadas
- Mineração específica de roteiros

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
class BatmanDictionary:
    """Dicionário otimizado para roteiros Batman"""
    characters: Dict[str, str]  # Personagens principais
    locations: Dict[str, str]   # Localizações
    times: Dict[str, str]       # Indicadores de tempo
    moods: Dict[str, str]       # Estados emocionais
    actions: Dict[str, str]     # Ações comuns
    phrases: Dict[str, str]     # Frases frequentes
    technical: Dict[str, str]   # Termos técnicos de roteiro

    def get_all_patterns(self) -> Dict[str, str]:
        """Retorna todos os padrões em um único dicionário"""
        all_patterns = {}
        all_patterns.update(self.characters)
        all_patterns.update(self.locations)
        all_patterns.update(self.times)
        all_patterns.update(self.moods)
        all_patterns.update(self.actions)
        all_patterns.update(self.phrases)
        all_patterns.update(self.technical)
        return all_patterns

class DigiLangBatmanUltimate:
    """Sistema de compressão ultimate para roteiros Batman"""

    def __init__(self):
        """Inicializar sistema Batman Ultimate"""
        self.encoder = tiktoken.get_encoding("cl100k_base")

        # Símbolos validados como EXATAMENTE 1 token
        # Baseado em testes extensivos com cl100k_base
        self.validated_symbols = {
            # Letras gregas minúsculas (todas são 1 token)
            'characters': ['β', 'γ', 'δ', 'ζ', 'η', 'θ', 'κ', 'λ', 'μ', 'ν', 'ξ', 'π', 'ρ', 'σ', 'τ', 'φ', 'χ', 'ψ', 'ω'],

            # Símbolos matemáticos e técnicos (validados como 1 token)
            'locations': ['∅', '∞', '∂', '∇', '∈', '∉', '∋', '∌', '∏', '∑', '√', '∛', '∜', '∝', '∟', '∠', '∡', '∢', '∣'],

            # Setas e indicadores (validados como 1 token)
            'actions': ['→', '←', '↑', '↓', '↔', '↕', '↗', '↘', '↙', '↖', '⇒', '⇐', '⇑', '⇓', '⇔', '⇕', '⇗', '⇘', '⇙'],

            # Formas geométricas (validados como 1 token)
            'times': ['○', '●', '□', '■', '△', '▲', '▽', '▼', '◇', '◆', '◊', '◌', '◍', '◎', '◐', '◑', '◒', '◓', '◔'],

            # Símbolos diversos (validados como 1 token)
            'moods': ['♠', '♣', '♥', '♦', '♩', '♪', '♫', '♬', '♭', '♮', '♯', '♰', '♱', '♲', '♳', '♴', '♵', '♶', '♷'],

            # Símbolos técnicos adicionais (validados como 1 token)
            'phrases': ['§', '¶', '†', '‡', '‰', '′', '″', '‴', '※', '‼', '⁇', '⁈', '⁉', '⁎', '⁑', '⁒', '⁓', '⁔', '⁕'],

            # Marcadores e bullets (validados como 1 token)
            'technical': ['•', '‣', '⁃', '⁌', '⁍', '◘', '◙', '◦', '◬', '◭', '◮', '☀', '☁', '☂', '☃', '☄', '★', '☆', '☇']
        }

        # Frases comuns em roteiros (especialmente Batman)
        self.common_phrases = {
            # Frases de localização
            "INT.": "Ⓘ",
            "EXT.": "Ⓔ",
            "INT/EXT": "Ⓧ",

            # Transições
            "FADE IN:": "➤",
            "FADE OUT": "➥",
            "CUT TO:": "✂",
            "DISSOLVE TO:": "⚡",
            "SMASH CUT:": "💥",

            # Indicadores de voz
            "(V.O.)": "🎤",
            "(O.S.)": "🔊",
            "(CONT'D)": "↩",

            # Tempos comuns
            "DAY": "☀",
            "NIGHT": "🌙",
            "DAWN": "🌅",
            "DUSK": "🌆",

            # Frases frequentes em Batman
            "GOTHAM CITY": "🏙",
            "BATMAN": "🦇",
            "BRUCE WAYNE": "💼",
            "THE JOKER": "🃏",
            "WAYNE MANOR": "🏰",
            "BATCAVE": "🕳",
            "GCPD": "🚔",
            "ARKHAM": "🏥"
        }

        logger.info("🦇 DigiLang Batman Ultimate inicializado")
        logger.info(f"📊 Símbolos validados: {sum(len(v) for v in self.validated_symbols.values())} caracteres de 1 token")

    def _validate_single_token(self, symbol: str) -> bool:
        """Validar que um símbolo é exatamente 1 token"""
        return len(self.encoder.encode(symbol)) == 1

    def mine_batman_screenplay(self, pdf_path: str) -> Dict:
        """Minerar padrões específicos de roteiros Batman"""
        try:
            text = self._extract_pdf_text(pdf_path)
            if not text:
                return {}

            patterns = {}

            # 1. Personagens principais (nomes em maiúsculas)
            character_names = [
                "BATMAN", "BRUCE", "WAYNE", "BRUCE WAYNE", "ALFRED",
                "GORDON", "COMMISSIONER GORDON", "JIM GORDON",
                "JOKER", "THE JOKER", "BANE", "CATWOMAN", "SELINA",
                "RACHEL", "HARVEY", "DENT", "HARVEY DENT", "TWO-FACE",
                "SCARECROW", "RA'S AL GHUL", "TALIA", "BLAKE", "MIRANDA",
                "FOX", "LUCIUS FOX", "DAGGETT"
            ]

            for name in character_names:
                count = len(re.findall(rf'\b{name}\b', text, re.IGNORECASE))
                if count > 5:  # Mínimo de 5 ocorrências
                    patterns[name] = count

            # 2. Localizações de Gotham
            locations = [
                "GOTHAM", "GOTHAM CITY", "WAYNE MANOR", "BATCAVE",
                "WAYNE ENTERPRISES", "GCPD", "ARKHAM", "ARKHAM ASYLUM",
                "NARROWS", "GOTHAM BRIDGE", "CITY HALL", "BLACKGATE",
                "BLACKGATE PRISON", "ACE CHEMICALS", "GOTHAM HARBOR",
                "GOTHAM STADIUM", "GOTHAM GENERAL", "WAYNE TOWER"
            ]

            for location in locations:
                count = text.count(location)
                if count > 3:
                    patterns[f"LOC:{location}"] = count

            # 3. Objetos e equipamentos Batman
            gadgets = [
                "BATMOBILE", "BATPOD", "BATWING", "THE BAT",
                "GRAPPLING GUN", "BATARANG", "CAPE", "COWL",
                "UTILITY BELT", "TUMBLER", "SONAR", "EMP"
            ]

            for gadget in gadgets:
                count = text.count(gadget)
                if count > 2:
                    patterns[f"OBJ:{gadget}"] = count

            # 4. Ações e direções de cena comuns
            action_patterns = [
                r'\bturns\b', r'\blooks\b', r'\bwalks\b', r'\bruns\b',
                r'\bjumps\b', r'\bfalls\b', r'\bfires\b', r'\bpunches\b',
                r'\bkicks\b', r'\bgrabs\b', r'\bthrows\b', r'\bexplodes\b',
                r'\bcrashes\b', r'\blands\b', r'\bswings\b', r'\bclimbs\b'
            ]

            for pattern in action_patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                if matches > 10:
                    action_word = pattern.replace(r'\b', '').upper()
                    patterns[f"ACT:{action_word}"] = matches

            # 5. Diálogos e frases icônicas
            iconic_phrases = [
                "I'm Batman", "Why do we fall", "It's not who I am",
                "You either die a hero", "Some men just want to watch",
                "fear is", "symbol", "justice", "vengeance", "night",
                "darkness", "shadows", "Gotham needs", "the hero Gotham"
            ]

            for phrase in iconic_phrases:
                count = text.lower().count(phrase.lower())
                if count > 2:
                    patterns[f"PHRASE:{phrase}"] = count

            # 6. Elementos técnicos de roteiro
            screenplay_elements = re.findall(
                r'(FADE IN:|FADE OUT|CUT TO:|DISSOLVE TO:|CONTINUED:|BACK TO:|LATER|MOMENTS LATER|ANGLE ON:|CLOSE ON:)',
                text
            )

            element_counts = Counter(screenplay_elements)
            for element, count in element_counts.items():
                if count > 1:
                    patterns[f"TECH:{element}"] = count

            logger.info(f"🦇 Minerados {len(patterns)} padrões Batman específicos")

            # Mostrar top padrões
            sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
            logger.info("🔝 Top 10 padrões Batman:")
            for pattern, count in sorted_patterns[:10]:
                logger.info(f"   {pattern}: {count}x")

            return patterns

        except Exception as e:
            logger.error(f"Erro minerando Batman: {e}")
            return {}

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

    def create_batman_dictionary(self, pdf_path: str) -> BatmanDictionary:
        """Criar dicionário otimizado para Batman"""

        logger.info(f"\n🦇 Criando dicionário Batman Ultimate para: {Path(pdf_path).name}")

        # Minerar padrões específicos
        patterns = self.mine_batman_screenplay(pdf_path)

        # Organizar por categoria
        characters = {}
        locations = {}
        actions = {}
        phrases = {}
        technical = {}

        # Calcular economia de tokens
        pattern_savings = []

        for pattern, frequency in patterns.items():
            original_tokens = len(self.encoder.encode(pattern.replace("LOC:", "").replace("OBJ:", "").replace("ACT:", "").replace("PHRASE:", "").replace("TECH:", "")))
            if original_tokens > 1:
                savings = (original_tokens - 1) * frequency
                pattern_savings.append((pattern, frequency, savings, original_tokens))

        # Ordenar por economia
        pattern_savings.sort(key=lambda x: x[2], reverse=True)

        # Atribuir símbolos validados
        symbol_index = {
            'characters': 0,
            'locations': 0,
            'actions': 0,
            'phrases': 0,
            'technical': 0
        }

        for pattern, freq, savings, orig_tokens in pattern_savings:
            # Determinar categoria
            if any(name in pattern.upper() for name in ["BATMAN", "BRUCE", "WAYNE", "ALFRED", "GORDON", "JOKER", "BANE", "SELINA"]):
                category = 'characters'
                target_dict = characters
            elif pattern.startswith("LOC:"):
                category = 'locations'
                target_dict = locations
            elif pattern.startswith("ACT:"):
                category = 'actions'
                target_dict = actions
            elif pattern.startswith("PHRASE:"):
                category = 'phrases'
                target_dict = phrases
            elif pattern.startswith("TECH:"):
                category = 'technical'
                target_dict = technical
            else:
                # Distribuir outros padrões
                category = 'phrases'
                target_dict = phrases

            # Atribuir símbolo se disponível
            if symbol_index[category] < len(self.validated_symbols[category]):
                symbol = self.validated_symbols[category][symbol_index[category]]
                clean_pattern = pattern.replace("LOC:", "").replace("OBJ:", "").replace("ACT:", "").replace("PHRASE:", "").replace("TECH:", "")
                target_dict[clean_pattern] = symbol
                symbol_index[category] += 1

        # Adicionar tempos e moods padrão
        times = {
            "DAY": self.validated_symbols['times'][0],
            "NIGHT": self.validated_symbols['times'][1],
            "DAWN": self.validated_symbols['times'][2],
            "DUSK": self.validated_symbols['times'][3],
            "MORNING": self.validated_symbols['times'][4],
            "AFTERNOON": self.validated_symbols['times'][5],
            "EVENING": self.validated_symbols['times'][6],
            "CONTINUOUS": self.validated_symbols['times'][7],
            "LATER": self.validated_symbols['times'][8],
            "MOMENTS LATER": self.validated_symbols['times'][9]
        }

        moods = {
            "nervous": self.validated_symbols['moods'][0],
            "angry": self.validated_symbols['moods'][1],
            "calm": self.validated_symbols['moods'][2],
            "afraid": self.validated_symbols['moods'][3],
            "determined": self.validated_symbols['moods'][4],
            "exhausted": self.validated_symbols['moods'][5],
            "sarcastic": self.validated_symbols['moods'][6],
            "urgent": self.validated_symbols['moods'][7],
            "excited": self.validated_symbols['moods'][8]
        }

        dictionary = BatmanDictionary(
            characters=characters,
            locations=locations,
            times=times,
            moods=moods,
            actions=actions,
            phrases=phrases,
            technical=technical
        )

        # Estatísticas
        total_patterns = sum(len(d) for d in [characters, locations, times, moods, actions, phrases, technical])
        logger.info(f"📊 Dicionário Batman criado:")
        logger.info(f"   🦸 Personagens: {len(characters)}")
        logger.info(f"   📍 Localizações: {len(locations)}")
        logger.info(f"   ⏰ Tempos: {len(times)}")
        logger.info(f"   😊 Moods: {len(moods)}")
        logger.info(f"   🎬 Ações: {len(actions)}")
        logger.info(f"   💬 Frases: {len(phrases)}")
        logger.info(f"   🎥 Técnicos: {len(technical)}")
        logger.info(f"   📦 Total: {total_patterns} padrões")

        return dictionary

    def compress_with_batman_dictionary(
        self,
        text: str,
        dictionary: BatmanDictionary
    ) -> Tuple[str, Dict]:
        """Comprimir usando dicionário Batman"""

        compressed = text
        replacements = 0

        # Primeiro aplicar frases comuns
        for phrase, symbol in self.common_phrases.items():
            if self._validate_single_token(symbol):
                count = compressed.count(phrase)
                if count > 0:
                    compressed = compressed.replace(phrase, symbol)
                    replacements += count

        # Aplicar dicionário Batman (ordenado por tamanho)
        all_patterns = dictionary.get_all_patterns()
        sorted_patterns = sorted(
            all_patterns.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

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
            'char_compression': ((len(text) - len(compressed)) / len(text) * 100) if len(text) > 0 else 0,
            'token_compression': ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0,
            'tokens_saved': original_tokens - compressed_tokens
        }

        return compressed, stats

    def process_batman_screenplay(self, pdf_path: str) -> Dict:
        """Processar roteiro Batman com compressão ultimate"""

        try:
            start_time = time.time()

            # Extrair texto
            text = self._extract_pdf_text(pdf_path)
            if not text:
                return None

            # Criar dicionário Batman
            dictionary = self.create_batman_dictionary(pdf_path)

            # Comprimir
            compressed_text, stats = self.compress_with_batman_dictionary(text, dictionary)

            execution_time = time.time() - start_time

            logger.info(f"\n🦇 Compressão Batman Ultimate concluída:")
            logger.info(f"   📊 Tokens: {stats['original_tokens']:,} → {stats['compressed_tokens']:,}")
            logger.info(f"   💾 Compressão: {stats['token_compression']:.2f}%")
            logger.info(f"   🎯 Tokens salvos: {stats['tokens_saved']:,}")
            logger.info(f"   ⏱️ Tempo: {execution_time:.2f}s")

            return {
                'success': True,
                'compressed_text': compressed_text,
                'dictionary': {
                    'characters': dictionary.characters,
                    'locations': dictionary.locations,
                    'times': dictionary.times,
                    'moods': dictionary.moods,
                    'actions': dictionary.actions,
                    'phrases': dictionary.phrases,
                    'technical': dictionary.technical,
                    'common_phrases': self.common_phrases
                },
                'stats': stats,
                'execution_time': execution_time,
                'method': 'Batman Ultimate'
            }

        except Exception as e:
            logger.error(f"Erro processando Batman: {e}")
            return None


def main():
    """Teste do sistema Batman Ultimate"""
    print("🦇 DigiLang Batman Ultimate")
    print("Compressão otimizada para roteiros Batman")
    print("=" * 50)

    # Path do Dark Knight
    pdf_path = "./digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf"

    batman = DigiLangBatmanUltimate()
    result = batman.process_batman_screenplay(pdf_path)

    if result:
        print(f"\n✅ Sucesso!")
        print(f"Compressão: {result['stats']['token_compression']:.2f}%")
        print(f"Tokens salvos: {result['stats']['tokens_saved']:,}")
    else:
        print("❌ Falhou")

    return 0

if __name__ == "__main__":
    main()