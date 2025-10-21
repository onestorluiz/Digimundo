#!/usr/bin/env python3
"""
🚀 TESTE SIMPLES MULTI-OLLAMA
Testa comunicação básica com múltiplos modelos
"""

import subprocess
import time
import json

def test_ollama_model(model_name: str, prompt: str):
    """Testa um modelo Ollama específico"""
    print(f"\n📋 Testando: {model_name}")
    print("-" * 40)

    try:
        # Comando simplificado
        cmd = f'echo "{prompt}" | ollama run {model_name}'

        # Executar com timeout
        start = time.time()
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed = time.time() - start

        if result.returncode == 0:
            response = result.stdout.strip()
            print(f"✅ Sucesso ({elapsed:.1f}s)")
            print(f"📝 Resposta: {response[:200]}...")
            return True
        else:
            print(f"❌ Erro: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("⏱️ Timeout (30s)")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🚀 TESTE MULTI-OLLAMA SIMPLIFICADO")
    print("=" * 60)

    # Modelos para teste
    test_models = [
        ("tinyllama:latest", "Say hello in 5 words"),
        ("phi3:mini", "What is 2+2?"),
        ("gemma2:9b", "Write hello world in Python"),
        ("llama3.2:3b", "Complete: Once upon a time")
    ]

    results = {}

    for model, prompt in test_models:
        success = test_ollama_model(model, prompt)
        results[model] = success
        time.sleep(1)  # Pausa entre testes

    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    working = sum(1 for v in results.values() if v)
    total = len(results)

    for model, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {model}")

    print(f"\n✨ {working}/{total} modelos funcionando")

if __name__ == "__main__":
    main()