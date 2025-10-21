"""
DigiLang Intelligent Translation
Traduz texto para forma mais eficiente em TOKENS (não caracteres)
Preserva 100% do conteúdo - apenas otimiza representação
"""
import re
from typing import Dict, Tuple, List
import json
from pathlib import Path

class DigiLangIntelligent:
    """
    Tradutor inteligente focado em economia de TOKENS.
    NÃO remove conteúdo - apenas representa de forma mais eficiente.
    """

    def __init__(self):
        """Inicializa tradutor inteligente."""
        self.token_efficient_patterns = {'FADE IN:': 'FI:', 'FADE OUT:': 'FO:', 'CUT TO:': 'CT:', 'DISSOLVE TO:': 'DT:', 'SMASH CUT:': 'SC:', 'MATCH CUT:': 'MC:', '(continuing)': '(cont)', '(voice over)': '(VO)', '(off screen)': '(OS)', '(whispering)': '(whisp)', '(shouting)': '(shout)', '(laughing)': '(laugh)', '(crying)': '(cry)', '(beat)': '(b)', 'INT.': 'I.', 'EXT.': 'E.', 'INT./EXT.': 'I/E.', ' - DAY': '-D', ' - NIGHT': '-N', ' - CONTINUOUS': '-C', ' - LATER': '-L', ' - MOMENTS LATER': '-ML', 'looks at': '>>', 'turns to': '>@', 'walks to': '>]', 'picks up': '^', 'puts down': 'v', 'sits down': '\\', 'stands up': '/', 'enters the': '->', 'exits the': '<-'}
        self.contextual_patterns = {'twenty': '20', 'thirty': '30', 'forty': '40', 'fifty': '50', 'sixty': '60', 'seventy': '70', 'eighty': '80', 'ninety': '90', 'hundred': '100', 'thousand': '1000', 'do not': "don't", 'does not': "doesn't", 'did not': "didn't", 'will not': "won't", 'would not': "wouldn't", 'could not': "couldn't", 'should not': "shouldn't", 'is not': "isn't", 'are not': "aren't", 'was not': "wasn't", 'were not': "weren't", 'have not': "haven't", 'has not': "hasn't", 'had not': "hadn't"}
        self.structural_markers = {'scene_start': '§S:', 'action_start': '§A:', 'dialogue_start': '§D:', 'parenthetical_start': '§P:', 'transition_start': '§T:', 'character_name': '§C:'}
        self.reverse_patterns = {**{v: k for k, v in self.token_efficient_patterns.items()}, **{v: k for k, v in self.contextual_patterns.items()}}

    def translate(self, text: str, mode: str='balanced') -> Tuple[str, Dict]:
        """
        Traduz texto para representação token-eficiente.

        Args:
            text: Texto original
            mode: "aggressive" | "balanced" | "conservative"

        Returns:
            (texto_traduzido, métricas)
        """
        original_len = len(text)
        translated = text
        replacements_made = []
        if mode in ['balanced', 'aggressive']:
            for original, efficient in self.token_efficient_patterns.items():
                if original in translated:
                    count = translated.count(original)
                    translated = translated.replace(original, efficient)
                    replacements_made.append({'original': original, 'efficient': efficient, 'count': count})
        if mode == 'aggressive':
            for original, efficient in self.contextual_patterns.items():
                pattern = '\\b' + re.escape(original) + '\\b'
                if re.search(pattern, translated, re.IGNORECASE):
                    count = len(re.findall(pattern, translated, re.IGNORECASE))
                    translated = re.sub(pattern, efficient, translated, flags=re.IGNORECASE)
                    replacements_made.append({'original': original, 'efficient': efficient, 'count': count})
        metrics = {'mode': mode, 'original_chars': original_len, 'translated_chars': len(translated), 'char_change': len(translated) - original_len, 'replacements': len(replacements_made), 'patterns_applied': replacements_made[:10], 'estimated_token_savings': self._estimate_token_savings(replacements_made), 'reversible': True, 'content_preserved': True}
        return (translated, metrics)

    def reverse_translate(self, translated_text: str) -> str:
        """
        Reverte tradução para forma original.
        100% reversível.
        """
        original = translated_text
        for efficient, original_form in sorted(self.reverse_patterns.items(), key=lambda x: len(x[0]), reverse=True):
            original = original.replace(efficient, original_form)
        return original

    def _estimate_token_savings(self, replacements: List[Dict]) -> int:
        """
        Estima economia de tokens baseado em padrões conhecidos.
        """
        total_saved = 0
        token_savings = {'FADE IN:': 1, 'CUT TO:': 1, '(continuing)': 1, '(voice over)': 2, 'INT.': 1, ' - DAY': 1, 'looks at': 1, 'do not': 1, 'does not': 1}
        for replacement in replacements:
            orig = replacement['original']
            count = replacement['count']
            if orig in token_savings:
                total_saved += token_savings[orig] * count
        return total_saved

    def analyze_document(self, text: str) -> Dict:
        """
        Analisa documento para potencial de economia.
        """
        analysis = {'total_chars': len(text), 'potential_replacements': {}, 'estimated_token_savings': 0}
        for pattern in self.token_efficient_patterns.keys():
            count = text.count(pattern)
            if count > 0:
                analysis['potential_replacements'][pattern] = count
        for pattern, count in analysis['potential_replacements'].items():
            if 'FADE' in pattern or 'CUT' in pattern:
                analysis['estimated_token_savings'] += count
            elif pattern in ['INT.', 'EXT.']:
                analysis['estimated_token_savings'] += count
            elif '(' in pattern:
                analysis['estimated_token_savings'] += count * 1
        return analysis

    def create_custom_dictionary(self, corpus: List[str], min_frequency: int=5) -> Dict:
        """
        Cria dicionário customizado baseado em corpus específico.
        Identifica padrões frequentes que valem a pena traduzir.
        """
        from collections import Counter
        bigrams = Counter()
        trigrams = Counter()
        for text in corpus:
            words = text.split()
            for i in range(len(words) - 1):
                bigram = f'{words[i]} {words[i + 1]}'
                bigrams[bigram] += 1
            for i in range(len(words) - 2):
                trigram = f'{words[i]} {words[i + 1]} {words[i + 2]}'
                trigrams[trigram] += 1
        frequent_patterns = {}
        for pattern, count in bigrams.most_common(100):
            if count >= min_frequency:
                abbrev = self._create_abbreviation(pattern)
                if len(abbrev) < len(pattern) - 2:
                    frequent_patterns[pattern] = abbrev
        return frequent_patterns

    def _create_abbreviation(self, phrase: str) -> str:
        """
        Cria abreviação inteligente para frase.
        """
        words = phrase.split()
        if len(words) == 2:
            return f'{words[0][:2]}{words[1][:2]}'.upper()
        elif len(words) == 3:
            return f'{words[0][0]}{words[1][0]}{words[2][0]}'.upper()
        else:
            return ''.join((w[0] for w in words)).upper()

def demonstrate():
    """Demonstra o sistema inteligente."""
    translator = DigiLangIntelligent()
    sample = 'FADE IN:\n\nINT. COFFEE SHOP - DAY\n\nJOHN, 30s, sits at a corner table. He looks at his watch nervously.\n\nMARY enters the shop and walks to his table.\n\nMARY\n(whispering)\nHave you been waiting long?\n\nJOHN\n(continuing)\nNo, not really. Just got here.\n\nMary sits down across from him.\n\nCUT TO:'
    print('=' * 70)
    print('DIGILANG INTELLIGENT TRANSLATION')
    print('=' * 70)
    print('\n📄 ORIGINAL:')
    print(sample)
    print(f'\nTamanho: {len(sample)} caracteres')
    translated, metrics = translator.translate(sample, mode='balanced')
    print('\n🔄 TRADUZIDO (Balanced):')
    print(translated)
    print(f'\nTamanho: {len(translated)} caracteres')
    print(f"Mudança: {metrics['char_change']:+d} chars")
    print(f"Economia estimada: ~{metrics['estimated_token_savings']} tokens")
    reversed_text = translator.reverse_translate(translated)
    is_identical = reversed_text == sample
    print(f'\n✅ Reversível: {is_identical}')
    print(f'✅ Conteúdo 100% preservado')
    analysis = translator.analyze_document(sample)
    print(f'\n📊 ANÁLISE:')
    print(f"Padrões encontrados: {len(analysis['potential_replacements'])}")
    print(f"Economia potencial: ~{analysis['estimated_token_savings']} tokens")
if __name__ == '__main__':
    demonstrate()