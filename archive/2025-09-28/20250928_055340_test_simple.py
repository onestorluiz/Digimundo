#!/usr/bin/env python3
"""
Teste simples e direto do modelo scripturemon-v9-final
"""

import subprocess
import json
import time

def test_basic_response():
    """Teste básico de resposta"""
    print("=" * 60)
    print("TESTE BÁSICO - SCRIPTUREMON v9")
    print("=" * 60)

    # Prompt muito simples
    prompt = "Responda apenas: OK"

    print(f"\nPrompt: {prompt}")
    print("Aguardando resposta do modelo...")

    start_time = time.time()

    try:
        # Executar com timeout maior
        result = subprocess.run(
            ["ollama", "run", "scripturemon-v9-final", prompt],
            capture_output=True,
            text=True,
            timeout=180  # 3 minutos
        )

        elapsed = time.time() - start_time

        print(f"\n✅ Resposta recebida em {elapsed:.1f}s")
        print("-" * 60)
        print("RESPOSTA:")
        print(result.stdout[:500])  # Primeiros 500 chars

        if len(result.stdout) > 500:
            print(f"... [+{len(result.stdout)-500} chars]")

        return True

    except subprocess.TimeoutExpired:
        print(f"\n❌ Timeout após 180s")
        return False
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False

def test_json_output():
    """Teste de output JSON"""
    print("\n" + "=" * 60)
    print("TESTE JSON OUTPUT")
    print("=" * 60)

    # Prompt para JSON
    prompt = """Analise brevemente e retorne JSON:
    FADE IN:
    João entra na sala.
    JOÃO: Olá.
    FADE OUT.

    Retorne apenas um JSON com campos: titulo, personagens, paginas."""

    print(f"\nPrompt: {prompt[:100]}...")
    print("Aguardando resposta JSON...")

    start_time = time.time()

    try:
        result = subprocess.run(
            ["ollama", "run", "scripturemon-v9-final", prompt],
            capture_output=True,
            text=True,
            timeout=180
        )

        elapsed = time.time() - start_time

        print(f"\n✅ Resposta recebida em {elapsed:.1f}s")

        output = result.stdout

        # Tentar extrair JSON
        if "{" in output and "}" in output:
            json_start = output.find("{")
            json_end = output.rfind("}") + 1
            json_str = output[json_start:json_end]

            try:
                parsed = json.loads(json_str)
                print("\n✅ JSON válido parseado:")
                print(json.dumps(parsed, indent=2)[:500])
                return True
            except:
                print("\n⚠️ JSON presente mas inválido")
                print(f"Tentativa: {json_str[:200]}...")
                return False
        else:
            print("\n❌ Nenhum JSON na resposta")
            print(f"Resposta: {output[:200]}...")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n❌ Timeout após 180s")
        return False
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🎬 TESTES SIMPLES - SCRIPTUREMON v9-FINAL\n")

    tests_passed = 0
    tests_total = 2

    # Teste 1: Resposta básica
    if test_basic_response():
        tests_passed += 1

    # Teste 2: Output JSON
    if test_json_output():
        tests_passed += 1

    # Resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)

    print(f"\n📊 {tests_passed}/{tests_total} testes passaram")

    if tests_passed == tests_total:
        print("✅ TODOS OS TESTES PASSARAM!")
    elif tests_passed > 0:
        print("⚠️ ALGUNS TESTES PASSARAM")
    else:
        print("❌ NENHUM TESTE PASSOU")

    print("\nDIGIMUNDO PRESENTE 🥷")