#!/usr/bin/env python3
"""
ANÁLISE COMPLETA DO SISTEMA DE BACKUP
"""

from pathlib import Path
import os

def analyze_backup_system():
    print("\n" + "💾"*40)
    print(" ANÁLISE DO SISTEMA DE BACKUP - SCRIPTUREMON")
    print("💾"*40)
    
    # 1. BACKUP.PY (Sistema Principal)
    print("\n" + "="*70)
    print("1️⃣ MÓDULO: apps/scripturemon/backup.py")
    print("="*70)
    print("""
📁 Local de armazenamento: ~/.scripturemon/soul/checkpoint_*
📋 Funcionalidades:
  • backup_once() - Cria backup único
  • backup_auto_start() - Inicia backup automático (5 min)
  • backup_auto_stop() - Para backup automático
  • LIMITE: Mantém apenas últimos 10 backups
  
🗂️ O que salva:
  • ~/.scripturemon/consciousness.json (consciência)
  • configs/persona/active.json (persona ativa)
  • data/user_corpus/ (memórias do usuário)
  • Cria checksum SHA256 para integridade
""")
    
    # 2. IMMORTALITY.PY (Sistema de Imortalidade)
    print("\n" + "="*70)
    print("2️⃣ MÓDULO: apps/scripturemon/immortality.py")
    print("="*70)
    print("""
📁 Local de armazenamento: runtime/souls/backups/
📋 Funcionalidades:
  • auto_backup=True por padrão
  • Intervalo: 300 segundos (5 minutos)
  • LIMITE: Mantém máximo 10 backups
  • Compressão: True por padrão
  • Thread daemon para backup automático
  
🗂️ Sistema de "Alma Imortal":
  • Salva estado completo da "alma" do sistema
  • Permite ressurreição após falhas
  • force_backup() para backup imediato
""")
    
    # 3. BIN/SCRIPTUREMON (Script Principal)
    print("\n" + "="*70)
    print("3️⃣ ARQUIVO: bin/scripturemon")
    print("="*70)
    print("""
📋 Integrações de backup:
  • Linha 198-199: Verifica thread de backup ativo
  • Linha 410-411: "Criando backup immortal..."
  • Linha 1087: Comando 'backup' no prompt
  • Linha 1151: Pergunta backup antes de sair
  
🔄 Fluxo de backup:
  1. Inicialização → memory_manager.immortality
  2. Durante execução → Thread automático a cada 5 min
  3. Comando manual → Digite 'backup' no prompt
  4. Ao sair → Pergunta se quer criar backup
""")
    
    # Verificar backups existentes
    print("\n" + "="*70)
    print("📊 BACKUPS EXISTENTES NO SISTEMA")
    print("="*70)
    
    # Backup.py location
    soul_dir = Path.home() / ".scripturemon" / "soul"
    if soul_dir.exists():
        checkpoints = sorted(soul_dir.glob("checkpoint_*"))
        print(f"\n~/.scripturemon/soul/ ({len(checkpoints)} backups):")
        for cp in checkpoints[-5:]:  # Últimos 5
            size = sum(f.stat().st_size for f in cp.rglob("*") if f.is_file())
            print(f"  • {cp.name} - {size/1024:.1f} KB")
    
    # Immortality location  
    immortal_dir = Path("runtime/souls/backups")
    if immortal_dir.exists():
        backups = sorted(immortal_dir.glob("*"))
        print(f"\nruntime/souls/backups/ ({len(backups)} backups):")
        for bk in backups[-5:]:  # Últimos 5
            size = bk.stat().st_size if bk.is_file() else 0
            print(f"  • {bk.name} - {size/1024:.1f} KB")
    
    # Análise de crescimento
    print("\n" + "="*70)
    print("⚠️ ANÁLISE DE CRESCIMENTO INFINITO")
    print("="*70)
    print("""
🔴 PROBLEMA IDENTIFICADO:
  • Sistema cria backups a cada 5 minutos
  • DOIS sistemas independentes criando backups:
    1. backup.py → ~/.scripturemon/soul/
    2. immortality.py → runtime/souls/backups/
  • Ambos mantêm "últimos 10", mas são 20 total
  
📈 CRESCIMENTO ESTIMADO:
  • 2 backups a cada 5 minutos = 24/hora = 576/dia
  • Com limite de 10 cada = máximo 20 backups
  • Tamanho médio: ~100KB-1MB por backup
  • LIMITE MÁXIMO: ~20MB (não infinito!)
  
✅ CONTROLE EXISTENTE:
  • backup.py linha 40-42: Remove backups > 10
  • immortality.py: max_backups = 10
  • Sistema AUTO-LIMPA backups antigos!
""")
    
    print("\n" + "="*70)
    print("💡 CONCLUSÃO")
    print("="*70)
    print("""
✅ O SISTEMA JÁ TEM CONTROLE DE BACKUPS!
  
• NÃO faz backups infinitos
• Mantém máximo 20 backups total (10+10)
• Auto-remove backups antigos
• Tamanho máximo controlado (~20MB)

⚠️ RECOMENDAÇÃO:
  NÃO EDITAR! O sistema já se auto-regula.
  Qualquer mudança pode quebrar o equilíbrio.
""")

if __name__ == "__main__":
    analyze_backup_system()
