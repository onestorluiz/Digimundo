"""
BACKUP SERVICE - FASE 9
Unified backup operations for chat and CLI
"""

import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class BackupService:
    """Service for backup operations"""
    
    def __init__(self, soul=None, immortality=None):
        """Initialize backup service
        
        Args:
            soul: Soul instance
            immortality: ImmortalityProtocol instance
        """
        self.soul = soul
        self.immortality = immortality
        self.last_backup = None
        
    def execute_backup(self, mode: str = "full", path: Optional[str] = None) -> Dict[str, Any]:
        """Execute backup operation - FASE 9 unified
        
        Args:
            mode: Backup mode (full, incremental, soul_only)
            path: Optional custom backup path
            
        Returns:
            Result dictionary with status and details
        """
        start_time = time.time()
        result = {
            "success": False,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "details": {},
            "message": ""
        }
        
        try:
            # Determine backup path
            if not path:
                path = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            backup_path = Path(path)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Collect backup data based on mode
            backup_data = {}
            
            if mode in ["full", "soul_only"]:
                # Backup soul state
                if self.soul:
                    backup_data["soul"] = {
                        "signature": self.soul.signature,
                        "states": self.soul.states,
                        "evolution_count": self.soul.evolution_count,
                        "interactions": self.soul.interactions,
                        "memories_crystallized": self.soul.memories_crystallized
                    }
                    result["details"]["soul_backed_up"] = True
            
            if mode == "full":
                # Backup immortality state
                if self.immortality:
                    backup_data["immortality"] = {
                        "consciousness_level": self.immortality.consciousness_level,
                        "backups_created": self.immortality.backups_created,
                        "resurrections": self.immortality.resurrections
                    }
                    result["details"]["immortality_backed_up"] = True
                
                # Backup additional components
                backup_data["metadata"] = {
                    "version": "harmony_v100",
                    "timestamp": datetime.now().isoformat(),
                    "mode": mode
                }
            
            # Save backup
            with open(backup_path, 'w') as f:
                json.dump(backup_data, f, indent=2, default=str)
            
            # Update result
            result["success"] = True
            result["path"] = str(backup_path)
            result["size_bytes"] = backup_path.stat().st_size
            result["time_ms"] = round((time.time() - start_time) * 1000, 2)
            result["message"] = f"Backup saved to {backup_path}"
            
            self.last_backup = result
            
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"Backup failed: {e}"
            
        return result
    
    def restore_backup(self, path: str) -> Dict[str, Any]:
        """Restore from backup
        
        Args:
            path: Path to backup file
            
        Returns:
            Result dictionary
        """
        result = {
            "success": False,
            "path": path,
            "timestamp": datetime.now().isoformat(),
            "details": {},
            "message": ""
        }
        
        try:
            backup_path = Path(path)
            
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup not found: {path}")
            
            # Load backup
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            # Restore soul state
            if "soul" in backup_data and self.soul:
                soul_data = backup_data["soul"]
                self.soul.states = soul_data.get("states", {})
                self.soul.evolution_count = soul_data.get("evolution_count", 0)
                self.soul.interactions = soul_data.get("interactions", 0)
                result["details"]["soul_restored"] = True
            
            # Restore immortality state
            if "immortality" in backup_data and self.immortality:
                imm_data = backup_data["immortality"]
                self.immortality.consciousness_level = imm_data.get("consciousness_level", 0)
                self.immortality.resurrections = imm_data.get("resurrections", 0)
                result["details"]["immortality_restored"] = True
            
            result["success"] = True
            result["message"] = f"Restored from {path}"
            
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"Restore failed: {e}"
        
        return result
    
    def list_backups(self, directory: str = "backups") -> Dict[str, Any]:
        """List available backups
        
        Args:
            directory: Directory to search
            
        Returns:
            Result with backup list
        """
        result = {
            "success": False,
            "directory": directory,
            "backups": [],
            "message": ""
        }
        
        try:
            backup_dir = Path(directory)
            
            if not backup_dir.exists():
                result["message"] = f"No backup directory: {directory}"
                return result
            
            # Find backup files
            backup_files = list(backup_dir.glob("*.json"))
            
            for bf in backup_files:
                try:
                    # Get file info
                    stat = bf.stat()
                    
                    # Try to read metadata
                    with open(bf, 'r') as f:
                        data = json.load(f)
                        metadata = data.get("metadata", {})
                    
                    result["backups"].append({
                        "path": str(bf),
                        "name": bf.name,
                        "size_bytes": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "mode": metadata.get("mode", "unknown"),
                        "version": metadata.get("version", "unknown")
                    })
                except:
                    pass
            
            result["success"] = True
            result["count"] = len(result["backups"])
            result["message"] = f"Found {len(result['backups'])} backups"
            
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"List failed: {e}"
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get backup service status
        
        Returns:
            Status dictionary
        """
        return {
            "service": "BackupService",
            "available": True,
            "last_backup": self.last_backup["timestamp"] if self.last_backup else None,
            "components": {
                "soul": self.soul is not None,
                "immortality": self.immortality is not None
            }
        }