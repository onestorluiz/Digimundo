#!/bin/bash
# clean_backups.sh - Remove backups redundantes e aninhados
# ATENÇÃO: Este script remove ~140GB de backups duplicados

echo "=" 
echo "🧹 LIMPEZA DE BACKUPS REDUNDANTES"
echo "="
echo ""
echo "📊 Situação atual:"
echo "   Espaço usado: $(du -sh backups/ 2>/dev/null | cut -f1)"
echo "   Total de arquivos: $(ls backups/*.zip backups/*.tar.gz 2>/dev/null | wc -l)"
echo ""

# Confirmar ação
read -p "⚠️  ATENÇÃO: Isso removerá ~140GB de backups duplicados. Continuar? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ Cancelado pelo usuário"
    exit 0
fi

echo ""
echo "🗑️  Iniciando limpeza..."
echo ""

# Contador
deleted=0
kept=0

# 1. Remover backups aninhados de 4.2GB (phase_00 até phase_03)
echo "1️⃣ Removendo backups aninhados de 4.2GB..."
for file in backups/20250905_124*-phase*.zip \
            backups/20250905_125*-phase*.zip \
            backups/20250905_135100-*.zip; do
    if [ -f "$file" ]; then
        echo "   Removendo: $(basename $file)"
        rm -f "$file"
        ((deleted++))
    fi
done

# 2. Remover versões v31/v32 redundantes de 2.8GB
echo ""
echo "2️⃣ Removendo versões v31/v32 redundantes..."
for file in backups/20250906_*-v3*.zip \
            backups/20250906_*-*_patch.zip \
            backups/20250906_*-*_pre.zip \
            backups/20250906_*-*_post.zip; do
    if [ -f "$file" ]; then
        echo "   Removendo: $(basename $file)"
        rm -f "$file"
        ((deleted++))
    fi
done

# 3. Remover backups fix/integrate de 4.4GB
echo ""
echo "3️⃣ Removendo backups fix/integrate antigos..."
for file in backups/20250907_*-fix*.zip \
            backups/20250908_*-integrate*.zip \
            backups/20250909_082507-phase0_initial.zip \
            backups/20250909_175008-phase0_initial.zip; do
    if [ -f "$file" ]; then
        echo "   Removendo: $(basename $file)"
        rm -f "$file"
        ((deleted++))
    fi
done

# 4. Remover backups CLI redundantes
echo ""
echo "4️⃣ Removendo backups CLI redundantes..."
for file in backups/cli_*.zip \
            backups/20250909_105353-phase6_personas.zip \
            backups/20250909_110535-phase7_final.zip \
            backups/20250909_125005-rejoin.zip; do
    if [ -f "$file" ]; then
        echo "   Removendo: $(basename $file)"
        rm -f "$file"
        ((deleted++))
    fi
done

# 5. Remover fases antigas de 473MB
echo ""
echo "5️⃣ Removendo fases antigas de setembro 05..."
for file in backups/20250905_10*-phase*.zip \
            backups/20250905_11*-phase*.zip \
            backups/20250905_122301-phase_15_final.zip; do
    if [ -f "$file" ]; then
        echo "   Removendo: $(basename $file)"
        rm -f "$file"
        ((deleted++))
    fi
done

# 6. Remover tar.gz grandes antigos
echo ""
echo "6️⃣ Removendo tar.gz grandes antigos..."
for file in backups/phase4_telepathy_*.tar.gz \
            backups/phase5_monitoring_*.tar.gz \
            backups/BACKUP_RESTORE_FULL_SYSTEM_*.tar.gz \
            backups/backup_fase*_complete_*.tar.gz; do
    if [ -f "$file" ]; then
        echo "   Removendo: $(basename $file)"
        rm -f "$file"
        ((deleted++))
    fi
done

# 7. Remover FASE_* backups grandes
echo ""
echo "7️⃣ Removendo backups FASE_* antigos..."
for file in backups/FASE_*_BACKUP_*.zip; do
    if [ -f "$file" ]; then
        echo "   Removendo: $(basename $file)"
        rm -f "$file"
        ((deleted++))
    fi
done

# 8. Remover outros backups problemáticos
echo ""
echo "8️⃣ Removendo outros backups problemáticos..."
if [ -f "backups/20250906_191957-harmonia_post.zip" ]; then
    echo "   Removendo: 20250906_191957-harmonia_post.zip"
    rm -f "backups/20250906_191957-harmonia_post.zip"
    ((deleted++))
fi

# Contar arquivos mantidos
for file in backups/*.zip backups/*.tar.gz; do
    if [ -f "$file" ]; then
        ((kept++))
    fi
done

echo ""
echo "=" 
echo "✅ LIMPEZA COMPLETA!"
echo "=" 
echo ""
echo "📊 Resultado:"
echo "   Arquivos removidos: $deleted"
echo "   Arquivos mantidos: $kept"
echo "   Novo espaço usado: $(du -sh backups/ 2>/dev/null | cut -f1)"
echo ""
echo "💾 Backups essenciais preservados:"
ls -lah backups/scripturemon_backup_*.tar.gz 2>/dev/null | tail -5
ls -lah backups/20250909_*-phase*.zip 2>/dev/null | grep -v "phase0_initial" | tail -5
echo ""
echo "✨ Espaço liberado: ~140GB"