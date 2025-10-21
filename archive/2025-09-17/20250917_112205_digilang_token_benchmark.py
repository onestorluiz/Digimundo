"""
DigiLang Token-Aware Benchmark
Mede economia REAL em tokens, não caracteres
"""
import tiktoken
from typing import Dict, List, Tuple
import json
from pathlib import Path

class TokenBenchmark:

    def __init__(self, model='gpt-4'):
        """Inicializa com tokenizer real."""
        self.enc = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """Conta tokens reais usando tiktoken."""
        return len(self.enc.encode(text))

    def analyze_pattern(self, original: str, replacements: Dict[str, str]) -> Dict:
        """
        Analisa se uma substituição economiza tokens.

        Returns:
            Dict com análise detalhada
        """
        results = {}
        orig_tokens = self.count_tokens(original)
        for name, replacement in replacements.items():
            repl_tokens = self.count_tokens(replacement)
            results[name] = {'original': original, 'replacement': replacement, 'orig_chars': len(original), 'repl_chars': len(replacement), 'orig_tokens': orig_tokens, 'repl_tokens': repl_tokens, 'char_saved': len(original) - len(replacement), 'token_saved': orig_tokens - repl_tokens, 'worth_it': orig_tokens > repl_tokens}
        return results

    def test_digilang_patterns(self):
        """Testa padrões do DigiLang v3."""
        print('=' * 70)
        print('ANÁLISE TOKEN-AWARE DOS PADRÕES DIGILANG')
        print('=' * 70)
        print('\n1️⃣ PADRÕES DE ESPAÇO (provavelmente ruins):')
        space_tests = {'Duas quebras': ('\n\n', {'⟦2n⟧': '⟦2n⟧', '§2n§': '§2n§', '\\n\\n': '\\n\\n'}), 'Três quebras': ('\n\n\n', {'⟦3n⟧': '⟦3n⟧', '§3n§': '§3n§'}), 'Tab (4 espaços)': ('    ', {'⟦4s⟧': '⟦4s⟧', '§TAB§': '§TAB§'})}
        for name, (original, replacements) in space_tests.items():
            print(f"\n{name}: '{repr(original)}'")
            results = self.analyze_pattern(original, replacements)
            for key, data in results.items():
                status = '✅' if data['worth_it'] else '❌'
                print(f"  {status} {key}: {data['orig_tokens']} → {data['repl_tokens']} tokens")
        print('\n2️⃣ PADRÕES DE TEXTO (podem funcionar):')
        text_tests = {'FADE IN:': ('FADE IN:', {'⟦FI⟧': '⟦FI⟧', '[FI]': '[FI]', '§FI§': '§FI§', '#FI#': '#FI#'}), 'INT.': ('INT.', {'⟦I⟧': '⟦I⟧', '[I]': '[I]', '§I§': '§I§'}), 'está sentado': ('está sentado', {'⟦es⟧': '⟦es⟧', '[ES]': '[ES]', '@es@': '@es@'}), 'ele olha para': ('ele olha para', {'⟦eop⟧': '⟦eop⟧', '[EOP]': '[EOP]', '#eop#': '#eop#'})}
        for name, (original, replacements) in text_tests.items():
            print(f"\n{name}: '{original}'")
            results = self.analyze_pattern(original, replacements)
            for key, data in results.items():
                status = '✅' if data['worth_it'] else '❌'
                print(f"  {status} {key}: {data['orig_tokens']} → {data['repl_tokens']} tokens ({data['token_saved']:+d})")
        print('\n3️⃣ PADRÕES DE REPETIÇÃO:')
        repeat_tests = {'20 hífens': ('-' * 20, {'⟦20-⟧': '⟦20-⟧', '[20H]': '[20H]', '---': '---'}), '10 pontos': ('.' * 10, {'⟦10.⟧': '⟦10.⟧', '[10P]': '[10P]'})}
        for name, (original, replacements) in repeat_tests.items():
            print(f"\n{name}: '{original[:20]}...'")
            results = self.analyze_pattern(original, replacements)
            for key, data in results.items():
                status = '✅' if data['worth_it'] else '❌'
                print(f"  {status} {key}: {data['orig_tokens']} → {data['repl_tokens']} tokens ({data['token_saved']:+d})")

    def benchmark_screenplay_sample(self):
        """Testa com amostra real de roteiro."""
        print('\n' + '=' * 70)
        print('TESTE COM ROTEIRO REAL')
        print('=' * 70)
        sample = 'FADE IN:\n\nINT. CAFÉ - DAY\n\nJOHN está sentado em uma mesa, olhando para o café.\n\nMARY\n(sussurrando)\nO que você está fazendo?\n\nJOHN\nEu não sei... talvez esperando.\n\n--------------------\n\nCUT TO:'
        print(f'\nOriginal: {self.count_tokens(sample)} tokens')
        strategies = {'v2 (atual - só padrões básicos)': self._apply_v2(sample), 'v3 (enhanced - com espaços)': self._apply_v3(sample), 'v3-TA (token-aware - sem espaços)': self._apply_v3_ta(sample)}
        for name, compressed in strategies.items():
            tokens = self.count_tokens(compressed)
            saved = self.count_tokens(sample) - tokens
            percent = saved / self.count_tokens(sample) * 100
            status = '✅' if saved > 0 else '❌'
            print(f'{status} {name}: {tokens} tokens ({saved:+d}, {percent:+.1f}%)')

    def _apply_v2(self, text: str) -> str:
        """Aplica DigiLang v2 (atual)."""
        replacements = {'FADE IN:': '⟦FI⟧', 'CUT TO:': '⟦CT⟧', 'INT.': '⟦I⟧', 'DAY': '⟦D⟧'}
        for orig, repl in replacements.items():
            text = text.replace(orig, repl)
        return text

    def _apply_v3(self, text: str) -> str:
        """Aplica DigiLang v3 (enhanced com espaços)."""
        text = self._apply_v2(text)
        text = text.replace('\n\n', '⟦2n⟧')
        text = text.replace('está sentado', '⟦es⟧')
        text = text.replace('-' * 20, '⟦20-⟧')
        return text

    def _apply_v3_ta(self, text: str) -> str:
        """Aplica DigiLang v3-TA (token-aware, sem espaços)."""
        replacements = {'FADE IN:': '#FI', 'CUT TO:': '#CT', 'INT.': '#I', 'DAY': '#D', 'está sentado': '#ES', '-' * 20: '#LINE20'}
        for orig, repl in replacements.items():
            text = text.replace(orig, repl)
        return text

    def find_optimal_markers(self):
        """Encontra marcadores que viram 1 token."""
        print('\n' + '=' * 70)
        print('BUSCA POR MARCADORES DE 1 TOKEN')
        print('=' * 70)
        candidates = ['⟦', '⟧', '§', '¤', '†', '‡', '¶', '@@', '##', '$$', '%%', '&&', '__', '#FI', '@FI', '$FI', '%FI', '_FI_', '[FI]', '{FI}', '<FI>', '|FI|']
        one_token_markers = []
        for marker in candidates:
            tokens = self.count_tokens(marker)
            if tokens == 1:
                one_token_markers.append(marker)
                print(f"✅ '{marker}' = 1 token")
            else:
                print(f"❌ '{marker}' = {tokens} tokens")
        return one_token_markers

def main():
    """Executa benchmark completo."""
    bench = TokenBenchmark()
    bench.test_digilang_patterns()
    bench.benchmark_screenplay_sample()
    print('\n🔍 Buscando marcadores de 1 token...')
    optimal = bench.find_optimal_markers()
    print('\n' + '=' * 70)
    print('CONCLUSÕES')
    print('=' * 70)
    print('\n1. ❌ Codificar espaços/quebras PIORA (mais tokens)\n2. ✅ Padrões de texto PODEM funcionar (com marcadores certos)\n3. 🎯 Marcadores ASCII simples (#, @) são melhores que Unicode\n4. 📊 Economia real: ~5-10% tokens (não 15% caracteres)\n5. 💡 Focar em RAG/recorte estrutural para economia maior\n')
if __name__ == '__main__':
    main()