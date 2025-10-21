#!/usr/bin/env python3
import os
import json
from datetime import datetime
import hashlib

def get_file_hash(filepath):
    """Calcula hash MD5 do arquivo"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    except:
        return "error"

def scan_files(root_dir):
    """Escaneia todos os arquivos .py e .db"""
    inventory = {
        "timestamp": datetime.now().isoformat(),
        "root_directory": os.path.abspath(root_dir),
        "statistics": {
            "total_py_files": 0,
            "total_db_files": 0,
            "total_size_bytes": 0,
            "by_directory": {}
        },
        "files": {
            "python": [],
            "database": []
        }
    }
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignorar diretórios desnecessários
        if any(skip in dirpath for skip in ['.venv', '__pycache__', '.git', 'node_modules']):
            continue
            
        rel_dir = os.path.relpath(dirpath, root_dir)
        
        for filename in filenames:
            if filename.endswith('.py') or filename.endswith('.db'):
                filepath = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(filepath, root_dir)
                
                try:
                    size = os.path.getsize(filepath)
                    inventory["statistics"]["total_size_bytes"] += size
                    
                    file_info = {
                        "path": rel_path,
                        "size": size,
                        "hash": get_file_hash(filepath)
                    }
                    
                    if filename.endswith('.py'):
                        inventory["files"]["python"].append(file_info)
                        inventory["statistics"]["total_py_files"] += 1
                    else:
                        inventory["files"]["database"].append(file_info)
                        inventory["statistics"]["total_db_files"] += 1
                    
                    # Estatísticas por diretório
                    dir_key = rel_dir if rel_dir != '.' else 'root'
                    if dir_key not in inventory["statistics"]["by_directory"]:
                        inventory["statistics"]["by_directory"][dir_key] = {"py": 0, "db": 0}
                    
                    if filename.endswith('.py'):
                        inventory["statistics"]["by_directory"][dir_key]["py"] += 1
                    else:
                        inventory["statistics"]["by_directory"][dir_key]["db"] += 1
                        
                except Exception as e:
                    print(f"Erro ao processar {filepath}: {e}")
    
    return inventory

def generate_markdown(inventory):
    """Gera relatório em Markdown"""
    md = []
    md.append("# Inventário de Arquivos - Scripturemon")
    md.append(f"\n**Data/Hora:** {inventory['timestamp']}")
    md.append(f"**Diretório Raiz:** `{inventory['root_directory']}`")
    md.append("\n## Estatísticas Gerais\n")
    md.append(f"- **Total de arquivos .py:** {inventory['statistics']['total_py_files']}")
    md.append(f"- **Total de arquivos .db:** {inventory['statistics']['total_db_files']}")
    md.append(f"- **Total geral:** {inventory['statistics']['total_py_files'] + inventory['statistics']['total_db_files']}")
    md.append(f"- **Tamanho total:** {inventory['statistics']['total_size_bytes'] / (1024*1024):.2f} MB")
    
    md.append("\n## Distribuição por Diretório\n")
    md.append("| Diretório | Arquivos .py | Arquivos .db |")
    md.append("|-----------|-------------|-------------|")
    
    for dir_name, counts in sorted(inventory["statistics"]["by_directory"].items()):
        md.append(f"| {dir_name} | {counts['py']} | {counts['db']} |")
    
    md.append("\n## Principais Arquivos Python (Top 20 por tamanho)\n")
    top_py = sorted(inventory["files"]["python"], key=lambda x: x["size"], reverse=True)[:20]
    for file in top_py:
        md.append(f"- `{file['path']}` ({file['size'] / 1024:.1f} KB) [hash: {file['hash']}]")
    
    if inventory["files"]["database"]:
        md.append("\n## Arquivos de Banco de Dados\n")
        for file in inventory["files"]["database"]:
            md.append(f"- `{file['path']}` ({file['size'] / 1024:.1f} KB) [hash: {file['hash']}]")
    
    return "\n".join(md)

if __name__ == "__main__":
    print("Gerando inventário de arquivos...")
    inventory = scan_files(".")
    
    # Salvar JSON
    with open("reports/harmony_vFinal/phase0_inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Salvar Markdown
    markdown = generate_markdown(inventory)
    with open("reports/harmony_vFinal/phase0_inventory.md", "w") as f:
        f.write(markdown)
    
    print(f"✅ Inventário gerado com sucesso!")
    print(f"   - Total de arquivos .py: {inventory['statistics']['total_py_files']}")
    print(f"   - Total de arquivos .db: {inventory['statistics']['total_db_files']}")
