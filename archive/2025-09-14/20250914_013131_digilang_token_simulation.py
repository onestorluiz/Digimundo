#!/usr/bin/env python3
"""
Simulação do problema de tokens vs caracteres no DigiLang
Demonstra por que o feedback está correto
"""

def simulate_tokenization(text: str) -> int:
    """
    Simula tokenização aproximada (sem tiktoken).
    Regras baseadas em observações de GPT-4:
    - Palavras comuns PT = 1-2 tokens
    - \n\n = 1 token (especial)
    - Unicode raro (⟦⟧) = 2-3 tokens cada
    - ASCII simples = 1 token
    """
    # Simulação simplificada mas realista
    tokens = 0

    # Casos especiais conhecidos
    special_patterns = {
        "\n\n": 1,      # Quebra dupla = 1 token!
        "\n": 0.5,      # Quebra simples = 0.5 token
        "    ": 1,      # Tab/4 espaços = 1 token
        "FADE IN:": 3,  # 3 tokens típico
        "INT.": 1,      # 1 token
        "está": 1,      # Palavra comum PT
        "para": 1,      # Palavra comum PT
    }

    # Processa padrões especiais
    remaining = text
    for pattern, token_count in special_patterns.items():
        count = remaining.count(pattern)
        if count > 0:
            tokens += count * token_count
            remaining = remaining.replace(pattern, "")

    # Conta caracteres restantes
    # Unicode especial (⟦⟧§¤) = 2-3 tokens cada
    unicode_special = len([c for c in remaining if ord(c) > 127])
    tokens += unicode_special * 2.5

    # ASCII normal ~4 chars = 1 token
    ascii_chars = len([c for c in remaining if ord(c) <= 127])
    tokens += ascii_chars / 4

    return int(tokens)


def compare_strategies():
    """Compara diferentes estratégias de compressão."""
    print("=" * 70)
    print("DEMONSTRAÇÃO: POR QUE TOKENS ≠ CARACTERES")
    print("=" * 70)

    # Caso 1: Quebras de linha
    print("\n🔴 CASO 1: Codificar quebras de linha")
    original = "Texto\n\nOutro texto"
    compressed_v3 = "Texto⟦2n⟧Outro texto"

    print(f"Original:    '{original}'")
    print(f"  Caracteres: {len(original)}")
    print(f"  Tokens (simulado): ~{simulate_tokenization(original)}")

    print(f"Comprimido:  '{compressed_v3}'")
    print(f"  Caracteres: {len(compressed_v3)} (economia: {len(original)-len(compressed_v3)})")
    print(f"  Tokens (simulado): ~{simulate_tokenization(compressed_v3)} (PIOROU!)")

    # Caso 2: Padrões de roteiro
    print("\n🟡 CASO 2: Padrões de roteiro")
    patterns = [
        ("FADE IN:", ["⟦FI⟧", "#FI", "FI"]),
        ("INT. CAFÉ - DAY", ["⟦I⟧ CAFÉ - ⟦D⟧", "#I CAFÉ - #D", "I. CAFÉ - D"]),
        ("está sentado", ["⟦es⟧", "#ES", "ES"]),
    ]

    for original, replacements in patterns:
        print(f"\n'{original}' ({len(original)} chars, ~{simulate_tokenization(original)} tokens)")
        for repl in replacements:
            char_diff = len(original) - len(repl)
            token_orig = simulate_tokenization(original)
            token_repl = simulate_tokenization(repl)
            token_diff = token_orig - token_repl

            status = "✅" if token_diff > 0 else "❌"
            print(f"  {status} '{repl}': {char_diff:+d} chars, {token_diff:+.0f} tokens")

    # Caso 3: Roteiro completo
    print("\n🎬 CASO 3: Roteiro completo")
    sample = """FADE IN:

INT. CAFÉ - DAY

JOHN está sentado em uma mesa.

MARY
O que você está fazendo?

JOHN
Eu não sei.

CUT TO:"""

    # Diferentes versões
    versions = {
        "Original": sample,
        "v2 (atual)": sample.replace("FADE IN:", "⟦FI⟧").replace("INT.", "⟦I⟧").replace("CUT TO:", "⟦CT⟧"),
        "v3 (com espaços)": sample.replace("FADE IN:", "⟦FI⟧").replace("\n\n", "⟦2n⟧").replace("está sentado", "⟦es⟧"),
        "v3-TA (token-aware)": sample.replace("FADE IN:", "#FI").replace("INT.", "#I").replace("CUT TO:", "#CT"),
    }

    print(f"\nComparação de estratégias:")
    baseline_tokens = simulate_tokenization(versions["Original"])

    for name, text in versions.items():
        chars = len(text)
        tokens = simulate_tokenization(text)
        char_saved = len(sample) - chars
        token_saved = baseline_tokens - tokens

        if name == "Original":
            print(f"\n{name}:")
            print(f"  {chars} chars, ~{tokens} tokens (baseline)")
        else:
            char_pct = (char_saved / len(sample)) * 100
            token_pct = (token_saved / baseline_tokens) * 100 if baseline_tokens > 0 else 0
            status = "✅" if token_saved > 0 else "❌"

            print(f"\n{status} {name}:")
            print(f"  Chars: {char_saved:+d} ({char_pct:+.1f}%)")
            print(f"  Tokens: {token_saved:+.0f} ({token_pct:+.1f}%)")


def show_key_insights():
    """Mostra os insights principais do feedback."""
    print("\n" + "=" * 70)
    print("INSIGHTS CRÍTICOS DO FEEDBACK")
    print("=" * 70)

    print("""
1️⃣ O PROBLEMA FUNDAMENTAL:
   • Tokenizers modernos (GPT-4) já comprimem bem PT-BR
   • "\\n\\n" = 1 token, mas "⟦2n⟧" = 3-4 tokens
   • Palavras comuns ("está", "para") = 1 token cada
   • Unicode especial (⟦⟧) = múltiplos tokens

2️⃣ POR QUE v3 ORIGINAL FALHA:
   ❌ Codificar espaços/quebras AUMENTA tokens
   ❌ Marcadores Unicode pioram ainda mais
   ❌ Medimos chars quando deveríamos medir tokens

3️⃣ SOLUÇÃO v3-TA (Token-Aware):
   ✅ NÃO codificar espaços/quebras para LLM
   ✅ Usar marcadores ASCII simples (#, @)
   ✅ Só substituir se economizar tokens reais
   ✅ Medir com tokenizer real (tiktoken)

4️⃣ ONDE REALMENTE ECONOMIZAR:
   🎯 RAG/Recorte: enviar só cenas relevantes (30-80% economia)
   🎯 Schema compacto: S:[INT|CAFÉ|DAY] (10-35% economia)
   🎯 Context caching: não reenviar regras fixas (10-20% economia)

5️⃣ CONCLUSÃO:
   DigiLang deve ser TOKEN-AWARE para funcionar com LLMs.
   Para storage/logs, pode usar compressão por caracteres.
""")


if __name__ == "__main__":
    compare_strategies()
    show_key_insights()