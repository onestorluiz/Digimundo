#!/usr/bin/env python3
"""
⚡ TESTE DE PERFORMANCE HÍBRIDA CPU+GPU
Compara modelos e monitora uso de recursos
"""

import subprocess
import json
import time
import psutil
import threading

def monitor_resources(duration=30, stop_event=None):
    """Monitora CPU e memória durante processamento"""

    cpu_usage = []
    memory_usage = []

    start_time = time.time()
    while time.time() - start_time < duration:
        if stop_event and stop_event.is_set():
            break

        # CPU por core
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_avg = sum(cpu_per_core) / len(cpu_per_core)
        cpu_usage.append(cpu_avg)

        # Memória
        mem = psutil.virtual_memory()
        memory_usage.append(mem.percent)

        # Print em tempo real
        print(f"\r🔥 CPU: {cpu_avg:.1f}% | RAM: {mem.percent:.1f}% | Cores ativos: {sum(1 for c in cpu_per_core if c > 20)}/28", end="")

    print()  # Nova linha

    return {
        'cpu_avg': sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0,
        'cpu_max': max(cpu_usage) if cpu_usage else 0,
        'memory_avg': sum(memory_usage) / len(memory_usage) if memory_usage else 0,
        'cores_used': sum(1 for c in cpu_per_core if c > 20)
    }

def test_model(model_name, prompt):
    """Testa um modelo e monitora recursos"""

    print(f"\n🤖 Testando: {model_name}")
    print("-" * 60)

    # Thread de monitoramento
    stop_event = threading.Event()
    monitor_thread = threading.Thread(
        target=monitor_resources,
        args=(60, stop_event)
    )

    # Preparar comando
    payload = {
        'model': model_name,
        'prompt': prompt,
        'stream': False
    }

    # Iniciar monitoramento
    monitor_thread.start()

    # Executar modelo
    start_time = time.time()
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '120',
             'http://localhost:11434/api/generate',
             '-d', json.dumps(payload)],
            capture_output=True,
            text=True
        )

        processing_time = time.time() - start_time

        if result.returncode == 0 and result.stdout:
            response = json.loads(result.stdout)
            response_text = response.get('response', '')[:500]

            print(f"\n✅ Processado em {processing_time:.1f} segundos")
            print(f"📝 Resposta: {response_text}...")
        else:
            print(f"\n❌ Erro no processamento")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        processing_time = 0

    # Parar monitoramento
    stop_event.set()
    monitor_thread.join(timeout=2)

    return processing_time

def main():
    print("⚡ TESTE DE PERFORMANCE HÍBRIDA")
    print("=" * 60)

    # Prompt de teste (médio)
    prompt = """Analyze the three-act structure in screenwriting.
    Provide specific examples from The Matrix and Inception.
    Include exact timing and page numbers.
    Compare with Save the Cat beat sheet.
    This requires deep analysis of narrative structure."""

    print(f"📝 Prompt: {len(prompt)} chars")

    # Testar modelos
    models = [
        "deeplearning-cinema",      # Original (GPU 999)
        "deeplearning-hybrid",       # Novo (24 threads, GPU -1)
        "deepseek-r1:32b"           # Base sem customização
    ]

    results = {}

    for model in models:
        # Verificar se existe
        check = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True
        )

        if model in check.stdout or model == "deepseek-r1:32b":
            time_taken = test_model(model, prompt)
            results[model] = time_taken

            # Pausa entre testes
            time.sleep(5)
        else:
            print(f"\n⚠️ Modelo {model} não encontrado")

    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DE PERFORMANCE:")
    for model, time_taken in results.items():
        if time_taken > 0:
            print(f"  {model:25} → {time_taken:.1f} segundos")

    # Recomendação
    if results:
        fastest = min(results.items(), key=lambda x: x[1] if x[1] > 0 else float('inf'))
        print(f"\n🏆 MAIS RÁPIDO: {fastest[0]} ({fastest[1]:.1f}s)")

        # Verificar se híbrido é melhor
        if "deeplearning-hybrid" in results and "deeplearning-cinema" in results:
            hybrid_time = results["deeplearning-hybrid"]
            original_time = results["deeplearning-cinema"]

            if hybrid_time < original_time:
                improvement = ((original_time - hybrid_time) / original_time) * 100
                print(f"✨ Híbrido {improvement:.0f}% mais rápido!")
            else:
                print("⚠️ Original ainda mais rápido")

if __name__ == "__main__":
    main()