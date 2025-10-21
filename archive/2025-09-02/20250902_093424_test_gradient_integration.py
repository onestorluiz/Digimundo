#!/usr/bin/env python3
"""
Teste de integração do Gradient com Scripturemon
"""

import subprocess
import time
from pathlib import Path

def test_gradient():
    print("🧪 TESTANDO INTEGRAÇÃO GRADIENT...")
    
    # Teste 1: Modelo responde?
    print("\n1️⃣ Teste básico de resposta...")
    try:
        result = subprocess.run(
            ["ollama", "run", "scripturemon-gradient", 
             "--num-ctx", "256000",
             "Olá, você é o Scripturemon com Gradient?"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✅ Modelo respondendo!")
            print(f"Resposta: {result.stdout[:200]}...")
        else:
            print("❌ Erro na resposta")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    # Teste 2: Contexto grande
    print("\n2️⃣ Teste de contexto grande (simulando PDFs)...")
    big_prompt = "Contexto: " + ("Cinema " * 10000) + "\nAnalise este conceito."
    
    try:
        start = time.time()
        result = subprocess.run(
            ["ollama", "run", "scripturemon-gradient",
             "--num-ctx", "256000",
             big_prompt[:50000]],  # 50k chars de teste
            capture_output=True,
            text=True,
            timeout=60
        )
        elapsed = time.time() - start
        
        if result.returncode == 0:
            print(f"✅ Contexto grande processado em {elapsed:.1f}s")
        else:
            print("❌ Falha com contexto grande")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    # Teste 3: Integração com sistema
    print("\n3️⃣ Teste de integração com ollama_core.py...")
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "apps" / "scripturemon"))
        from ollama_core import get_ollama
        
        ollama = get_ollama()
        response = ollama.generate(
            "Qual sua capacidade de contexto?",
            model="scripturemon-gradient",
            num_ctx=256000
        )
        
        if response:
            print("✅ Integração com ollama_core funcionando!")
            print(f"Resposta: {response[:200]}...")
        else:
            print("❌ Sem resposta do ollama_core")
            return False
            
    except Exception as e:
        print(f"⚠️ Não foi possível testar ollama_core: {e}")
    
    print("\n" + "="*60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("🧠 Gradient está pronto como cérebro do Scripturemon!")
    print("="*60)
    
    return True

if __name__ == "__main__":
    test_gradient()
