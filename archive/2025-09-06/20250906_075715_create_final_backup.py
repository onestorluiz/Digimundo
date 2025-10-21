#!/usr/bin/env python3
"""
Cria backup final V3.1
"""
import sys
import zipfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def create_final_backup():
    """Cria backup final V3.1"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backups/{timestamp}-v3_1_final.zip"
    
    backup_dir = Path(__file__).parent.parent.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    backup_path = backup_dir / f"{timestamp}-v3_1_final.zip"
    
    # Criar ZIP
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Adicionar arquivos importantes
        paths_to_backup = [
            'src/',
            'config/settings.yaml',
            'reports/fix_v3/',
            'tools/fix_v3/',
            'apps/scripturemon/'
        ]
        
        for path in paths_to_backup:
            base_path = Path(__file__).parent.parent.parent / path
            if base_path.exists():
                if base_path.is_file():
                    zf.write(base_path, path)
                else:
                    for file_path in base_path.rglob('*'):
                        if file_path.is_file():
                            # Pular arquivos de backup e cache
                            if 'backup' in str(file_path) or '__pycache__' in str(file_path):
                                continue
                            if file_path.suffix in ['.pyc', '.pyo']:
                                continue
                            
                            arcname = file_path.relative_to(Path(__file__).parent.parent.parent)
                            zf.write(file_path, arcname)
    
    print(f"Backup V3.1 criado: {backup_path}")
    return str(backup_path)

if __name__ == '__main__':
    create_final_backup()