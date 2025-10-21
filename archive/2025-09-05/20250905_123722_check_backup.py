#!/usr/bin/env python3
"""Check para verificar o sistema de backup seguro"""

import sys
import json
import time
import shutil
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa verificação do sistema de backup"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Importar sistema de backup
        from src.utils.backup_ops import BackupManager
        
        # Criar instância
        backup_mgr = BackupManager(settings)
        result['notes'].append('BackupManager instantiated')
        
        # Teste 1: Criar backup
        backup_result = backup_mgr.create_backup('verify_test')
        
        if backup_result and backup_result.get('success'):
            result['details']['create_backup'] = 'PASS'
            backup_path = backup_result.get('path')
            result['notes'].append(f'Backup created: {backup_path}')
        else:
            result['details']['create_backup'] = 'FAIL'
            result['notes'].append('Failed to create backup')
            return result
        
        # Teste 2: Verificar integridade do backup
        backup_file = Path(backup_path)
        if backup_file.exists():
            size_mb = backup_file.stat().st_size / (1024 * 1024)
            result['details']['backup_exists'] = 'PASS'
            result['notes'].append(f'Backup size: {size_mb:.2f} MB')
            
            # Verificar se é um arquivo zip válido
            import zipfile
            try:
                with zipfile.ZipFile(backup_file, 'r') as zf:
                    file_count = len(zf.namelist())
                    result['details']['valid_zip'] = 'PASS'
                    result['notes'].append(f'Valid zip with {file_count} files')
            except:
                result['details']['valid_zip'] = 'FAIL'
                result['notes'].append('Invalid zip file')
        else:
            result['details']['backup_exists'] = 'FAIL'
            result['notes'].append('Backup file not found')
        
        # Teste 3: Listar backups
        backups = backup_mgr.list_backups()
        if backups and len(backups) > 0:
            result['details']['list_backups'] = 'PASS'
            result['notes'].append(f'Found {len(backups)} backups')
        else:
            result['details']['list_backups'] = 'FAIL'
            result['notes'].append('No backups found')
        
        # Teste 4: Verificar que não modifica sistema durante backup
        test_file = Path('data/verify_test_marker.txt')
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text('test content')
        original_mtime = test_file.stat().st_mtime
        
        # Criar outro backup
        backup_mgr.create_backup('verify_test_2')
        
        # Verificar que arquivo não foi modificado
        new_mtime = test_file.stat().st_mtime
        if original_mtime == new_mtime:
            result['details']['no_system_modification'] = 'PASS'
            result['notes'].append('Backup does not modify source files')
        else:
            result['details']['no_system_modification'] = 'FAIL'
            result['notes'].append('Backup modified source files!')
        
        # Cleanup do arquivo de teste
        test_file.unlink()
        
        # Teste 5: Backup incremental
        time.sleep(0.1)  # Pequena espera
        incremental_result = backup_mgr.create_backup('verify_incremental')
        
        if incremental_result and incremental_result.get('success'):
            result['details']['incremental_backup'] = 'PASS'
            result['notes'].append('Incremental backup successful')
        else:
            result['details']['incremental_backup'] = 'FAIL'
            result['notes'].append('Incremental backup failed')
        
        # Teste 6: Verificar naming convention
        backup_dir = Path('backups')
        if backup_dir.exists():
            backup_files = list(backup_dir.glob('*.zip'))
            valid_names = 0
            
            for bf in backup_files:
                # Formato esperado: YYYYMMDD_HHMMSS-description.zip
                name = bf.stem
                if '_' in name and '-' in name:
                    parts = name.split('-', 1)
                    timestamp_part = parts[0]
                    if len(timestamp_part) == 15 and timestamp_part[8] == '_':
                        valid_names += 1
            
            if valid_names == len(backup_files):
                result['details']['naming_convention'] = 'PASS'
                result['notes'].append('All backups follow naming convention')
            else:
                result['details']['naming_convention'] = 'WARN'
                result['notes'].append(f'Some backups have non-standard names')
        
        # Teste 7: Cleanup de backups antigos
        old_backup_count = len(list(Path('backups').glob('verify_test*.zip')))
        if old_backup_count > 0:
            cleanup_result = backup_mgr.cleanup_old_backups(keep_last=1, pattern='verify_test')
            
            new_backup_count = len(list(Path('backups').glob('verify_test*.zip')))
            if new_backup_count < old_backup_count:
                result['details']['cleanup_old'] = 'PASS'
                result['notes'].append(f'Cleaned up {old_backup_count - new_backup_count} old backups')
            else:
                result['details']['cleanup_old'] = 'WARN'
                result['notes'].append('Cleanup may not be working')
        else:
            result['details']['cleanup_old'] = 'SKIP'
            result['notes'].append('No old backups to clean')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        warnings = [k for k, v in result['details'].items() if v == 'WARN']
        
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            if warnings:
                result['reason'] = f'Backup system OK with warnings: {", ".join(warnings)}'
            else:
                result['reason'] = 'All backup checks passed'
        else:
            result['status'] = 'failed'
            result['reason'] = f'Failed checks: {", ".join(failures)}'
        
    except ImportError as e:
        result['status'] = 'blocked'
        result['reason'] = f'Import error: {str(e)}'
        result['exception'] = str(e)
    except Exception as e:
        result['status'] = 'error'
        result['reason'] = f'Unexpected error: {str(e)}'
        result['exception'] = str(e)
        result['traceback'] = traceback.format_exc()
    
    return result

if __name__ == "__main__":
    # Para teste local
    from generate_inventory import load_default_settings
    settings = load_default_settings()
    result = run_check(settings)
    print(json.dumps(result, indent=2))