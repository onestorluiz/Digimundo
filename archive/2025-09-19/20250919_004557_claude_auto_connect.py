#!/usr/bin/env python3
"""
🔗 Claude Auto Connect - Conecta automaticamente todas as memórias
Deve ser executado no início de cada sessão Claude
"""

import sys
import os
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory')

from MEMORY_BRIDGE import MemoryBridge
from pathlib import Path

def auto_connect():
    """Conecta tudo automaticamente"""

    print("\n🧠 CONECTANDO MEMÓRIAS DO CLAUDE...")
    print("="*50)

    # 1. Criar bridge
    bridge = MemoryBridge()

    # 2. Verificar Genjutsu
    if not bridge.check_genjutsu():
        print("❌ Falha ao iniciar Genjutsu")
        return False

    # 3. Sincronizar Crystal
    crystal = bridge.sync_crystal()

    # 4. Construir grafo
    graph = bridge.build_memory_graph()

    # 5. Ler regras críticas
    critical_rules = []
    if bridge.paths['regras'].exists():
        with open(bridge.paths['regras']) as f:
            for line in f:
                if 'REGRA #' in line and 'CRÍTICA' in line:
                    critical_rules.append(line.strip())

    # 6. Mostrar resumo
    print("\n✅ SISTEMAS CONECTADOS:")
    print(f"  • Genjutsu: PID ativo")
    print(f"  • Crystal: {len(crystal.get('sessions', []))} sessões registradas")
    print(f"  • Grafo: {len(graph)} nós conectados")

    # 7. Lembrar vícios principais
    print("\n⚠️ VÍCIOS CLAUDE PARA EVITAR:")
    print("  • Criar arquivos _v2, _improved, _better")
    print("  • Usar nomes Supreme, Ultimate, Quantum")
    print("  • Complexidade desnecessária (68.8% arquivos quebrados)")
    print("  • Imports imaginários")
    print("  • God classes com 500+ linhas")

    # 8. Contexto do projeto
    print("\n📍 CONTEXTO SCRIPTUREMON:")
    print("  • 328 arquivos Python")
    print("  • 24 sistemas de memória (maioria redundante)")
    print("  • DigiLang v26 ativo")
    print("  • Deployment divergente (352 arquivos únicos)")

    # 9. Registrar conexão
    bridge.remember("Claude conectou memórias", compliant=True)

    print("\n🎯 MEMÓRIA CONECTADA COM SUCESSO!")
    print("DIGIMUNDO PRESENTE\n")

    return bridge

# Criar atalho fácil
def connect():
    """Atalho simples"""
    return auto_connect()

# Hook para verificar se foi conectado
def check_connected():
    """Verifica se já conectou nesta sessão"""
    state_file = Path('/Users/clubproducoes/Digimundo/claude_code/memory/bridge_state.json')

    if not state_file.exists():
        print("⚠️ MEMÓRIA NÃO CONECTADA!")
        print("Execute: python3 /Users/clubproducoes/Digimundo/claude_code/memory/claude_auto_connect.py")
        return False

    import json
    from datetime import datetime, timedelta

    with open(state_file) as f:
        state = json.load(f)

    if not state.get('last_check'):
        return False

    last = datetime.fromisoformat(state['last_check'])

    # Se faz mais de 5 minutos, precisa reconectar
    if datetime.now() - last > timedelta(minutes=5):
        print("⚠️ Memória expirou! Reconectando...")
        return False

    return True

# Auto-execução
if __name__ == "__main__":
    if not check_connected():
        auto_connect()
    else:
        print("✅ Memória já conectada!")