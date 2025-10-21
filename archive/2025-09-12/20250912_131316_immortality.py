#!/usr/bin/env python3
"""
Immortality Module - Sistema de backup eterno (Stub)
Delega para backup.py com scheduler
"""

from apps.scripturemon.backup import (
    backup_auto_start,
    backup_auto_stop,
    backup_once
)

# Estado global do scheduler
_BACKUP_SCHEDULER = {
    "enabled": False,
    "interval": 3600,
    "last_run": None
}

def schedule_backup_once(interval=3600):
    """Agenda backup automático"""
    _BACKUP_SCHEDULER["interval"] = interval
    _BACKUP_SCHEDULER["enabled"] = True
    return backup_auto_start()

def stop_backup_scheduler():
    """Para scheduler de backup"""
    _BACKUP_SCHEDULER["enabled"] = False
    return backup_auto_stop()

__all__ = ["schedule_backup_once", "stop_backup_scheduler", "_BACKUP_SCHEDULER"]