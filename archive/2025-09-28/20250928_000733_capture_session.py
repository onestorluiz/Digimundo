#!/usr/bin/env python3
"""
💾 CAPTURA DE SESSÃO - Salva memórias desta conversa
"""

import sys
sys.path.append('/Users/clubproducoes/Digimundo/claude_code')

from memory.claude_memory_hook import ClaudeMemoryHook
from datetime import datetime

# Conversa atual sobre sistema de memória
CONVERSA_ATUAL = """
Descobri que o sistema de memória existe mas não está sendo usado automaticamente.
A solução foi criar hooks automáticos para capturar memórias.
Vamos usar ClaudeMemoryHook para persistir conhecimento automaticamente.
REGRA #54: Sistema de memória deve capturar automaticamente.
Nunca deixar memórias serem perdidas entre sessões.
O problema era que o sistema estava parado na garagem.
Aprendi que ter sistema não é suficiente, precisa integrar.
Lição aprendida: Automação > Processo manual.
✅ Sistema de memória agora captura automaticamente!
"""

def capture_current():
    """Captura memórias da sessão atual"""
    print("🧠 CAPTURANDO MEMÓRIAS DA SESSÃO ATUAL...\n")
    
    hook = ClaudeMemoryHook()
    stats = hook.extract_and_save(CONVERSA_ATUAL)
    
    print(f"📊 ESTATÍSTICAS DE CAPTURA:")
    print(f"  • Decisões: {stats['decisions']}")
    print(f"  • Regras: {stats['rules']}")
    print(f"  • Aprendizados: {stats['learnings']}")
    
    # Adiciona memória sobre esta sessão
    hook.save_memory(
        'session_memory_system_fixed',
        'Sistema de memória foi consertado em 23/09/2025. '
        'Criado ClaudeMemoryHook para captura automática. '
        'Antes: 2 memórias. Agora: captura contínua.',
        'milestone'
    )
    
    print("\n✅ MEMÓRIAS SALVAS COM SUCESSO!")
    
    # Mostra estado atual do banco
    import sqlite3
    conn = sqlite3.connect('/Users/clubproducoes/Digimundo/claude_code/memory/claude_memory.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM memories")
    total_memories = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM decisions")
    total_decisions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM learned_rules")
    total_rules = cursor.fetchone()[0]
    
    print(f"\n📊 ESTADO DO BANCO:")
    print(f"  • Total de memórias: {total_memories}")
    print(f"  • Total de decisões: {total_decisions}")
    print(f"  • Total de regras: {total_rules}")
    
    conn.close()

if __name__ == '__main__':
    capture_current()
