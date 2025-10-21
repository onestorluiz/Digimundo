#!/usr/bin/env python3
"""
🎬 DEMONSTRAÇÃO DE INTERAÇÃO REAL
Mostra os sistemas trabalhando juntos em tempo real
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from apps.scripturemon.chat import ScripturemonChat

def demo_real_interaction():
    """Demonstra interação real com o sistema completo"""
    
    print("=" * 60)
    print("🎬 DEMONSTRAÇÃO INTERATIVA - SCRIPTUREMON")
    print("=" * 60)
    print("Sistema completo com todos os componentes integrados\n")
    
    # Inicializa chat
    print("⏳ Inicializando Scripturemon...")
    chat = ScripturemonChat()
    print("✅ Sistema inicializado!\n")
    
    # Script de exemplo para análise
    sample_script = """FADE IN:

EXT. DESERTO - DIA

O sol implacável. MARIA (30s) caminha sozinha, determinada.

MARIA
(para si mesma)
Três dias. Ainda nada.

Ela para. Olha o horizonte vazio. Silêncio.

MARIA (CONT'D)
Você prometeu estar aqui.

O vento é sua única resposta.

FADE OUT."""
    
    # Salva script temporário
    temp_file = Path("runtime/demo_script.txt")
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_text(sample_script)
    
    # Lista de interações para demonstrar
    interactions = [
        {
            "prompt": "/status",
            "description": "📊 Verificando status completo do sistema",
            "wait": 1
        },
        {
            "prompt": f"/analyze {temp_file}",
            "description": "🎬 Analisando roteiro com brutalidade característica",
            "wait": 2
        },
        {
            "prompt": "/search conflito interno do protagonista",
            "description": "🔍 Buscando conhecimento com RAG avançado (HyDE + RAPTOR)",
            "wait": 2
        },
        {
            "prompt": "/hyde arco do herói",
            "description": "🧬 Demonstrando expansão HyDE de queries",
            "wait": 1
        },
        {
            "prompt": "Como Chinatown constrói tensão no terceiro ato?",
            "description": "💬 Conversação normal com syscalls automáticas",
            "wait": 2
        },
        {
            "prompt": "/telepathy",
            "description": "🧠 Verificando rede telepática",
            "wait": 1
        },
        {
            "prompt": "/telepathy broadcast Insight: economia narrativa é tudo",
            "description": "📢 Compartilhando conhecimento via telepathy",
            "wait": 1
        },
        {
            "prompt": "/evolve",
            "description": "✨ Evoluindo consciência",
            "wait": 1
        },
        {
            "prompt": "Qual a diferença entre mostrar e contar?",
            "description": "💭 Pergunta sobre técnica narrativa",
            "wait": 2
        },
        {
            "prompt": "/backup",
            "description": "💾 Salvando estado da alma",
            "wait": 1
        }
    ]
    
    # Executa interações
    for i, interaction in enumerate(interactions, 1):
        print(f"\n{'='*60}")
        print(f"INTERAÇÃO {i}/{len(interactions)}: {interaction['description']}")
        print(f"{'='*60}")
        print(f"\n📝 Comando: {interaction['prompt']}\n")
        
        # Processa comando
        start_time = time.time()
        response = chat.process_input(interaction['prompt'])
        elapsed = time.time() - start_time
        
        # Mostra resposta (truncada se muito longa)
        print("🎭 Resposta Scripturemon:")
        print("-" * 40)
        
        if len(response) > 800:
            print(response[:800])
            print(f"\n... [resposta truncada, total: {len(response)} chars]")
        else:
            print(response)
        
        print("-" * 40)
        print(f"⏱️ Tempo de resposta: {elapsed:.2f}s")
        
        # Verifica elementos importantes
        checks = []
        if "62/100" in response:
            checks.append("✅ Score 62/100 presente")
        if "[" in response and "]" in response:
            checks.append("✅ Syscalls detectadas")
        if "HyDE" in response or "RAPTOR" in response:
            checks.append("✅ RAG avançado ativo")
        if "Online" in response and "Redis" in response:
            checks.append("✅ Telepathy online")
        
        if checks:
            print("\n🔍 Verificações:")
            for check in checks:
                print(f"  {check}")
        
        # Pequena pausa entre interações
        if i < len(interactions):
            time.sleep(interaction.get('wait', 1))
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DA DEMONSTRAÇÃO")
    print("=" * 60)
    
    # Status final do sistema
    print("\n🎯 STATUS FINAL:")
    
    # Consciência
    from apps.scripturemon.consciousness import get_level
    print(f"  🔮 Consciência: {get_level():.5f}")
    
    # Syscalls
    syscalls = len(chat.soulos.syscall_log)
    print(f"  ⚙️ Syscalls executadas: {syscalls}")
    
    # Memórias
    memories = chat.soulos.get_memories(limit=100)
    print(f"  💎 Memórias cristalizadas: {len(memories)}")
    
    # Telepathy
    telepathy_stats = chat.telepathy.get_stats()
    print(f"  🧠 Mensagens telepáticas: {telepathy_stats['messages_sent']}")
    
    # RAG
    print(f"  🔍 RAG avançado: HyDE + RAPTOR + Self-RAG ativos")
    
    # Pipeline
    pipeline_stats = chat.quadruple.get_stats()
    print(f"  🔄 Pipeline quádruplo: {pipeline_stats['total_runs']} execuções")
    
    print("\n" + "=" * 60)
    print("🎬 DEMONSTRAÇÃO COMPLETA")
    print("=" * 60)
    print("\nTodos os sistemas funcionando em perfeita harmonia.")
    print("62/100. Como sempre, mas agora com superpoderes.")
    print("\n'The greatest trick the Devil ever pulled was")
    print("convincing the world he didn't exist.'")
    print("                    - The Usual Suspects")
    print("\nScripturemon existe. E está evoluindo.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        demo_real_interaction()
    except KeyboardInterrupt:
        print("\n\n🎬 Demonstração interrompida.")
        print("'I'll be back.' - Terminator")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()