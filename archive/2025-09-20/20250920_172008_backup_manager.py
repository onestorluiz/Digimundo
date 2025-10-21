"""
BACKUP MANAGER - Phase 4
Simple backup management with rotation policy (keep last 3)
"""

import os
import json
import zipfile
import threading
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Global lock to prevent concurrent backups
_BACKUP_LOCK = threading.Lock()

# Exclusion patterns
EXCLUSIONS = [
    'backups/',
    '.git/',
    '__pycache__/',
    '.venv/',
    'data/chroma/',
    'data/tpd/',
    'data/screenplay_synth/',
    'data/cinema_knowledge/',
    'reports/',
    'TESTES/',
    'RESULTADOS_TESTES/',
    '*.old',
    '*.pyc',
    '.DS_Store',
    '*.log',
    '.pytest_cache/',
    '.mypy_cache/',
    'node_modules/',
    'dist/',
    'build/',
    '*.egg-info',
    '*.tar.gz',
    '*.zip',
    '*.pdf',
    'BACKUP_*'
]

class BackupManager:
    """Simple backup manager with rotation policy"""
    
    def __init__(self, backup_dir: str = "backups", max_backups: int = 3):
        """
        Initialize backup manager
        
        Args:
            backup_dir: Directory to store backups
            max_backups: Maximum number of backups to keep (default: 3)
        """
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self, prefix: str = "scripturemon") -> Optional[Path]:
        """
        Create a new backup with exclusions
        
        Args:
            prefix: Prefix for backup filename
            
        Returns:
            Path to created backup or None if failed
        """
        with _BACKUP_LOCK:
            try:
                # Generate timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{prefix}_{timestamp}.zip"
                backup_path = self.backup_dir / backup_name
                
                logger.info(f"Creating backup: {backup_path}")
                
                # Create zip file
                with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    # Walk through all files
                    for root, dirs, files in os.walk('.'):
                        # Skip excluded directories
                        dirs[:] = [d for d in dirs if not self._should_exclude(os.path.join(root, d))]
                        
                        for file in files:
                            file_path = os.path.join(root, file)
                            
                            # Skip excluded files
                            if self._should_exclude(file_path):
                                continue
                            
                            # Skip large files over 10MB
                            try:
                                if os.path.getsize(file_path) > 10 * 1024 * 1024:
                                    continue
                            except:
                                pass
                            
                            # Add to zip with relative path
                            try:
                                arcname = os.path.relpath(file_path, '.')
                                zf.write(file_path, arcname)
                            except Exception as e:
                                pass  # Skip files we can't read
                
                # Get file size
                size_mb = backup_path.stat().st_size / (1024 * 1024)
                logger.info(f"✅ Backup created: {backup_path} ({size_mb:.1f} MB)")
                
                # Rotate backups
                self.rotate_backups()
                
                return backup_path
                
            except Exception as e:
                logger.error(f"Failed to create backup: {e}")
                return None
    
    def _should_exclude(self, path: str) -> bool:
        """
        Check if path should be excluded from backup
        
        Args:
            path: Path to check
            
        Returns:
            True if should be excluded
        """
        # Normalize path
        path = path.replace('\\', '/')
        
        # Check each exclusion pattern
        for pattern in EXCLUSIONS:
            # Handle directory patterns
            if pattern.endswith('/'):
                if path.startswith(pattern) or f"/{pattern}" in path or path.endswith(pattern[:-1]):
                    return True
            # Handle wildcards
            elif '*' in pattern:
                import fnmatch
                if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                    return True
            # Handle exact matches
            elif pattern in path:
                return True
        
        return False
    
    def rotate_backups(self) -> List[Path]:
        """
        Rotate backups keeping only the most recent ones
        
        Returns:
            List of deleted backup paths
        """
        deleted = []
        
        try:
            # Get all zip files in backup directory
            backups = sorted(
                [f for f in self.backup_dir.glob("*.zip")],
                key=lambda x: x.stat().st_mtime,
                reverse=True  # Most recent first
            )
            
            # Keep only max_backups
            if len(backups) > self.max_backups:
                for old_backup in backups[self.max_backups:]:
                    logger.info(f"Deleting old backup: {old_backup}")
                    old_backup.unlink()
                    deleted.append(old_backup)
                    
            logger.info(f"Backup rotation complete. Kept {min(len(backups), self.max_backups)} backups")
            
        except Exception as e:
            logger.error(f"Failed to rotate backups: {e}")
        
        return deleted
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        List all backups with metadata
        
        Returns:
            List of backup info dicts
        """
        backups = []
        
        try:
            for backup_file in sorted(self.backup_dir.glob("*.zip")):
                stat = backup_file.stat()
                backups.append({
                    "name": backup_file.name,
                    "path": str(backup_file),
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "age_hours": round((datetime.now().timestamp() - stat.st_mtime) / 3600, 1)
                })
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x["created"], reverse=True)
        
        return backups
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get backup system status
        
        Returns:
            Status dictionary
        """
        backups = self.list_backups()
        total_size = sum(b["size_mb"] for b in backups)
        
        return {
            "backup_dir": str(self.backup_dir),
            "max_backups": self.max_backups,
            "current_backups": len(backups),
            "total_size_mb": round(total_size, 2),
            "oldest_backup": backups[-1]["name"] if backups else None,
            "newest_backup": backups[0]["name"] if backups else None,
            "backups": backups
        }


# Global instance
_manager = None

def get_backup_manager() -> BackupManager:
    """Get or create global backup manager instance"""
    global _manager
    if _manager is None:
        _manager = BackupManager()
    return _manager


def create_backup(prefix: str = "scripturemon") -> Optional[Path]:
    """
    Create a backup using the global manager
    
    Args:
        prefix: Prefix for backup filename
        
    Returns:
        Path to created backup or None if failed
    """
    manager = get_backup_manager()
    return manager.create_backup(prefix)


def rotate_backups() -> List[Path]:
    """
    Rotate backups using the global manager
    
    Returns:
        List of deleted backup paths
    """
    manager = get_backup_manager()
    return manager.rotate_backups()


def list_backups() -> List[Dict[str, Any]]:
    """
    List all backups using the global manager
    
    Returns:
        List of backup info dicts
    """
    manager = get_backup_manager()
    return manager.list_backups()


if __name__ == "__main__":
    # Test the backup manager
    manager = BackupManager()
    
    # Create a test backup
    backup_path = manager.create_backup("test")
    if backup_path:
        print(f"Created backup: {backup_path}")
    
    # List backups
    backups = manager.list_backups()
    print(f"\nCurrent backups ({len(backups)}):")
    for backup in backups:
        print(f"  - {backup['name']} ({backup['size_mb']} MB)")
    
    # Get status
    status = manager.get_status()
    print(f"\nBackup status:")
    print(f"  Total size: {status['total_size_mb']} MB")
    print(f"  Backups: {status['current_backups']}/{status['max_backups']}")