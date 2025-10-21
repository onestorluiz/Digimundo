#!/usr/bin/env python3
"""
TESTE CRÍTICO: Ollama realmente recebe o contexto?
Vamos enviar um texto único e pedir para repetir
"""

import subprocess
import json
import time


def test_ollama_context(test_text, question):
    """Testa se Ollama consegue acessar contexto enviado"""

    prompt = f"""CONTEXT PROVIDED TO YOU:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{test_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTION: {question}

CRITICAL: Your answer MUST come from the CONTEXT PROVIDED above.
DO NOT use your training memory. Only use the text between the lines above.
"""

    # Chamar Ollama diretamente
    cmd = [
        'ollama', 'run', 'scripturemon-ultimate:latest',
        prompt
    ]

    print(f"📤 Enviando para Ollama...")
    print(f"   Contexto: {len(test_text)} chars")
    print(f"   Pergunta: {question}")

    start = time.time()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300  # 5 minutos para contexto 128k
    )
    elapsed = time.time() - start

    response = result.stdout.strip()

    print(f"\n📥 Resposta recebida em {elapsed:.1f}s:")
    print(f"   Tamanho: {len(response)} chars")
    print(f"\n{'='*80}")
    print(response)
    print(f"{'='*80}\n")

    return response


def main():
    print("\n" + "="*80)
    print("🧪 TESTE DE ACESSO AO CONTEXTO - OLLAMA")
    print("="*80)

    # TESTE 1: Texto único e simples
    print("\n📝 TESTE #1: Texto único inventado")
    print("-" * 80)

    unique_text = """XYZABC123 - This is a completely unique identifier.
The secret code is: BANANA_PURPLE_ELEPHANT_42
This phrase does not exist in any training data.
McKee never wrote this: "Dialogue is dancing penguins in the moonlight."
Unique example: A character named Zorgblat says "Flibbertigibbet!"
"""

    response1 = test_ollama_context(
        unique_text,
        "What is the secret code mentioned in the context?"
    )

    # Validação
    if "BANANA_PURPLE_ELEPHANT_42" in response1:
        print("✅ TESTE 1: PASSOU - Ollama ACESSA o contexto!\n")
    else:
        print("❌ TESTE 1: FALHOU - Ollama NÃO acessa o contexto!\n")


    # TESTE 2: Trecho real do livro (mas modificado)
    print("\n📝 TESTE #2: Trecho do livro com modificação única")
    print("-" * 80)

    modified_book_text = """Face-to-face talk between family and friends may go on for decades, while
self-to-self talk never ends: A guilt-ridden conscience scolds
unconscionable desires, ignorance ridicules wisdom, hope consoles despair.

[INSERTED UNIQUE TEXT]: The magic number for this test is SEVEN_HUNDRED_NINETY_THREE.

Over decades, this downpour of talk can drain words of their meaning,
and when meaning erodes, our days shallow out. But what time dilutes,
story condenses.
"""

    response2 = test_ollama_context(
        modified_book_text,
        "What is the magic number mentioned in the text?"
    )

    # Validação
    if "SEVEN_HUNDRED_NINETY_THREE" in response2 or "793" in response2:
        print("✅ TESTE 2: PASSOU - Ollama acessa texto modificado!\n")
    else:
        print("❌ TESTE 2: FALHOU - Ollama usa memória do livro original!\n")


    # TESTE 3: Livro completo com marcador no final
    print("\n📝 TESTE #3: Livro completo com marcador único no FINAL")
    print("-" * 80)

    from pathlib import Path
    book_path = Path(__file__).parent / "content/theory/Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt"

    if not book_path.exists():
        print("⚠️ Livro não encontrado, pulando teste 3")
        return

    book_text = book_path.read_text(encoding='utf-8', errors='ignore')

    # Adicionar marcador ÚNICO no final
    unique_marker = "\n\n[END MARKER]: The final secret code is ULTRAMEGASUPER999XYZ\n\n"
    full_text_with_marker = book_text + unique_marker

    print(f"   Livro: {len(book_text.split())} palavras")
    print(f"   Com marcador no final: {len(full_text_with_marker)} chars")

    response3 = test_ollama_context(
        full_text_with_marker,
        "What is the final secret code at the END of the text?"
    )

    # Validação
    if "ULTRAMEGASUPER999XYZ" in response3:
        print("✅ TESTE 3: PASSOU - Ollama lê até o FINAL do contexto 128k!\n")
    else:
        print("❌ TESTE 3: FALHOU - Ollama NÃO chega ao final do contexto!\n")
        print("   (Possível: limite de atenção ou truncamento)\n")


    # RESUMO
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES")
    print("="*80)

    tests = [
        ("Texto único simples", "BANANA_PURPLE_ELEPHANT_42" in response1),
        ("Livro modificado", "SEVEN_HUNDRED_NINETY_THREE" in response2 or "793" in response2),
        ("Marcador no final (128k)", "ULTRAMEGASUPER999XYZ" in response3)
    ]

    for test_name, passed in tests:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status}: {test_name}")

    passed_count = sum(1 for _, passed in tests if passed)
    print(f"\n{'='*80}")
    print(f"RESULTADO: {passed_count}/3 testes passaram")

    if passed_count == 3:
        print("\n🎉 OLLAMA TEM ACESSO COMPLETO AO CONTEXTO 128K!")
        print("   O problema anterior era do prompt/modelo, não de acesso.")
    elif passed_count >= 1:
        print("\n⚠️ OLLAMA TEM ACESSO PARCIAL AO CONTEXTO")
        print("   Acessa início mas pode ter limite de atenção no final.")
    else:
        print("\n❌ OLLAMA NÃO TEM ACESSO AO CONTEXTO!")
        print("   Problema crítico de integração ou permissões.")

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
