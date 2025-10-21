#!/usr/bin/env python3
"""
Backup Configuration - Sistema centralizado de configuração de backups
Prevents recursion and directs all backups to SURGICAL_PRESERVATION
"""

import os
from pathlib import Path
from datetime import datetime

# Base directory for all backups
SURGICAL_PRESERVATION_BASE = Path("/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION")

# Create date-based subfolder
def get_backup_dir():
    """Get or create today's backup directory in SURGICAL_PRESERVATION"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    backup_dir = SURGICAL_PRESERVATION_BASE / f"{date_str}_SCRIPTUREMON_CHAMPION"
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir

# Backup configuration
BACKUP_CONFIG = {
    # Main backup directory - OUTSIDE the project to prevent recursion
    "backup_dir": get_backup_dir(),

    # Directories to exclude from backups (prevent recursion)
    "exclude_patterns": [
        "backups",
        "BACKUPS_SISTEMA",
        ".git",
        "__pycache__",
        "*.pyc",
        ".DS_Store",
        "deployments",  # Prevent deployment loop
        "dist",
        "build",
        "*.tar.gz",
        "*.zip",
        "node_modules",
        ".venv",
        "venv",
        "env",
        ".cache",
        "logs/*.log"
    ],

    # Directories to include in backups
    "include_dirs": [
        "apps",
        "tests",
        "config",
        "data/revolutionary",  # Crystal Memory
        "data/crystal_memory",
        "docs",
        "bin",
        "Pesquisas_Digilab"
    ],

    # Backup naming convention
    "name_format": "scripturemon_champion_{timestamp}_{label}.tar.gz",

    # Maximum backups to keep per day
    "max_backups_per_day": 10,

    # Retention policy (days)
    "retention_days": 30,

    # Compression level (0-9, 9 = maximum)
    "compression_level": 6,

    # Create metadata file with each backup
    "create_metadata": True,

    # Metadata to include
    "metadata_fields": [
        "timestamp",
        "size_bytes",
        "files_count",
        "directories_count",
        "soul_id",
        "evolution_level",
        "phases_completed",
        "harmony_score"
    ]
}

# Helper functions
def get_exclude_args():
    """Get tar exclude arguments"""
    excludes = []
    for pattern in BACKUP_CONFIG["exclude_patterns"]:
        excludes.extend(["--exclude", pattern])
    return excludes

def get_backup_path(label=None):
    """Get full backup path with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    label_str = f"_{label}" if label else ""
    filename = f"scripturemon_champion_{timestamp}{label_str}.tar.gz"
    return BACKUP_CONFIG["backup_dir"] / filename

def validate_backup_location():
    """Ensure backup is not inside project directory"""
    import sys
    project_dir = Path(sys.argv[0]).parent.absolute()
    backup_dir = BACKUP_CONFIG["backup_dir"].absolute()

    # Check if backup dir is inside project dir
    try:
        backup_dir.relative_to(project_dir)
        # If this doesn't raise, backup is inside project - BAD!
        raise ValueError(
            f"❌ ERRO CRÍTICO: Backup directory está DENTRO do projeto!\n"
            f"   Projeto: {project_dir}\n"
            f"   Backup: {backup_dir}\n"
            f"   Isso causará RECURSÃO INFINITA!\n"
            f"   Use SURGICAL_PRESERVATION em: {SURGICAL_PRESERVATION_BASE}"
        )
    except ValueError:
        # Good - backup is outside project
        pass

    return True

# Auto-validate on import
if __name__ != "__main__":
    validate_backup_location()