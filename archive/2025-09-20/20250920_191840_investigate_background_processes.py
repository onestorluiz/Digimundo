#!/usr/bin/env python3
"""
🔍 INVESTIGADOR DE PROCESSOS EM BACKGROUND
Identifica EXATAMENTE o que está rodando e porque não conseguimos terminar
"""

import psutil
import subprocess
import time
from pathlib import Path

def get_claude_code_processes():
    """
    Identifica todos os processos relacionados ao Claude Code
    """
    processes = []

    # Buscar por processos Python com Claude Code
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])

            # Filtrar processos relacionados
            if any(keyword in cmdline.lower() for keyword in [
                'scripturemon', 'mixtral', 'ollama', 'genjutsu', 'claude',
                'activate_full_deep_learning', 'migrate', 'ml_unified'
            ]):
                # Calcular tempo de execução
                runtime = time.time() - proc.info['create_time']

                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': cmdline,
                    'runtime_minutes': runtime / 60,
                    'cpu_percent': proc.cpu_percent(),
                    'memory_mb': proc.memory_info().rss / 1024 / 1024
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes

def get_bash_background_info():
    """
    Identifica processos bash em background
    """
    bash_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'ppid']):
        try:
            if proc.info['name'] in ['bash', 'sh', 'zsh']:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if cmdline and len(cmdline) > 10:  # Ignorar shells vazios
                    bash_processes.append({
                        'pid': proc.info['pid'],
                        'ppid': proc.info['ppid'],
                        'cmdline': cmdline[:100] + '...' if len(cmdline) > 100 else cmdline
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return bash_processes

def check_ollama_status():
    """
    Verifica status do Ollama
    """
    try:
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True, timeout=10)
        return {
            'running': result.returncode == 0,
            'output': result.stdout if result.returncode == 0 else result.stderr
        }
    except Exception as e:
        return {'running': False, 'error': str(e)}

def analyze_process_tree():
    """
    Analisa árvore de processos para entender dependências
    """
    print("🌳 ÁRVORE DE PROCESSOS RELACIONADOS")
    print("-" * 50)

    processes = get_claude_code_processes()

    # Organizar por PID pai
    tree = {}
    for proc in processes:
        try:
            parent = psutil.Process(proc['pid']).parent()
            parent_pid = parent.pid if parent else 0
            if parent_pid not in tree:
                tree[parent_pid] = []
            tree[parent_pid].append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            if 0 not in tree:
                tree[0] = []
            tree[0].append(proc)

    for parent_pid, children in tree.items():
        if parent_pid == 0:
            print("📋 Processos órfãos/raiz:")
        else:
            try:
                parent_name = psutil.Process(parent_pid).name()
                print(f"📋 Filhos do processo {parent_pid} ({parent_name}):")
            except:
                print(f"📋 Filhos do processo {parent_pid} (desconhecido):")

        for proc in children:
            print(f"  PID {proc['pid']}: {proc['name']}")
            print(f"    CMD: {proc['cmdline'][:80]}...")
            print(f"    Runtime: {proc['runtime_minutes']:.1f} min")
            print(f"    CPU: {proc['cpu_percent']:.1f}% | RAM: {proc['memory_mb']:.1f} MB")
            print()

def force_terminate_analysis():
    """
    Analisa por que não conseguimos terminar processos
    """
    print("🔧 ANÁLISE DE TERMINAÇÃO FORÇADA")
    print("-" * 50)

    processes = get_claude_code_processes()

    for proc in processes:
        pid = proc['pid']
        print(f"\n🎯 Analisando PID {pid}")

        try:
            p = psutil.Process(pid)

            # Status do processo
            print(f"  Status: {p.status()}")
            print(f"  Terminal: {p.terminal()}")
            print(f"  Background: {p.is_running()}")

            # Verificar se é um processo zombie ou suspenso
            if p.status() in ['zombie', 'stopped']:
                print(f"  ⚠️ Processo em estado especial: {p.status()}")

            # Verificar se tem filhos
            children = p.children(recursive=True)
            if children:
                print(f"  👶 {len(children)} processos filhos")
                for child in children[:3]:
                    print(f"    - PID {child.pid}: {child.name()}")

            # Tentar kill suave
            print(f"  🔄 Tentando SIGTERM...")
            try:
                p.terminate()
                time.sleep(1)
                if p.is_running():
                    print(f"    ❌ SIGTERM ignorado")
                else:
                    print(f"    ✅ SIGTERM funcionou")
                    continue
            except psutil.NoSuchProcess:
                print(f"    ✅ Processo já morreu")
                continue
            except Exception as e:
                print(f"    ❌ Erro no SIGTERM: {e}")

            # Tentar kill forçado
            print(f"  💀 Tentando SIGKILL...")
            try:
                p.kill()
                time.sleep(1)
                if p.is_running():
                    print(f"    ❌ SIGKILL ignorado - processo imortal?")
                else:
                    print(f"    ✅ SIGKILL funcionou")
            except psutil.NoSuchProcess:
                print(f"    ✅ Processo já morreu")
            except Exception as e:
                print(f"    ❌ Erro no SIGKILL: {e}")

        except psutil.NoSuchProcess:
            print(f"  ✅ Processo {pid} já não existe")
        except Exception as e:
            print(f"  ❌ Erro ao analisar {pid}: {e}")

def main():
    print("🔍 INVESTIGADOR DE PROCESSOS EM BACKGROUND")
    print("=" * 60)

    # 1. Listar todos os processos relacionados
    print("\n📋 PROCESSOS RELACIONADOS AO CLAUDE CODE")
    print("-" * 50)

    processes = get_claude_code_processes()
    print(f"Encontrados {len(processes)} processos relacionados:")

    for proc in processes:
        print(f"\nPID {proc['pid']}: {proc['name']}")
        print(f"  CMD: {proc['cmdline'][:80]}...")
        print(f"  Runtime: {proc['runtime_minutes']:.1f} min")
        print(f"  CPU: {proc['cpu_percent']:.1f}% | RAM: {proc['memory_mb']:.1f} MB")

    # 2. Status do Ollama
    print(f"\n🦙 STATUS DO OLLAMA")
    print("-" * 50)
    ollama_status = check_ollama_status()
    if ollama_status['running']:
        print("✅ Ollama está rodando")
        print(f"Modelos ativos:\n{ollama_status['output']}")
    else:
        print("❌ Ollama não está rodando")
        if 'error' in ollama_status:
            print(f"Erro: {ollama_status['error']}")

    # 3. Processos bash
    print(f"\n⌨️ PROCESSOS BASH EM BACKGROUND")
    print("-" * 50)
    bash_procs = get_bash_background_info()
    print(f"Encontrados {len(bash_procs)} processos bash:")
    for proc in bash_procs:
        print(f"  PID {proc['pid']} (pai: {proc['ppid']}): {proc['cmdline']}")

    # 4. Análise da árvore
    print(f"\n")
    analyze_process_tree()

    # 5. Análise de terminação
    force_terminate_analysis()

    print("\n" + "=" * 60)
    print("📊 RESUMO")
    print(f"• {len(processes)} processos Claude Code ativos")
    print(f"• {len(bash_procs)} processos bash em background")
    print(f"• Ollama: {'✅ Ativo' if ollama_status['running'] else '❌ Inativo'}")

    # Recomendações
    print(f"\n💡 RECOMENDAÇÕES")
    if len(processes) > 3:
        print("• Muitos processos ativos - considerar limpeza")
    if any(p['runtime_minutes'] > 60 for p in processes):
        print("• Processos rodando há mais de 1 hora")
    if any(p['cpu_percent'] > 50 for p in processes):
        print("• Processos com alto uso de CPU")

if __name__ == "__main__":
    main()