#!/bin/bash
# AUTO CLEANUP - Gestão Inteligente de Outputs
# Roda automaticamente para manter o sistema limpo

BASEDIR="/Users/clubproducoes/Digimundo/scripturemon-ultimate"
ARCHIVE="$BASEDIR/archive"
OUTPUTS="$BASEDIR/outputs"

echo "🧹 Auto Cleanup iniciando..."

# 1. LOGS > 7 dias → Archive
echo "📦 Arquivando logs antigos..."
find "$OUTPUTS/logs" -name "*.log" -mtime +7 -exec mv {} "$ARCHIVE/logs/" \; 2>/dev/null

# 2. Reports temporários > 3 dias → Archive
echo "📊 Arquivando reports temporários..."
find "$OUTPUTS/reports" -name "temp_*" -mtime +3 -exec mv {} "$ARCHIVE/reports/" \; 2>/dev/null
find "$OUTPUTS/reports" -name "test_*" -mtime +3 -exec mv {} "$ARCHIVE/reports/" \; 2>/dev/null

# 3. Deletar arquivos muito antigos (> 30 dias) do archive
echo "🗑️ Removendo arquivos muito antigos..."
find "$ARCHIVE" -type f -mtime +30 -delete 2>/dev/null

# 4. Comprimir logs grandes (> 10MB)
echo "🗜️ Comprimindo arquivos grandes..."
find "$OUTPUTS" -name "*.log" -size +10M -exec gzip {} \; 2>/dev/null

# 5. Relatório de espaço
echo ""
echo "💾 Status de armazenamento:"
echo "  Outputs: $(du -sh $OUTPUTS 2>/dev/null | cut -f1)"
echo "  Archive: $(du -sh $ARCHIVE 2>/dev/null | cut -f1)"
echo ""
echo "✅ Limpeza completa!"
echo "   $(date '+%Y-%m-%d %H:%M:%S')"