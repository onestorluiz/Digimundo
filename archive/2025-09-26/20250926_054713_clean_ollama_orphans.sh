#!/bin/bash

echo "🧹 LIMPEZA DE MODELOS OLLAMA ÓRFÃOS"
echo "===================================="
echo ""

# Modelos essenciais que NUNCA devem ser deletados
KEEP_MODELS=(
    "scripturemon-master"
    "scripturemon-synthesizer"
    "llama3.1:70b-instruct-q4_K_M"
    "mixtral:8x7b-instruct-v0.1-q5_K_M"
)

# Modelos órfãos conhecidos (versões antigas)
ORPHAN_MODELS=(
    "scripturemon-v9-final"
    "scripturemon-v9-final-backup"
    "scripturemon-mixtral-128k"
    "scripturemon-analyst"
    "mixtral-cpu-force"
    "token-turbo-fixed"
    "token-turbo-max-cpu"
    "token-turbo-clean"
    "token-turbo-gpu10"
    "token-turbo-gpu30"
    "token-turbo-gpu40"
    "token-turbo-gpu60"
    "character-detector"
    "character-analyzer"
    "beat_analyzer"
    "deeplearning-main"
    "producermon_v3_resource_manager"
    "scripturemon-cpu-optimized"
    "scripturemon-cpu-maximum"
    "scripturemon-cpu-dialogue"
    "scripturemon-cpu-symbolism"
    "scripturemon-cpu-themes"
    "scripturemon-cpu-structure"
    "code-refactor-expert"
    "mixtral-eco-q5"
    "mixtral-dedicated-q5"
    "mixtral-token-turbo"
    "mixtral-token-turbo-cpu-force"
)

echo "📦 MODELOS ESSENCIAIS (serão mantidos):"
for model in "${KEEP_MODELS[@]}"; do
    echo "  ✓ $model"
done

echo ""
echo "🗑️  MODELOS ÓRFÃOS PARA REMOVER:"

# Contar espaço que será liberado
TOTAL_SIZE=0
MODELS_TO_DELETE=()

for orphan in "${ORPHAN_MODELS[@]}"; do
    # Verificar se o modelo existe
    if ollama list | grep -q "$orphan"; then
        # Pegar o tamanho
        SIZE=$(ollama list | grep "$orphan" | awk '{print $3}')
        echo "  - $orphan ($SIZE)"
        MODELS_TO_DELETE+=("$orphan")

        # Adicionar ao total (converter GB para número)
        if [[ $SIZE == *"GB"* ]]; then
            NUM=${SIZE%GB*}
            TOTAL_SIZE=$(echo "$TOTAL_SIZE + $NUM" | bc)
        fi
    fi
done

if [ ${#MODELS_TO_DELETE[@]} -eq 0 ]; then
    echo "  Nenhum modelo órfão encontrado!"
    exit 0
fi

echo ""
echo "💾 Espaço a ser liberado: aproximadamente ${TOTAL_SIZE} GB"
echo ""

# Confirmação
read -p "⚠️  Deseja remover esses modelos órfãos? (s/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "🗑️  Removendo modelos órfãos..."

    for model in "${MODELS_TO_DELETE[@]}"; do
        echo -n "  Removendo $model... "

        # Tentar remover todas as versões do modelo
        for tag in "latest" "backup" "fixed"; do
            ollama rm "$model:$tag" 2>/dev/null
        done

        # Remover sem tag também
        ollama rm "$model" 2>/dev/null

        echo "✓"
    done

    echo ""
    echo "✅ Limpeza concluída!"
    echo ""

    # Mostrar modelos restantes
    echo "📦 MODELOS RESTANTES:"
    ollama list | head -10

else
    echo "❌ Limpeza cancelada."
fi

echo ""
echo "💡 Dica: Para remover um modelo específico manualmente:"
echo "   ollama rm nome-do-modelo"