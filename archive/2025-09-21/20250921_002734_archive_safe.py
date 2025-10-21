#!/usr/bin/env python3
"""
Arquivamento Seguro com Verificação
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Pastas para arquivar
SOURCES = [
    'scripturemon-champion',
    'scripturemon-champion-refactored_chatgpt', 
    'Respostas CHAT GPT',
    'Pre_Limpeza_Minimalista_Lixo',
    'Respostas_testes',
    'ollama_multi_system.py',
    'analyze_backups_digimunod.py'
]

ARCHIVE = Path('/Users/clubproducoes/Digimundo/Archive/backup-2025-09-21')

def archive_all():
    """Arquiva tudo em backup-2025-09-21"""
    
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    
    total = 0
    for source in SOURCES:
        source_path = Path('/Users/clubproducoes/Digimundo') / source
        
        if not source_path.exists():
            print(f"⚠️  {source} não existe")
            continue
            
        dest_path = ARCHIVE / source
        
        if source_path.is_file():
            # Arquivo individual
            print(f"📄 Copiando arquivo: {source}")
            shutil.copy2(source_path, dest_path)
            total += 1
        else:
            # Diretório
            print(f"📁 Arquivando pasta: {source}")
            if dest_path.exists():
                print(f"  Já existe, pulando...")
                continue
            shutil.copytree(source_path, dest_path, symlinks=True)
            files = sum(1 for _ in dest_path.rglob('*') if _.is_file())
            print(f"  ✅ {files} arquivos copiados")
            total += files
            
    print(f"\n🎯 TOTAL: {total} arquivos arquivados")
    print(f"📦 Local: {ARCHIVE}")
    
    # Verificação
    print("\n🔍 Verificando...")
    for source in SOURCES:
        source_path = Path('/Users/clubproducoes/Digimundo') / source
        dest_path = ARCHIVE / source
        
        if dest_path.exists():
            if dest_path.is_file():
                print(f"  ✅ {source} arquivado")
            else:
                files = sum(1 for _ in dest_path.rglob('*') if _.is_file())
                print(f"  ✅ {source}: {files} arquivos")
        else:
            print(f"  ❌ {source} FALTANDO!")
            
    return True

def cleanup():
    """Remove originais após backup verificado"""
    
    print("\n🗑️ Removendo originais...")
    
    for source in SOURCES:
        source_path = Path('/Users/clubproducoes/Digimundo') / source
        
        if not source_path.exists():
            continue
            
        backup_path = ARCHIVE / source
        if not backup_path.exists():
            print(f"❌ {source} não tem backup! Pulando...")
            continue
            
        if source_path.is_file():
            source_path.unlink()
            print(f"  🗑️ Removido: {source}")
        else:
            shutil.rmtree(source_path)
            print(f"  🗑️ Removido: {source}/")
            
    print("\n✅ Limpeza concluída!")

if __name__ == "__main__":
    import sys
    
    if '--cleanup' in sys.argv:
        cleanup()
    else:
        archive_all()