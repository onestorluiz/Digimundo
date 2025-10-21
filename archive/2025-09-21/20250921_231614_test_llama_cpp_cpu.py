#!/usr/bin/env python3
"""
Teste llama-cpp-python CPU-ONLY
Compilado SEM suporte Metal - deve usar apenas CPU!
"""

import os
import time
import psutil
from llama_cpp import Llama

def monitor_cpu():
    """Monitora CPU do processo."""
    pid = os.getpid()
    process = psutil.Process(pid)
    return process.cpu_percent()

def find_model_path():
    """Encontra arquivo GGUF do Mixtral."""
    # Possíveis locais onde Ollama guarda modelos
    possible_paths = [
        os.path.expanduser("~/.ollama/models/blobs"),
        os.path.expanduser("~/.ollama/models"),
        "/usr/local/share/ollama/models",
    ]

    for base_path in possible_paths:
        if not os.path.exists(base_path):
            continue

        for root, dirs, files in os.walk(base_path):
            for file in files:
                # Procura por arquivos grandes (modelos)
                filepath = os.path.join(root, file)
                try:
                    size_gb = os.path.getsize(filepath) / (1024**3)
                    if size_gb > 10:  # Modelos grandes (>10GB)
                        print(f"📁 Encontrado arquivo grande: {filepath} ({size_gb:.1f}GB)")
                        return filepath
                except:
                    pass

    # Se não encontrar, usa path manual
    print("⚠️ Modelo não encontrado automaticamente")
    print("   Use: ollama show mixtral-cpu-force --modelfile")
    print("   Para descobrir o path do modelo")
    return None

def test_llama_cpp():
    """Testa inferência com llama-cpp-python."""
    print("=" * 60)
    print("🧪 TESTE LLAMA-CPP-PYTHON CPU-ONLY")
    print("=" * 60)

    # 1. Encontra modelo
    model_path = find_model_path()

    if not model_path:
        print("\n❌ Modelo não encontrado!")
        print("\nPara testar manualmente:")
        print("1. Descubra o path: ollama show mixtral-cpu-force --modelfile")
        print("2. Procure por 'FROM' no output")
        print("3. Use o path completo aqui")
        return

    print(f"\n✅ Usando modelo: {model_path}")

    # 2. Carrega modelo com CPU-only
    print("\n📊 Carregando modelo (CPU-only, 20 threads)...")

    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,  # Contexto menor para teste
            n_threads=20,  # 20 threads CPU
            n_gpu_layers=0,  # ZERO layers na GPU!
            verbose=True  # Mostra logs
        )

        print("✅ Modelo carregado!")

        # 3. Monitora CPU antes
        print("\n📊 CPU antes da inferência:", monitor_cpu(), "%")

        # 4. Faz inferência
        print("\n🤖 Gerando texto (monitore Activity Monitor)...")
        start_time = time.time()

        result = llm(
            "Analyze the three-act structure in screenwriting. Be brief.",
            max_tokens=100,
            temperature=0.7,
            stop=["###"]
        )

        elapsed = time.time() - start_time

        # 5. Monitora CPU durante
        cpu_during = monitor_cpu()
        print(f"\n📊 CPU durante inferência: {cpu_during}%")

        # 6. Mostra resultado
        print("\n📝 Resposta gerada:")
        print("-" * 40)
        print(result['choices'][0]['text'][:200])
        print("-" * 40)

        # 7. Estatísticas
        tokens = result['usage']['total_tokens']
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   Tempo: {elapsed:.2f}s")
        print(f"   Tokens: {tokens}")
        print(f"   Velocidade: {tokens/elapsed:.1f} tokens/s")
        print(f"   CPU médio: {cpu_during}%")

        if cpu_during > 5:
            print("\n✅ SUCESSO! Modelo rodando em CPU!")
        else:
            print("\n⚠️ CPU baixo - pode estar usando GPU ainda")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\nDicas:")
        print("- Verifique se o modelo existe")
        print("- Tente com um modelo menor primeiro")
        print("- Use: CMAKE_ARGS='-DLLAMA_METAL=OFF' pip install llama-cpp-python")

if __name__ == "__main__":
    # Verifica instalação
    try:
        import llama_cpp
        print(f"✅ llama-cpp-python versão: {llama_cpp.__version__}")
    except:
        print("❌ llama-cpp-python não instalado!")
        print("   Instale com: CMAKE_ARGS='-DLLAMA_METAL=OFF' pip install llama-cpp-python")
        exit(1)

    test_llama_cpp()