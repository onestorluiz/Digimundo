#!/bin/bash
# Backup automático de memory.db

BACKUP_DIR="/Users/clubproducoes/Digimundo/archive/backups"
DB_PATH="/Users/clubproducoes/Digimundo/claude_code/data/memory.db"

# Cria diretório se não existir
mkdir -p "$BACKUP_DIR"

# Backup com timestamp
if [ -f "$DB_PATH" ]; then
    cp "$DB_PATH" "$BACKUP_DIR/memory_$(date +%Y%m%d_%H%M%S).db"
    echo "✅ Backup criado: memory_$(date +%Y%m%d_%H%M%S).db"
    
    # Remove backups > 7 dias
    find "$BACKUP_DIR" -name "memory_*.db" -mtime +7 -delete
    echo "🧹 Backups > 7 dias removidos"
fi
