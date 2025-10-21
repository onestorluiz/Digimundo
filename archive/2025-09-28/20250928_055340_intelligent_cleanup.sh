#!/bin/bash
# SCRIPTUREMON INTELLIGENT CLEANUP
# Limpeza inteligente sem perder dados importantes

echo "🤖 Iniciando limpeza inteligente..."

# 1. Temporários (24h+)
echo "Limpando temporários antigos..."
find outputs/temporary -type f -mtime +1 -delete 2>/dev/null

# 2. Logs antigos (compactar após 30 dias)
echo "Compactando logs antigos..."
find outputs/logs -name "*.log" -mtime +30 -exec gzip {} \; 2>/dev/null

# 3. Resultados de teste antigos
echo "Removendo resultados de teste antigos..."
find tests/results -name "*_result.txt" -mtime +7 -delete 2>/dev/null

# 4. Database backup (manter apenas o mais recente)
echo "Mantendo apenas backup mais recente do DB..."
cd data/memories/backups
ls -t *.db 2>/dev/null | tail -n +2 | xargs rm -f 2>/dev/null

# 5. Cache não usado
echo "Limpando cache não utilizado..."
find data/cache -type f -atime +14 -delete 2>/dev/null

# 6. Git cleanup
echo "Otimizando Git..."
git gc --auto 2>/dev/null

echo "✅ Limpeza inteligente concluída!"
echo "📊 Espaço economizado: $(du -sh . | cut -f1)"
