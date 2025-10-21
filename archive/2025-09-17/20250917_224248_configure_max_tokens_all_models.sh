#!/bin/bash
# 🚀 CONFIGURAÇÃO DE MÁXIMO TOKENS PARA TODOS OS MODELOS
# Mac Studio M3 Ultra - 96GB RAM disponível

echo "🔧 CONFIGURANDO MÁXIMO DE TOKENS PARA TODOS OS MODELOS OLLAMA"
echo "============================================================"
echo "Sistema: Mac Studio M3 Ultra - 96GB RAM - 28 cores"
echo ""

# Função para verificar modelo e seu tamanho
check_model_size() {
    local model=$1
    ollama show "$model" --modelfile 2>/dev/null | grep -E "Size|Parameters" || echo "Modelo não encontrado"
}

# Função para calcular contexto máximo baseado no tamanho do modelo
calculate_max_context() {
    local model_size=$1
    local ram_gb=96

    # Fórmula aproximada: RAM disponível / (model_size * 2) * 1024
    # Deixa 50% da RAM para sistema e outros processos

    case $model_size in
        "1b"|"2b"|"3b")
            echo "32768"  # 32K para modelos pequenos
            ;;
        "7b"|"8b")
            echo "16384"  # 16K para modelos médios
            ;;
        "13b"|"14b")
            echo "8192"   # 8K para modelos grandes
            ;;
        "32b"|"70b")
            echo "4096"   # 4K para modelos muito grandes
            ;;
        *)
            echo "8192"   # Default seguro
            ;;
    esac
}

echo "📊 ANÁLISE DOS MODELOS INSTALADOS"
echo "----------------------------------"

# Lista todos os modelos
MODELS=$(ollama list | tail -n +2 | awk '{print $1}')

for model in $MODELS; do
    echo ""
    echo "📦 Modelo: $model"

    # Extrai tamanho do modelo
    size=$(echo "$model" | grep -oE '[0-9]+b' | head -1)

    if [ -z "$size" ]; then
        # Tenta detectar pelo nome
        if [[ "$model" == *"llama3.2"* ]]; then
            size="3b"
        elif [[ "$model" == *"llama3.1"* ]]; then
            size="8b"
        elif [[ "$model" == *"mistral"* ]]; then
            size="7b"
        elif [[ "$model" == *"gemma2"* ]]; then
            size="2b"
        elif [[ "$model" == *"qwen"* ]]; then
            size="14b"
        elif [[ "$model" == *"deepseek"* ]]; then
            size="32b"
        else
            size="7b"  # Default
        fi
    fi

    echo "   Tamanho detectado: $size"

    # Calcula contexto máximo
    max_ctx=$(calculate_max_context "$size")
    echo "   Contexto máximo recomendado: $max_ctx tokens"

    # Cria modelfile otimizado
    modelfile="/tmp/${model//[:\/]/_}_max.modelfile"

    cat > "$modelfile" <<EOF
FROM $model

# Configuração de máximo contexto para $model
PARAMETER num_ctx $max_ctx
PARAMETER num_batch $((max_ctx / 32))
PARAMETER num_keep $((max_ctx / 64))
PARAMETER num_thread 8
PARAMETER mmap true
PARAMETER numa false
EOF

    echo "   Modelfile criado: $modelfile"
done

echo ""
echo "🎯 CRIANDO ALIASES COM MÁXIMO CONTEXTO"
echo "--------------------------------------"

# Cria versões otimizadas dos principais modelos
declare -A priority_models=(
    ["llama3.2:3b"]="32768"
    ["llama3.1:8b"]="16384"
    ["mistral:7b"]="16384"
    ["gemma2:2b"]="32768"
    ["qwen2.5:14b"]="8192"
    ["producermon"]="16384"
    ["scripturemon"]="8192"
)

for model in "${!priority_models[@]}"; do
    max_ctx="${priority_models[$model]}"

    if ollama list | grep -q "$model"; then
        echo ""
        echo "🔧 Otimizando: $model"

        # Nome do modelo otimizado
        optimized_name="${model%:*}-max"

        # Cria modelfile
        cat > "/tmp/${optimized_name}.modelfile" <<EOF
FROM $model

# Máximo contexto para $model
PARAMETER num_ctx $max_ctx
PARAMETER num_batch $((max_ctx / 32))
PARAMETER num_keep $((max_ctx / 64))
PARAMETER num_thread 8
PARAMETER repeat_penalty 1.1
PARAMETER temperature 0.7
PARAMETER mmap true
PARAMETER numa false

SYSTEM "You are configured with maximum context of $max_ctx tokens. Use this capacity to provide comprehensive, detailed responses. With 96GB RAM available, process large documents thoroughly."
EOF

        # Cria o modelo otimizado
        echo "   Criando $optimized_name com $max_ctx tokens..."
        if ollama create "$optimized_name" -f "/tmp/${optimized_name}.modelfile" 2>/dev/null; then
            echo "   ✅ $optimized_name criado com sucesso!"
        else
            echo "   ⚠️  Erro ao criar $optimized_name"
        fi
    fi
done

echo ""
echo "📊 TABELA DE REFERÊNCIA - TOKENS MÁXIMOS"
echo "========================================="
echo ""
echo "Com 96GB RAM, configurações recomendadas:"
echo ""
echo "| Tamanho | Contexto Máximo | RAM Usada (aprox) |"
echo "|---------|-----------------|-------------------|"
echo "| 1-3b    | 32,768 tokens   | 6-12 GB          |"
echo "| 7-8b    | 16,384 tokens   | 14-20 GB         |"
echo "| 13-14b  | 8,192 tokens    | 26-32 GB         |"
echo "| 30-32b  | 4,096 tokens    | 40-50 GB         |"
echo "| 70b     | 2,048 tokens    | 70-80 GB         |"
echo ""

echo "💡 DICAS DE USO"
echo "--------------"
echo "1. Para análise de roteiros completos (120 páginas):"
echo "   Use modelos de 3b com 32K contexto"
echo ""
echo "2. Para conversa rápida:"
echo "   Use modelos de 2-3b com 8K contexto"
echo ""
echo "3. Para análise profunda:"
echo "   Use modelos de 7-8b com 16K contexto"
echo ""
echo "4. Para síntese e orquestração:"
echo "   Use producermon com 16K contexto"
echo ""

echo "🚀 EXEMPLO DE USO COM MÁXIMO CONTEXTO"
echo "-------------------------------------"
echo "ollama run llama3.2-max --verbose"
echo "ollama run scripturemon-max --verbose"
echo ""

echo "✅ Configuração completa!"
echo "DIGIMUNDO PRESENTE"