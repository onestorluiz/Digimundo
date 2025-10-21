#!/usr/bin/env python3
"""
Diff Summary - Compara estado atual com inventário da FASE_00.
Identifica arquivos alterados, adicionados e removidos.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple


def load_phase_00_inventory() -> Dict:
    """
    Carrega inventário da FASE_00.
    
    Returns:
        Dicionário com inventário inicial
    """
    inventory_path = Path(__file__).parent.parent / 'reports' / 'repair' / 'phase_00_inventory.json'
    
    if not inventory_path.exists():
        print(f"⚠️ Inventário FASE_00 não encontrado: {inventory_path}")
        return {'python_files': {'files': []}, 'db_files': {'files': []}}
    
    with open(inventory_path, 'r') as f:
        data = json.load(f)
        # Converter formato se necessário
        if 'python_files' in data and isinstance(data['python_files'], dict):
            return {
                'python_files': data['python_files'].get('files', []),
                'db_files': data.get('db_files', {}).get('files', [])
            }
        return data


def get_current_inventory() -> Dict:
    """
    Gera inventário atual do projeto.
    
    Returns:
        Dicionário com inventário atual
    """
    base_dir = Path(__file__).parent.parent
    
    # Coletar arquivos Python
    python_files = []
    for py_file in base_dir.rglob('*.py'):
        if not any(part.startswith('.') for part in py_file.parts):
            rel_path = str(py_file.relative_to(base_dir))
            if 'venv' not in rel_path and '__pycache__' not in rel_path:
                python_files.append({
                    'path': rel_path,
                    'size': py_file.stat().st_size,
                    'modified': datetime.fromtimestamp(py_file.stat().st_mtime).isoformat()
                })
    
    # Coletar arquivos DB
    db_files = []
    for db_file in base_dir.rglob('*.db'):
        if not any(part.startswith('.') for part in db_file.parts):
            rel_path = str(db_file.relative_to(base_dir))
            db_files.append({
                'path': rel_path,
                'size': db_file.stat().st_size,
                'modified': datetime.fromtimestamp(db_file.stat().st_mtime).isoformat()
            })
    
    return {
        'python_files': python_files,
        'db_files': db_files,
        'timestamp': datetime.now().isoformat()
    }


def compare_inventories(old_inventory: Dict, new_inventory: Dict) -> Dict:
    """
    Compara dois inventários e identifica mudanças.
    
    Args:
        old_inventory: Inventário inicial (FASE_00)
        new_inventory: Inventário atual
        
    Returns:
        Dicionário com diferenças
    """
    # Normalizar paths - usar relative_path do FASE_00
    old_py_files = old_inventory.get('python_files', [])
    if old_py_files:
        old_py_paths = {f.get('relative_path', f.get('path', '')) for f in old_py_files}
    else:
        old_py_paths = set()
        
    new_py_paths = {f['path'] for f in new_inventory.get('python_files', [])}
    
    old_db_files = old_inventory.get('db_files', [])
    if old_db_files:
        old_db_paths = {f.get('relative_path', f.get('path', '')) for f in old_db_files}
    else:
        old_db_paths = set()
        
    new_db_paths = {f['path'] for f in new_inventory.get('db_files', [])}
    
    # Calcular diferenças
    py_added = new_py_paths - old_py_paths
    py_removed = old_py_paths - new_py_paths
    py_common = old_py_paths & new_py_paths
    
    db_added = new_db_paths - old_db_paths
    db_removed = old_db_paths - new_db_paths
    db_common = old_db_paths & new_db_paths
    
    # Identificar modificados (comparar tamanho)
    py_modified = []
    for path in py_common:
        # Buscar arquivo no inventário antigo
        old_file = None
        for f in old_py_files:
            if f.get('relative_path', f.get('path', '')) == path:
                old_file = f
                break
                
        # Buscar arquivo no inventário novo
        new_file = next((f for f in new_inventory['python_files'] if f['path'] == path), None)
        
        if old_file and new_file and old_file.get('size', 0) != new_file.get('size', 0):
            py_modified.append({
                'path': path,
                'old_size': old_file.get('size', 0),
                'new_size': new_file.get('size', 0),
                'size_diff': new_file.get('size', 0) - old_file.get('size', 0)
            })
    
    return {
        'python': {
            'added': sorted(list(py_added)),
            'removed': sorted(list(py_removed)),
            'modified': sorted(py_modified, key=lambda x: x['path']),
            'unchanged': len(py_common) - len(py_modified)
        },
        'database': {
            'added': sorted(list(db_added)),
            'removed': sorted(list(db_removed)),
            'total': len(new_db_paths)
        },
        'summary': {
            'total_py_before': len(old_py_paths),
            'total_py_after': len(new_py_paths),
            'total_db_before': len(old_db_paths),
            'total_db_after': len(new_db_paths)
        }
    }


def generate_diff_markdown(diff: Dict) -> str:
    """
    Gera relatório Markdown das diferenças.
    
    Args:
        diff: Dicionário de diferenças
        
    Returns:
        String Markdown
    """
    md = []
    md.append("# Diferenças desde FASE_00\n")
    md.append(f"**Gerado em:** {datetime.now().isoformat()}\n")
    
    # Resumo
    md.append("## Resumo\n")
    summary = diff['summary']
    md.append(f"- **Arquivos Python antes:** {summary['total_py_before']}")
    md.append(f"- **Arquivos Python depois:** {summary['total_py_after']}")
    md.append(f"- **Arquivos DB antes:** {summary['total_db_before']}")
    md.append(f"- **Arquivos DB depois:** {summary['total_db_after']}\n")
    
    # Python Files
    md.append("## Arquivos Python\n")
    
    py_diff = diff['python']
    md.append(f"### Adicionados ({len(py_diff['added'])})\n")
    if py_diff['added']:
        for path in py_diff['added']:
            md.append(f"- `{path}`")
    else:
        md.append("*Nenhum arquivo adicionado*")
    
    md.append(f"\n### Modificados ({len(py_diff['modified'])})\n")
    if py_diff['modified']:
        for item in py_diff['modified']:
            size_change = f"+{item['size_diff']}" if item['size_diff'] > 0 else str(item['size_diff'])
            md.append(f"- `{item['path']}` ({size_change} bytes)")
    else:
        md.append("*Nenhum arquivo modificado*")
    
    md.append(f"\n### Removidos ({len(py_diff['removed'])})\n")
    if py_diff['removed']:
        for path in py_diff['removed']:
            md.append(f"- `{path}`")
    else:
        md.append("*Nenhum arquivo removido*")
    
    md.append(f"\n### Inalterados: {py_diff['unchanged']} arquivos\n")
    
    # Database Files
    md.append("## Arquivos de Banco de Dados\n")
    
    db_diff = diff['database']
    md.append(f"### Adicionados ({len(db_diff['added'])})\n")
    if db_diff['added']:
        for path in db_diff['added']:
            md.append(f"- `{path}`")
    else:
        md.append("*Nenhum banco adicionado*")
    
    md.append(f"\n### Removidos ({len(db_diff['removed'])})\n")
    if db_diff['removed']:
        for path in db_diff['removed']:
            md.append(f"- `{path}`")
    else:
        md.append("*Nenhum banco removido*")
    
    # Estatísticas
    md.append("\n## Estatísticas\n")
    
    total_added = len(py_diff['added']) + len(db_diff['added'])
    total_modified = len(py_diff['modified'])
    total_removed = len(py_diff['removed']) + len(db_diff['removed'])
    
    md.append(f"- **Total de arquivos adicionados:** {total_added}")
    md.append(f"- **Total de arquivos modificados:** {total_modified}")
    md.append(f"- **Total de arquivos removidos:** {total_removed}")
    md.append(f"- **Mudança líquida em arquivos Python:** {len(py_diff['added']) - len(py_diff['removed'])}")
    
    return '\n'.join(md)


def main():
    """Executa comparação e gera relatórios."""
    print("=" * 60)
    print("DIFF SUMMARY - Comparando com FASE_00")
    print("=" * 60)
    
    # Carregar inventários
    print("\n1. Carregando inventário FASE_00...")
    old_inventory = load_phase_00_inventory()
    
    print("2. Gerando inventário atual...")
    new_inventory = get_current_inventory()
    
    # Comparar
    print("3. Comparando inventários...")
    diff = compare_inventories(old_inventory, new_inventory)
    
    # Salvar diff JSON
    diff_json_path = Path(__file__).parent.parent / 'reports' / 'repair' / 'final_diff.json'
    with open(diff_json_path, 'w') as f:
        json.dump(diff, f, indent=2)
    print(f"\n✅ Diff JSON salvo: {diff_json_path}")
    
    # Gerar e salvar Markdown
    markdown = generate_diff_markdown(diff)
    diff_md_path = Path(__file__).parent.parent / 'reports' / 'repair' / 'final_diff.md'
    with open(diff_md_path, 'w') as f:
        f.write(markdown)
    print(f"✅ Diff Markdown salvo: {diff_md_path}")
    
    # Mostrar resumo
    print("\n" + "=" * 60)
    print("RESUMO DAS MUDANÇAS")
    print("=" * 60)
    print(f"Arquivos Python:")
    print(f"  - Adicionados: {len(diff['python']['added'])}")
    print(f"  - Modificados: {len(diff['python']['modified'])}")
    print(f"  - Removidos: {len(diff['python']['removed'])}")
    print(f"  - Inalterados: {diff['python']['unchanged']}")
    print(f"\nArquivos DB:")
    print(f"  - Adicionados: {len(diff['database']['added'])}")
    print(f"  - Removidos: {len(diff['database']['removed'])}")
    
    return diff


if __name__ == "__main__":
    main()