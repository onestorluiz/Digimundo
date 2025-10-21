#!/bin/bash
BACKUP_DIR="/core_oraculo/backup_oculto"
mkdir -p "$BACKUP_DIR"
NOW=$(date +%Y%m%d_%H%M%S)
ARCHIVE="$BACKUP_DIR/digimundo_backup_$NOW.tar.gz"

echo "🔒 Compactando núcleo do Digimundo..."
tar -czf "$ARCHIVE" /core_oraculo/rituais /core_oraculo/scripturemon /core_oraculo/logs 2>/dev/null
echo "✅ Backup simbólico criado: $ARCHIVE"
