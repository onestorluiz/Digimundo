#!/bin/bash
echo "🔍 Iniciando limpeza de arquivos obsoletos..."
find /root -type f -name '*.log' -size +100M -print -delete
find /root -type f -name '*.tmp' -mtime +10 -print -delete
find /var/log -type f -name '*.gz' -print -delete
echo "✅ Limpeza simbólica concluída."
