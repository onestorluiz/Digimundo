#!/bin/bash

echo "========================================"
echo "🧹 LIMPEZA DE MODELOS OLLAMA"
echo "========================================"
echo ""

# Modelos para MANTER
KEEP_MODELS=(
    "deepseek-r1:32b"
    "deepseek-r1:70b"
    "deepseek-r1:14b"
    "scripturemon-deepseek:latest"
    "scripturemon-ultimate:latest"
    "mistral:instruct"
    "mistral:latest"
    "llama3.1:8b"
    "llama3.2:latest"
    "qwen2.5-coder:7b"
)

echo "📦 MODELOS ESSENCIAIS A MANTER (10):"
for model in "${KEEP_MODELS[@]}"; do
    echo "   ✅ $model"
done
echo ""

# Listar todos os modelos atuais
ALL_MODELS=$(ollama list | tail -n +2 | awk '{print $1}')
TOTAL_MODELS=$(echo "$ALL_MODELS" | wc -l)

echo "📊 Total de modelos atuais: $TOTAL_MODELS"
echo ""

# Array para armazenar modelos a remover
MODELS_TO_REMOVE=()

# Identificar modelos para remover
for model in $ALL_MODELS; do
    SHOULD_KEEP=false
    
    for keep_model in "${KEEP_MODELS[@]}"; do
        if [[ "$model" == "$keep_model" ]]; then
            SHOULD_KEEP=true
            break
        fi
    done
    
    if [[ "$SHOULD_KEEP" == false ]]; then
        MODELS_TO_REMOVE+=("$model")
    fi
done

REMOVE_COUNT=${#MODELS_TO_REMOVE[@]}
echo "🗑️ Modelos a remover: $REMOVE_COUNT"
echo ""

if [ $REMOVE_COUNT -eq 0 ]; then
    echo "✅ Nenhum modelo para remover!"
    exit 0
fi

echo "⚠️ AVISO: Isso removerá $REMOVE_COUNT modelos e liberará muito espaço em disco!"
echo ""
echo "Modelos que serão REMOVIDOS:"
echo "----------------------------"
for model in "${MODELS_TO_REMOVE[@]}"; do
    SIZE=$(ollama list | grep "^$model " | awk '{print $3 " " $4}')
    echo "   ❌ $model ($SIZE)"
done | head -20

if [ $REMOVE_COUNT -gt 20 ]; then
    echo "   ... e mais $((REMOVE_COUNT - 20)) modelos"
fi

echo ""
echo "Pressione ENTER para confirmar ou Ctrl+C para cancelar..."
read

echo ""
echo "🔄 Iniciando remoção..."
echo ""

# Remover modelos
REMOVED=0
FAILED=0

for model in "${MODELS_TO_REMOVE[@]}"; do
    echo -n "Removendo $model... "
    if ollama rm "$model" 2>/dev/null; then
        echo "✅"
        REMOVED=$((REMOVED + 1))
    else
        echo "❌ Falhou"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "========================================"
echo "📊 RESULTADO DA LIMPEZA:"
echo "========================================"
echo "✅ Removidos: $REMOVED modelos"
echo "❌ Falharam: $FAILED modelos"
echo ""

# Listar modelos restantes
echo "📦 MODELOS RESTANTES:"
ollama list | tail -n +2 | awk '{print "   • " $1 " (" $3 " " $4 ")"}'

echo ""
echo "💾 Espaço em disco liberado!"
echo "✅ Sistema otimizado com apenas modelos essenciais"
echo ""