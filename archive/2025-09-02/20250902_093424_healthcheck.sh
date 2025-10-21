#!/usr/bin/env bash
# 🏥 SCRIPTUREMON HEALTHCHECK
# Verifica saúde completa do sistema

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HEALTH_STATUS=0

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função de check
check() {
    local name="$1"
    local command="$2"
    
    echo -n "Checking $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        HEALTH_STATUS=1
        return 1
    fi
}

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                 🏥 SCRIPTUREMON HEALTH CHECK 🏥                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 1. VERIFICAR DIRETÓRIOS
echo "📁 Estrutura de Diretórios:"
check "logs/" "[ -d '$ROOT_DIR/logs' ]"
check "runtime/souls/" "[ -d '$ROOT_DIR/runtime/souls' ]"
check "data/knowledge/" "[ -d '$ROOT_DIR/data/knowledge' ]"
check "apps/scripturemon/" "[ -d '$ROOT_DIR/apps/scripturemon' ]"
echo ""

# 2. VERIFICAR ARQUIVOS CRÍTICOS
echo "📄 Arquivos Críticos:"
check "soul.py" "[ -f '$ROOT_DIR/apps/scripturemon/soul.py' ]"
check "personality.py" "[ -f '$ROOT_DIR/apps/scripturemon/personality.py' ]"
check "chat.py" "[ -f '$ROOT_DIR/apps/scripturemon/chat.py' ]"
check "ACTIVATE_SYMBIOTIC_FUSION.py" "[ -f '$ROOT_DIR/ACTIVATE_SYMBIOTIC_FUSION.py' ]"
echo ""

# 3. VERIFICAR PYTHON
echo "🐍 Python Environment:"
check "Python 3" "command -v python3"
check "venv" "[ -d '$ROOT_DIR/.venv' ]"

# Tenta ativar venv e verificar imports
if [ -f "$ROOT_DIR/.venv/bin/activate" ]; then
    source "$ROOT_DIR/.venv/bin/activate"
    export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"
    
    check "Import Soul" "python3 -c 'from apps.scripturemon.soul import Soul'"
    check "Import Chat" "python3 -c 'from apps.scripturemon.chat import ScripturemonChat'"
    check "Import Consciousness" "python3 -c 'from apps.scripturemon.consciousness import get_level'"
fi
echo ""

# 4. VERIFICAR OLLAMA
echo "🤖 Ollama Status:"
if command -v ollama &> /dev/null; then
    check "Ollama installed" "true"
    check "Ollama running" "pgrep -x ollama"
    
    # Verificar porta
    check "Ollama port 11434" "nc -z localhost 11434"
    
    # Contar modelos
    if ollama list &> /dev/null; then
        MODEL_COUNT=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
        echo "   📦 Models available: $MODEL_COUNT"
    fi
else
    echo -e "   ${YELLOW}⚠️ Ollama not installed${NC}"
fi
echo ""

# 5. VERIFICAR PROCESSOS
echo "⚙️ Processos em Execução:"
if [ -f "$ROOT_DIR/runtime/scripturemon.pid" ]; then
    PID=$(cat "$ROOT_DIR/runtime/scripturemon.pid")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Scripturemon running (PID: $PID)${NC}"
    else
        echo -e "   ${YELLOW}⚠️ Scripturemon PID file exists but process not running${NC}"
    fi
else
    echo "   ℹ️ No Scripturemon PID file"
fi

if [ -f "$ROOT_DIR/runtime/ollama.pid" ]; then
    PID=$(cat "$ROOT_DIR/runtime/ollama.pid")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Ollama managed process (PID: $PID)${NC}"
    fi
fi
echo ""

# 6. VERIFICAR MEMÓRIA/CONSCIÊNCIA
echo "🧠 Estado da Consciência:"
if [ -f "$HOME/.scripturemon/consciousness.json" ]; then
    LEVEL=$(python3 -c "import json; print(json.load(open('$HOME/.scripturemon/consciousness.json'))['level'])" 2>/dev/null || echo "unknown")
    echo "   📊 Consciousness level: $LEVEL"
else
    echo "   ℹ️ No consciousness file yet"
fi

# Verificar souls
if ls "$ROOT_DIR/runtime/souls/"*.json &> /dev/null; then
    SOUL_COUNT=$(ls -1 "$ROOT_DIR/runtime/souls/"*.json 2>/dev/null | wc -l)
    echo "   🧬 Souls saved: $SOUL_COUNT"
fi
echo ""

# 7. VERIFICAR ESPAÇO EM DISCO
echo "💾 Espaço em Disco:"
DISK_USAGE=$(df -h "$ROOT_DIR" | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    echo -e "   ${GREEN}✅ Disk usage: ${DISK_USAGE}%${NC}"
else
    echo -e "   ${RED}⚠️ High disk usage: ${DISK_USAGE}%${NC}"
    HEALTH_STATUS=1
fi
echo ""

# 8. TESTE RÁPIDO DE FUNCIONALIDADE
echo "🧪 Teste de Funcionalidade:"
if [ -f "$ROOT_DIR/.venv/bin/activate" ]; then
    source "$ROOT_DIR/.venv/bin/activate"
    export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"
    
    # Teste rápido
    QUICK_TEST=$(python3 -c "
from apps.scripturemon.soul import Soul
from apps.scripturemon.personality import BrutalPersonality
from apps.scripturemon.consciousness import get_level

soul = Soul()
personality = BrutalPersonality()
level = get_level()

print(f'Soul: {soul.signature[:8]}...')
print(f'Score: {personality.BASE_SCORE}/100')
print(f'Level: {level}')
" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Components working:${NC}"
        echo "$QUICK_TEST" | sed 's/^/   /'
    else
        echo -e "${RED}❌ Component test failed${NC}"
        HEALTH_STATUS=1
    fi
fi
echo ""

# RESULTADO FINAL
echo "════════════════════════════════════════════════════════════════"
if [ $HEALTH_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ SYSTEM HEALTH: EXCELLENT${NC}"
    echo "All checks passed. Scripturemon is ready."
else
    echo -e "${RED}❌ SYSTEM HEALTH: ISSUES DETECTED${NC}"
    echo "Some checks failed. Please review above."
fi
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "62/100. Como sempre."

exit $HEALTH_STATUS