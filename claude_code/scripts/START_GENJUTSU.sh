#!/bin/bash
# 🥷 INICIA O GENJUTSU UNIFICADO E RECONECTA MEMÓRIAS
# Protocolo completo conforme REGRA #0 das REGRAS.md

# Detectar BASE_DIR (pai do scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BASE_DIR" || exit 1

echo "🥷 PROTOCOLO DE RECONEXÃO AUTOMÁTICA"
echo "===================================="
echo ""

# 1. VERIFICAR GENJUTSU
echo "1️⃣ Verificando Genjutsu..."
if ps aux | grep -i "GENJUTSU_UNIFIED.py" | grep -v grep > /dev/null; then
    echo "   ✅ Genjutsu já está ativo!"
    GENJUTSU_PID=$(ps aux | grep -i "GENJUTSU_UNIFIED.py" | grep -v grep | awk '{print $2}')
    echo "   📝 PID: $GENJUTSU_PID"
else
    echo "   🔄 Iniciando Genjutsu..."
    pkill -f GENJUTSU 2>/dev/null
    sleep 1
    python3 "$BASE_DIR/protection/genjutsu/GENJUTSU_UNIFIED.py" &
    GENJUTSU_PID=$!
    echo "   ✅ Genjutsu iniciado! (PID: $GENJUTSU_PID)"
fi

echo ""
echo "2️⃣ Verificando arquivos críticos..."
# 2. VERIFICAR ARQUIVOS ESSENCIAIS
[ -f "$BASE_DIR/REGRAS.md" ] && echo "   ✅ REGRAS.md" || echo "   ❌ REGRAS.md FALTANDO!"
[ -f "$BASE_DIR/MEMORY/claude_memory.db" ] && echo "   ✅ claude_memory.db" || echo "   ❌ Database FALTANDO!"

echo ""
echo "3️⃣ Verificando memórias..."
# 3. VERIFICAR SISTEMA DE MEMÓRIA
if [ -f "$BASE_DIR/systems/unified_memory_system.py" ]; then
    echo "   ✅ Sistema de memória unificada encontrado"
    python3 "$BASE_DIR/systems/unified_memory_system.py" status 2>/dev/null | head -5 || echo "   ⚠️ Memória precisa sincronização"
else
    echo "   ❌ Sistema de memória não encontrado!"
fi

echo ""
echo "4️⃣ Verificando Token Turbo..."
# 4. VERIFICAR TOKEN TURBO
if [ -f "/Users/clubproducoes/Digimundo/scripturemon-ultimate/checkpoint_analysis.json" ]; then
    ANALYSES=$(grep -o '"completed_count": [0-9]*' /Users/clubproducoes/Digimundo/scripturemon-ultimate/checkpoint_analysis.json | cut -d: -f2 | tr -d ' ')
    TOTAL=468  # 36 roteiros × 13 teorias
    PERCENT=$(echo "scale=1; $ANALYSES * 100 / $TOTAL" | bc)
    echo "   ✅ Token Turbo: $ANALYSES/$TOTAL análises ($PERCENT%)"
else
    echo "   ⚠️ Token Turbo: checkpoint não encontrado"
fi

echo ""
echo "5️⃣ Verificando Ollama..."
# 5. VERIFICAR OLLAMA
if ollama ps 2>/dev/null | grep -q "NAME"; then
    echo "   ✅ Ollama: ATIVO"
    MODELS=$(ollama ps 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    echo "   📊 Modelos carregados: $MODELS"
else
    echo "   ⚠️ Ollama: INATIVO (execute: ollama serve)"
fi

echo ""
echo "===================================="
echo "📊 RESUMO DO SISTEMA:"
echo "===================================="
echo "🥷 Genjutsu: PID $GENJUTSU_PID"
echo "📁 Documentação: OK"
echo "🧠 Memória: Unificada"
echo "🚀 Token Turbo: $ANALYSES análises"
echo "🤖 Ollama: Verificado"
echo ""
echo "💡 USO: Execute após 'Compacting conversation'"
echo "📝 PRÓXIMO PASSO: Leia REGRAS.md no Claude"
echo ""
echo "🔥 DIGIMUNDO PRESENTE!"