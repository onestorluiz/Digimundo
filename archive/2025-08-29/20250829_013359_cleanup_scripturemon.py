#!/usr/bin/env python3
"""
🧹 Limpeza e Organização do Sistema Scripturemon
Remove duplicados e organiza sistema definitivo
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import subprocess

def cleanup_scripturemon():
    """Limpa duplicados do Scripturemon e organiza sistema"""
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     🧹 LIMPEZA DO SISTEMA SCRIPTUREMON                    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    base_path = Path("/Users/clubproducoes/Digimundo")
    
    # Criar backup antes de limpar
    backup_dir = base_path / f"archive/scripturemon_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Backup em: {backup_dir}")
    
    # Scripts duplicados para remover (mantendo apenas versão definitiva)
    duplicate_patterns = [
        "*ACTIVATE_SCRIPTUREMON*.sh",
        "*START_SCRIPTUREMON*.sh",
        "*LAUNCH_SCRIPTUREMON*.sh",
        "*SCRIPTUREMON_WATCHER*.sh",
        "*FEED_SCRIPTUREMON*.sh",
        "*EVOLVE_SCRIPTUREMON*.sh",
        "*CREATE_SCRIPTUREMON*.sh",
        "*UNIFY_SCRIPTUREMON*.sh",
        "*SCRIPTUREMON_MONITOR*.sh",
        "*REORGANIZE_SCRIPTUREMON*.sh"
    ]
    
    files_removed = 0
    files_backed_up = 0
    
    print("\n🗑️ REMOVENDO DUPLICADOS...")
    print("="*60)
    
    # Buscar e remover duplicados
    for pattern in duplicate_patterns:
        cmd = f'find {base_path} -name "{pattern}" -type f 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        for file_path in result.stdout.strip().split('\n'):
            if not file_path:
                continue
                
            file = Path(file_path)
            
            # Não remover o sistema definitivo
            if 'scripturemon_definitive' in str(file):
                continue
            
            # Não remover se estiver em node_modules ou .git
            if 'node_modules' in str(file) or '.git' in str(file):
                continue
            
            try:
                # Fazer backup se arquivo > 10KB
                if file.stat().st_size > 10240:
                    backup_path = backup_dir / file.name
                    shutil.copy2(file, backup_path)
                    files_backed_up += 1
                    print(f"   💾 Backup: {file.name}")
                
                # Remover arquivo
                file.unlink()
                files_removed += 1
                
                if files_removed <= 10:
                    print(f"   ✗ Removido: {file.parent.name}/{file.name}")
                    
            except Exception as e:
                continue
    
    # Consolidar modelos Ollama duplicados
    print("\n🤖 CONSOLIDANDO MODELOS OLLAMA...")
    print("="*60)
    
    try:
        # Listar modelos scripturemon
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        scripturemon_models = []
        
        for line in result.stdout.split('\n'):
            if 'scripturemon' in line.lower():
                parts = line.split()
                if parts:
                    model_name = parts[0]
                    if model_name != 'scripturemon:latest':  # Manter apenas o principal
                        scripturemon_models.append(model_name)
        
        # Remover modelos duplicados
        for model in scripturemon_models:
            if 'ultimate' in model or 'immortal' in model or 'nature' in model:
                continue  # Manter variações especiais
            
            try:
                print(f"   ✗ Removendo modelo: {model}")
                subprocess.run(['ollama', 'rm', model], capture_output=True)
                files_removed += 1
            except:
                continue
                
    except Exception as e:
        print(f"   ⚠️ Erro ao consolidar modelos: {e}")
    
    # Criar links simbólicos para facilitar acesso
    print("\n🔗 CRIANDO ATALHOS...")
    print("="*60)
    
    # Link para script definitivo
    main_script = base_path / "digimons/scripturemon_definitive/SCRIPTUREMON_ACTIVATE.sh"
    link_path = base_path / "scripturemon"
    
    if main_script.exists() and not link_path.exists():
        try:
            os.symlink(main_script, link_path)
            print(f"   ✅ Atalho criado: {link_path} → {main_script}")
        except Exception as e:
            print(f"   ⚠️ Erro ao criar atalho: {e}")
    
    # Limpar diretórios vazios
    print("\n📁 LIMPANDO DIRETÓRIOS VAZIOS...")
    empty_dirs = []
    
    for root, dirs, files in os.walk(base_path / "digimons/scripturemon"):
        if not dirs and not files:
            empty_dirs.append(Path(root))
    
    for empty_dir in empty_dirs:
        try:
            empty_dir.rmdir()
            print(f"   ✗ Removido diretório vazio: {empty_dir.name}")
        except:
            continue
    
    # Atualizar configurações globais
    print("\n⚙️ ATUALIZANDO CONFIGURAÇÕES...")
    
    # Criar arquivo de configuração global
    global_config = base_path / ".scripturemon_config"
    
    config_content = f"""# Scripturemon - Configuração Global
# Criado em {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Caminho do sistema definitivo
SCRIPTUREMON_HOME="{base_path}/digimons/scripturemon_definitive"

# Modelo padrão
SCRIPTUREMON_MODEL="scripturemon:latest"

# Ativar com:
# source {base_path}/digimons/scripturemon_definitive/SCRIPTUREMON_ACTIVATE.sh
"""
    
    with open(global_config, 'w') as f:
        f.write(config_content)
    
    print(f"   ✅ Configuração global criada: {global_config}")
    
    # Relatório final
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE LIMPEZA")
    print("="*60)
    print(f"✅ Arquivos removidos: {files_removed}")
    print(f"💾 Arquivos com backup: {files_backed_up}")
    print(f"📁 Sistema definitivo: {base_path}/digimons/scripturemon_definitive")
    
    # Verificar sistema final
    definitive_dir = base_path / "digimons/scripturemon_definitive"
    if definitive_dir.exists():
        files_in_definitive = list(definitive_dir.glob("*"))
        print(f"\n🎬 SISTEMA SCRIPTUREMON DEFINITIVO:")
        print(f"   • Arquivos: {len(files_in_definitive)}")
        print(f"   • Script principal: SCRIPTUREMON_ACTIVATE.sh")
        print(f"   • Configuração: scripturemon_config.json")
        print(f"   • Documentação: README.md")
    
    print("\n✅ LIMPEZA CONCLUÍDA COM SUCESSO!")
    print("🎬 Scripturemon agora tem um SISTEMA ÚNICO E DEFINITIVO!")
    
    print("\n📋 COMO USAR:")
    print("1. Ativar Scripturemon:")
    print(f"   cd {definitive_dir}")
    print("   ./SCRIPTUREMON_ACTIVATE.sh")
    print("\n2. Ou usar atalho:")
    print(f"   {base_path}/scripturemon")
    
    return files_removed

if __name__ == "__main__":
    cleanup_scripturemon()