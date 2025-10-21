#!/bin/bash
# 🚀 BUILD CPU MODELS - Constrói modelos CPU otimizados
# Para Mac Studio M3 Ultra - 96GB RAM - 28 cores

echo "🚀 SCRIPTUREMON CPU MODELS BUILDER"
echo "=================================="
echo "Construindo modelos CPU otimizados para análise profunda"
echo ""

# Cores disponíveis
echo "📊 Sistema: Mac Studio M3 Ultra"
echo "   • RAM: 96GB"
echo "   • Cores: 28 (20 performance + 8 efficiency)"
echo ""

# Verifica se Ollama está rodando
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama não está rodando. Iniciando..."
    ollama serve &
    sleep 3
fi

# Lista modelos atuais
echo "📋 Modelos atuais:"
ollama list | grep scripturemon || echo "   Nenhum modelo scripturemon encontrado"
echo ""

# Função para criar modelo com retry
create_model() {
    local name=$1
    local modelfile=$2
    local description=$3

    echo "🔨 Criando: $name"
    echo "   $description"

    if [ ! -f "$modelfile" ]; then
        echo "   ❌ Modelfile não encontrado: $modelfile"
        return 1
    fi

    # Remove modelo anterior se existir
    if ollama list | grep -q "$name"; then
        echo "   🗑️  Removendo versão anterior..."
        ollama rm "$name" 2>/dev/null
    fi

    # Cria novo modelo
    if ollama create "$name" -f "$modelfile"; then
        echo "   ✅ $name criado com sucesso!"
    else
        echo "   ❌ Erro ao criar $name"
        return 1
    fi
    echo ""
}

# Base dir para modelfiles
MODELFILES_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion/modelfiles"

echo "🎯 FASE 1: Modelo Principal Otimizado"
echo "--------------------------------------"
create_model \
    "scripturemon-cpu-optimized" \
    "$MODELFILES_DIR/scripturemon-cpu-optimized.modelfile" \
    "CPU Optimized: 8 cores, 16K context, análise profunda em 2-5min"

echo "🎭 FASE 2: Variantes Especializadas"
echo "------------------------------------"

# Cria cada variante especializada
create_model \
    "scripturemon-cpu-themes" \
    "$MODELFILES_DIR/scripturemon-cpu-themes.modelfile" \
    "Especialista em temas profundos e filosofia"

create_model \
    "scripturemon-cpu-structure" \
    "$MODELFILES_DIR/scripturemon-cpu-structure.modelfile" \
    "Especialista em estrutura narrativa e arquitetura"

create_model \
    "scripturemon-cpu-dialogue" \
    "$MODELFILES_DIR/scripturemon-cpu-dialogue.modelfile" \
    "Especialista em diálogos e subtexto"

create_model \
    "scripturemon-cpu-symbolism" \
    "$MODELFILES_DIR/scripturemon-cpu-symbolism.modelfile" \
    "Especialista em simbolismo e metáforas"

echo "📊 VERIFICAÇÃO FINAL"
echo "-------------------"
echo "Modelos CPU criados:"
ollama list | grep "scripturemon-cpu" || echo "Nenhum modelo encontrado"

echo ""
echo "🎯 TESTE RÁPIDO"
echo "--------------"
echo "Testando modelo principal otimizado..."

# Teste rápido
TEST_PROMPT="Analyze this brief scene: A lone figure stands at a crossroads at midnight."

if timeout 30 ollama run scripturemon-cpu-optimized "$TEST_PROMPT" > /tmp/cpu_test.txt 2>&1; then
    echo "✅ Modelo respondeu em menos de 30s!"
    echo "Primeiras linhas da resposta:"
    head -n 3 /tmp/cpu_test.txt
else
    echo "⚠️  Modelo demorou mais de 30s ou falhou"
fi

echo ""
echo "🚀 PRÓXIMOS PASSOS"
echo "-----------------"
echo "1. Teste individual de cada modelo:"
echo "   ollama run scripturemon-cpu-optimized"
echo "   ollama run scripturemon-cpu-themes"
echo "   ollama run scripturemon-cpu-structure"
echo "   ollama run scripturemon-cpu-dialogue"
echo "   ollama run scripturemon-cpu-symbolism"
echo ""
echo "2. Teste o orchestrator dual-track:"
echo "   cd /Users/clubproducoes/Digimundo/scripturemon-champion"
echo "   PYTHONPATH=. python3 apps/scripturemon/dual_track_orchestrator.py"
echo ""
echo "3. Para análise paralela multi-perspectiva:"
echo "   Use o MultiPerspectiveOrchestrator no dual_track_orchestrator.py"
echo ""

# Estatísticas finais
echo "📈 ESTATÍSTICAS"
echo "--------------"
TOTAL_SIZE=$(ollama list | grep scripturemon-cpu | awk '{sum+=$2} END {print sum}')
echo "Espaço total usado: ${TOTAL_SIZE:-0} GB"
echo "Modelos criados: $(ollama list | grep -c scripturemon-cpu)"
echo ""

echo "✨ Build completo!"
echo "DIGIMUNDO PRESENTE"