"""
Ponte para backup_ops em tools/ com classe BackupManager.
Criado para compatibilidade com harness de verificação.
"""

import os
import sys
import json
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

# Adicionar tools ao path
tools_path = str(Path(__file__).parent.parent.parent / 'tools')
if tools_path not in sys.path:
    sys.path.insert(0, tools_path)

# Importar função de tools
from backup_ops import safe_snapshot


class BackupManager:
    """
    Gerenciador de backups com anti-recursão e validação.
    """
    
    def __init__(self, source_dir: str = '.', exclude_globs: Optional[List[str]] = None, settings: Optional[Dict] = None):
        """
        Inicializa o gerenciador de backup.
        
        Args:
            source_dir: Diretório fonte para backup
            exclude_globs: Lista de padrões a excluir
            settings: Configurações opcionais (para compatibilidade)
        """
        # Compatibilidade: se chamado só com dict (old style)
        if isinstance(source_dir, dict) and exclude_globs is None and settings is None:
            settings = source_dir
            source_dir = '.'
            
        self.settings = settings or {}
        self.source_dir = self.settings.get('source_dir', source_dir)
        self.backup_dir = Path(self.settings.get('backup_dir', 'backups'))
        self.backup_dir.mkdir(exist_ok=True)
        
        # Exclusões padrão
        default_excludes = [
            '*backup*', '*backups*', '*.venv*', '*__pycache__*',
            '*.mypy_cache*', '*.ruff_cache*', '*.pytest_cache*',
            '*.pyc', '*.pyo', '*.pyd', '.git/*', '.DS_Store'
        ]
        
        # Usar exclusões fornecidas ou defaults
        if exclude_globs is not None:
            self.exclude_globs = exclude_globs
        else:
            self.exclude_globs = default_excludes
            # Adicionar exclusões customizadas de settings
            custom_excludes = self.settings.get('exclude_globs', [])
            self.exclude_globs.extend(custom_excludes)
    
    def create_backup(self, description: str = 'backup') -> Dict[str, Any]:
        """
        Cria um novo backup.
        
        Args:
            description: Descrição do backup
            
        Returns:
            Dict com informações do backup
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{timestamp}-{description}.zip"
        backup_path = self.backup_dir / backup_name
        
        try:
            # Usar safe_snapshot de tools
            result = safe_snapshot(
                source_dir=self.source_dir,
                zip_path=str(backup_path),
                exclude_globs=self.exclude_globs
            )
            
            # Adicionar metadados
            result.update({
                'success': True,
                'timestamp': timestamp,
                'description': description,
                'path': str(backup_path),
                'size_mb': backup_path.stat().st_size / (1024 * 1024) if backup_path.exists() else 0
            })
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'path': str(backup_path)
            }
    
    def list_backups(self, pattern: Optional[str] = None) -> List[Dict]:
        """
        Lista backups existentes.
        
        Args:
            pattern: Padrão para filtrar backups
            
        Returns:
            Lista de dicionários com info dos backups
        """
        backups = []
        
        pattern = pattern or '*.zip'
        for backup_file in sorted(self.backup_dir.glob(pattern), reverse=True):
            backups.append({
                'name': backup_file.name,
                'path': str(backup_file),
                'size_mb': backup_file.stat().st_size / (1024 * 1024),
                'modified': datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat()
            })
        
        return backups
    
    def cleanup_old_backups(self, keep_last: int = 10, pattern: Optional[str] = None) -> Dict:
        """
        Remove backups antigos, mantendo apenas os N mais recentes.
        
        Args:
            keep_last: Número de backups a manter
            pattern: Padrão para filtrar
            
        Returns:
            Dict com resultado da limpeza
        """
        pattern = pattern or '*.zip'
        all_backups = sorted(self.backup_dir.glob(pattern), key=lambda f: f.stat().st_mtime, reverse=True)
        
        removed = []
        kept = []
        
        for i, backup in enumerate(all_backups):
            if i < keep_last:
                kept.append(backup.name)
            else:
                backup.unlink()
                removed.append(backup.name)
        
        return {
            'kept': kept,
            'removed': removed,
            'total_removed': len(removed)
        }
    
    def validate(self, zip_path: str) -> Dict:
        """
        Valida um arquivo de backup.
        
        Args:
            zip_path: Caminho do arquivo zip
            
        Returns:
            Dict com resultado da validação
        """
        zip_path = Path(zip_path)
        
        if not zip_path.exists():
            return {'valid': False, 'reason': 'File does not exist'}
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Verificar integridade
                bad_file = zf.testzip()
                if bad_file:
                    return {'valid': False, 'reason': f'Corrupt file: {bad_file}'}
                
                # Verificar que não contém backup/backups
                for name in zf.namelist():
                    if 'backup' in name.lower() or 'backups' in name.lower():
                        return {
                            'valid': False,
                            'reason': f'Contains backup path: {name}',
                            'warning': 'Potential recursion detected'
                        }
                
                # Verificar que não contém caches
                cache_patterns = ['__pycache__', '.venv', '.mypy_cache', '.ruff_cache', '.pytest_cache']
                for name in zf.namelist():
                    for pattern in cache_patterns:
                        if pattern in name:
                            return {
                                'valid': False,
                                'reason': f'Contains cache: {name}'
                            }
                
                return {
                    'valid': True,
                    'files': len(zf.namelist()),
                    'size_mb': zip_path.stat().st_size / (1024 * 1024)
                }
                
        except Exception as e:
            return {'valid': False, 'reason': str(e)}
    
    def get_memory_by_id(self, backup_id: str) -> Optional[Dict]:
        """
        Stub para compatibilidade - não usado em backups.
        """
        return None
    
    def snapshot(self, out_zip: str) -> Dict:
        """
        Cria snapshot usando safe_snapshot com anti-recursão.
        """
        try:
            result = safe_snapshot(
                source_dir=self.source_dir,
                zip_path=out_zip,
                exclude_globs=self.exclude_globs
            )
            return {
                'success': True,
                'path': out_zip,
                'files_count': result.get('files_count', 0),
                'size_mb': Path(out_zip).stat().st_size / (1024 * 1024) if Path(out_zip).exists() else 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'path': out_zip
            }
    
    def prune(self, dir_backups: str = None, keep: int = 10) -> Dict:
        """
        Alias para cleanup_old_backups - mantém N backups mais recentes.
        
        Args:
            dir_backups: Diretório de backups (usa self.backup_dir se None)
            keep: Número de backups a manter
            
        Returns:
            Dict com resultado da limpeza
        """
        if dir_backups:
            # Temporariamente mudar diretório de backups
            old_dir = self.backup_dir
            self.backup_dir = Path(dir_backups)
            result = self.cleanup_old_backups(keep_last=keep)
            self.backup_dir = old_dir
            return result
        else:
            return self.cleanup_old_backups(keep_last=keep)


# Exportar também safe_snapshot para compatibilidade
__all__ = ['BackupManager', 'safe_snapshot']