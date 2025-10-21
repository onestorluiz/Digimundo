#!/bin/bash
# SMART CLEANUP - Limpeza com Verificação Git
# Só deleta se já estiver no Git

BASEDIR="/Users/clubproducoes/Digimundo/scripturemon-ultimate"
ARCHIVE="$BASEDIR/archive"
OUTPUTS="$BASEDIR/outputs"

echo "🔍 Smart Cleanup - Verificando Git primeiro..."
cd "$BASEDIR"

# Função para verificar se arquivo está no Git
is_in_git() {
    git ls-files --error-unmatch "$1" 2>/dev/null
    return $?
}

# Função para verificar se arquivo foi commitado
is_committed() {
    git diff --quiet HEAD -- "$1" 2>/dev/null
    return $?
}

echo "📊 Analisando arquivos..."

# 1. PROCESSAR LOGS
for log in $(find "$OUTPUTS/logs" -name "*.log" -mtime +7 2>/dev/null); do
    if is_in_git "$log" && is_committed "$log"; then
        echo "  ✅ $log → Git OK, deletando..."
        rm "$log"
    else
        echo "  📦 $log → Não commitado, arquivando..."
        mv "$log" "$ARCHIVE/logs/" 2>/dev/null
    fi
done

# 2. PROCESSAR REPORTS
for report in $(find "$OUTPUTS/reports" -name "*.json" -mtime +3 2>/dev/null); do
    if is_in_git "$report" && is_committed "$report"; then
        echo "  ✅ $report → Git OK, pode deletar"
        rm "$report"
    else
        # Se não está no Git, verifica importância
        if [[ "$report" == *"temp_"* ]] || [[ "$report" == *"test_"* ]]; then
            echo "  🗑️ $report → Temporário, deletando..."
            rm "$report"
        else
            echo "  💾 $report → Importante, commitando..."
            git add "$report" 2>/dev/null
            git commit -m "Auto-backup: $(basename $report)" 2>/dev/null
        fi
    fi
done

# 3. COMPRIMIR ARQUIVOS GRANDES NO ARCHIVE (> 10MB)
find "$ARCHIVE" -type f -size +10M ! -name "*.gz" -exec gzip {} \; 2>/dev/null

# 4. DELETAR APENAS ARQUIVOS MUITO ANTIGOS E JÁ NO GIT (> 60 dias)
for old_file in $(find "$ARCHIVE" -type f -mtime +60 2>/dev/null); do
    # Verifica se o arquivo original estava no Git
    original_path="${old_file/$ARCHIVE/$BASEDIR}"
    if git log --oneline -- "$original_path" 2>/dev/null | grep -q .; then
        echo "  🗑️ $(basename $old_file) → Histórico no Git, deletando..."
        rm "$old_file"
    fi
done

# 5. RELATÓRIO FINAL
echo ""
echo "📈 Status Final:"
echo "  Git Status: $(git status --porcelain | wc -l) arquivos não commitados"
echo "  Outputs: $(du -sh $OUTPUTS 2>/dev/null | cut -f1)"
echo "  Archive: $(du -sh $ARCHIVE 2>/dev/null | cut -f1)"
echo ""
echo "💡 Dica: Execute 'git status' para ver mudanças pendentes"
echo "✅ Smart Cleanup completo! $(date '+%Y-%m-%d %H:%M:%S')"