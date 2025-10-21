#!/usr/bin/env python3
"""
EXECUTE DENSE REORGANIZATION
Executa a reorganização densa baseada na análise profunda
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
import os

def execute_reorganization():
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
    
    # Carrega o relatório mais recente
    report_files = list(base_path.glob('deep_analysis_report_*.json'))
    if not report_files:
        print("❌ Nenhum relatório de análise encontrado")
        return
    
    latest_report = max(report_files, key=lambda p: p.stat().st_mtime)
    print(f"📊 Usando relatório: {latest_report.name}")
    
    with open(latest_report, 'r') as f:
        report = json.load(f)
    
    reorganization_plan = report.get('reorganization_plan', {})
    
    print("\n" + "="*60)
    print("🚀 EXECUTANDO REORGANIZAÇÃO DENSA")
    print("="*60)
    
    # 1. Move arquivos para locais corretos
    to_move = reorganization_plan.get('to_move', [])
    moved_count = 0
    
    print(f"\n📦 Movendo {len(to_move)} arquivos...")
    for move_item in to_move:
        src = base_path / move_item['from']
        dst = base_path / move_item['to']
        
        if src.exists():
            try:
                # Cria diretório destino se necessário
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                print(f"✓ Movido: {move_item['from']} → {move_item['to']}")
                moved_count += 1
            except Exception as e:
                print(f"✗ Erro ao mover {move_item['from']}: {e}")
        else:
            print(f"⚠️ Arquivo não encontrado: {move_item['from']}")
    
    # 2. Arquiva arquivos obsoletos
    to_archive = reorganization_plan.get('to_archive', [])
    archived_count = 0
    
    if to_archive:
        print(f"\n🗄️ Arquivando {len(to_archive)} arquivos obsoletos...")
        archive_dir = base_path / 'archive' / 'obsolete' / datetime.now().strftime('%Y%m%d')
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        for archive_item in to_archive:
            src = base_path / archive_item['file']
            if src.exists():
                try:
                    dst = archive_dir / src.name
                    shutil.move(str(src), str(dst))
                    print(f"✓ Arquivado: {archive_item['file']} ({archive_item['reason']})")
                    archived_count += 1
                except Exception as e:
                    print(f"✗ Erro ao arquivar {archive_item['file']}: {e}")
    
    # 3. Move para lixeira arquivos inúteis
    to_delete = reorganization_plan.get('to_delete', [])
    deleted_count = 0
    
    if to_delete:
        print(f"\n🗑️ Movendo {len(to_delete)} arquivos para lixeira...")
        trash_dir = base_path / 'trash' / datetime.now().strftime('%Y%m%d_%H%M%S')
        trash_dir.mkdir(parents=True, exist_ok=True)
        
        for delete_item in to_delete:
            src = base_path / delete_item['file']
            if src.exists():
                try:
                    dst = trash_dir / src.name
                    shutil.move(str(src), str(dst))
                    print(f"✓ Lixeira: {delete_item['file']} ({delete_item['reason']})")
                    deleted_count += 1
                except Exception as e:
                    print(f"✗ Erro ao mover para lixeira {delete_item['file']}: {e}")
    
    # 4. Resumo final
    print("\n" + "="*60)
    print("✅ REORGANIZAÇÃO CONCLUÍDA")
    print("="*60)
    print(f"📦 Arquivos movidos: {moved_count}/{len(to_move)}")
    print(f"🗄️ Arquivos arquivados: {archived_count}/{len(to_archive)}")
    print(f"🗑️ Arquivos na lixeira: {deleted_count}/{len(to_delete)}")
    
    # 5. Salva log da reorganização
    log_file = base_path / f'reorganization_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(log_file, 'w') as f:
        f.write(f"Reorganização executada em {datetime.now().isoformat()}\n")
        f.write(f"Arquivos movidos: {moved_count}\n")
        f.write(f"Arquivos arquivados: {archived_count}\n")
        f.write(f"Arquivos na lixeira: {deleted_count}\n")
    
    print(f"\n📝 Log salvo em: {log_file.name}")
    
    return {
        'moved': moved_count,
        'archived': archived_count,
        'deleted': deleted_count
    }

if __name__ == "__main__":
    execute_reorganization()