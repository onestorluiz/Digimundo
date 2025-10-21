#!/usr/bin/env python3
"""Cria backup v32_post com anti-recursão"""
import zipfile
from pathlib import Path
from datetime import datetime

def create_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(f'backups/{timestamp}-v32_post.zip')
    
    exclude_patterns = ['backup', 'backups', '.venv', '__pycache__', '.mypy_cache', '.ruff_cache', '.pytest_cache']
    
    file_count = 0
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in Path('.').rglob('*'):
            if path.is_file():
                # Check exclusions
                path_str = str(path)
                if any(pattern in path_str for pattern in exclude_patterns):
                    continue
                if path.suffix in ['.pyc', '.pyo']:
                    continue
                    
                zf.write(path, path.relative_to('.'))
                file_count += 1
    
    size_mb = backup_path.stat().st_size / (1024*1024)
    print(f"Backup criado: {backup_path}")
    print(f"Arquivos: {file_count}, Tamanho: {size_mb:.2f}MB")
    return str(backup_path), size_mb, file_count

if __name__ == '__main__':
    path, size, count = create_backup()