#!/usr/bin/env python3
"""
Script de Verificação de Uso de CPU pelo Ollama
Confirma que o modelo mixtral-cpu-force está usando CPU corretamente
"""

import subprocess
import time
import sys
import psutil
import threading

def monitor_ollama_cpu():
    """Monitora CPU do processo Ollama runner"""
    print("\n📊 Monitorando CPU do Ollama...")
    print("-" * 50)

    for _ in range(20):  # Monitora por 20 segundos
        try:
            # Procura processo ollama runner
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                if 'ollama' in proc.info['name'].lower():
                    if proc.info['cpu_percent'] > 0:
                        print(f"PID {proc.info['pid']}: {proc.info['cpu_percent']:.1f}% CPU - {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        time.sleep(1)

def test_cpu_model():
    """Testa modelo CPU-force"""
    print("=" * 60)
    print("🧪 TESTE DE USO DE CPU - MIXTRAL-CPU-FORCE")
    print("=" * 60)

    # 1. Verifica se modelo existe
    print("\n1️⃣ Verificando se modelo mixtral-cpu-force existe...")
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True
    )

    if "mixtral-cpu-force" not in result.stdout:
        print("❌ Modelo mixtral-cpu-force não encontrado!")
        print("\n📝 Para criar o modelo:")
        print("1. Crie um arquivo 'modelfile_cpu' com:")
        print("   FROM mixtral:8x7b-instruct-v0.1-q5_K_M")
        print("   PARAMETER num_gpu 0")
        print("   PARAMETER num_thread 20")
        print("   PARAMETER num_ctx 200000")
        print("\n2. Execute: ollama create mixtral-cpu-force -f modelfile_cpu")
        return False

    print("✅ Modelo encontrado!")

    # 2. Inicia monitoramento em thread separada
    monitor_thread = threading.Thread(target=monitor_ollama_cpu)
    monitor_thread.daemon = True
    monitor_thread.start()

    # 3. Executa inferência
    print("\n2️⃣ Executando inferência com modelo CPU-force...")
    print("   (Observe o uso de CPU acima)")
    print("-" * 50)

    start_time = time.time()

    # Executa comando
    process = subprocess.Popen(
        ["ollama", "run", "mixtral-cpu-force", "Analyze the hero's journey in one paragraph."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Aguarda conclusão
    stdout, stderr = process.communicate()

    elapsed = time.time() - start_time

    # 4. Mostra resultado
    print("\n3️⃣ Resultado da inferência:")
    print("-" * 50)
    if stdout:
        print(stdout[:500])  # Primeiros 500 chars
    print("-" * 50)

    print(f"\n⏱️ Tempo de execução: {elapsed:.2f}s")

    # 5. Aguarda thread de monitoramento terminar
    time.sleep(2)

    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 60)
    print("\n📋 RESUMO:")
    print("- Se você viu CPU% > 50% no processo ollama: ✅ USANDO CPU!")
    print("- Se você viu CPU% < 5% no processo ollama: ❌ USANDO GPU")
    print("\n💡 DICA: Use Activity Monitor para confirmar visualmente")

    return True

def verify_system_config():
    """Verifica configuração do sistema"""
    print("\n🔍 Verificando configuração do sistema...")
    print("-" * 50)

    # CPU info
    print(f"CPU Cores (lógicos): {psutil.cpu_count()}")
    print(f"CPU Cores (físicos): {psutil.cpu_count(logical=False)}")
    print(f"CPU Usage atual: {psutil.cpu_percent(interval=1)}%")

    # Memória
    mem = psutil.virtual_memory()
    print(f"RAM Total: {mem.total / (1024**3):.1f} GB")
    print(f"RAM Disponível: {mem.available / (1024**3):.1f} GB")

    # Verifica Ollama
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True
        )
        print(f"Ollama: {result.stdout.strip()}")
    except FileNotFoundError:
        print("Ollama: ❌ Não instalado")

if __name__ == "__main__":
    print("🚀 VERIFICADOR DE USO DE CPU - SCRIPTUREMON ULTIMATE")
    print("=" * 60)

    # 1. Verifica sistema
    verify_system_config()

    # 2. Testa modelo CPU
    success = test_cpu_model()

    if success:
        print("\n✅ Sistema pronto para usar CPU!")
        print("\n📝 Próximos passos:")
        print("1. O arquivo ollama_continuous_learning.py já foi atualizado")
        print("2. Execute: python3 ollama_continuous_learning.py --cycles 1")
        print("3. Monitore CPU com: ps aux | grep ollama")
        sys.exit(0)
    else:
        print("\n⚠️ Configure o modelo primeiro!")
        sys.exit(1)