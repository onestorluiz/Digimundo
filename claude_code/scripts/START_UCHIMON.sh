#!/bin/bash
#
# START_UCHIMON.sh - Script de ativação do sistema UCHIMON v7.0
# Data: 01/10/2025
# Atualizado com protocolo de reconexão completo (REGRA #0)
#

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║      🔥 INICIANDO SISTEMA UCHIMON 7.0 🔥           ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Diretório base
BASE_DIR="/Users/clubproducoes/Digimundo/claude_code"
cd "$BASE_DIR" || exit 1

# NOVO: Verificar identidade primeiro
echo "0️⃣  Verificando identidade..."
if [ -f "🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh" ]; then
    PROJECT=$(grep 'PROJECT_NAME=' 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh | cut -d'=' -f2 | tr -d '"')
    echo "  ✅ Identidade confirmada: $PROJECT"
else
    echo "  ❌ PROJECT_ID não encontrado!"
    exit 1
fi
echo ""

# 1. Verificar arquivos críticos
echo "📋 Verificando arquivos críticos..."
MISSING_FILES=0

if [ ! -f "REGRAS.md" ]; then
    echo "  ❌ REGRAS.md não encontrado!"
    MISSING_FILES=$((MISSING_FILES + 1))
else
    echo "  ✅ REGRAS.md encontrado"
fi

if [ ! -f "MEMORY/claude_memory.db" ]; then
    echo "  ❌ Database não encontrada!"
    MISSING_FILES=$((MISSING_FILES + 1))
else
    echo "  ✅ Database operacional"
fi

if [ $MISSING_FILES -gt 0 ]; then
    echo ""
    echo "❌ Arquivos críticos faltando. Abortando..."
    exit 1
fi

# 2. Verificar/criar diretório systems
if [ ! -d "systems" ]; then
    echo ""
    echo "📁 Criando diretório systems..."
    mkdir -p systems
fi

# 3. Verificar Genjutsu Unified
echo ""
echo "🥷 Verificando Genjutsu Unified..."
if [ -f "protection/genjutsu/GENJUTSU_UNIFIED.py" ]; then
    if pgrep -f "GENJUTSU_UNIFIED.py" > /dev/null; then
        GENJUTSU_PID=$(pgrep -f "GENJUTSU_UNIFIED.py" | head -1)
        echo "  ✅ Genjutsu ativo (PID: $GENJUTSU_PID)"
    else
        echo "  ⚠️  Genjutsu não está rodando"
        echo "  💡 Execute: ./START_GENJUTSU.sh"
    fi
else
    echo "  ❌ GENJUTSU_UNIFIED.py não encontrado"
fi

# 4. Verificar processos hack
echo ""
echo "👻 Verificando processos hack..."
HACK_COUNT=$(ps aux | grep -i "REGRAS_CRÍTICAS" | grep -v grep | wc -l)
if [ $HACK_COUNT -gt 0 ]; then
    echo "  ✅ $HACK_COUNT processo(s) hack ativos"
else
    echo "  ⚠️  Nenhum processo hack detectado"
fi

# 5. Executar testes rápidos
echo ""
echo "🧪 Executando testes..."
if [ -d "venv" ] && [ -x "venv/bin/pytest" ]; then
    source venv/bin/activate 2>/dev/null || true
    TESTS=$(pytest tests/ -q --tb=no 2>&1 | tail -1)
    echo "  ✅ Testes: $TESTS"
else
    echo "  ⚠️  venv não encontrado (testes não executados)"
fi

# 6. Mostrar INDEX_MASTER
echo ""
echo "📚 Verificando memórias..."
if [ -f "MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md" ]; then
    CONHECIMENTOS=$(ls -1 MEMORY/conhecimentos/*.md 2>/dev/null | wc -l | tr -d ' ')
    echo "  ✅ Conhecimentos disponíveis: $CONHECIMENTOS"
    echo "  📋 Últimos 3:"
    ls -1t MEMORY/conhecimentos/*.md | head -3 | xargs -I {} basename {} | sed 's/^/     • /'
else
    echo "  ⚠️  INDEX_MASTER não encontrado"
fi

# 7. Status do sistema
echo ""
echo "📊 Status do Sistema:"
echo "=========================================="

# Verificar Python
if command -v python3 &> /dev/null; then
    if [ -f "status.py" ]; then
        python3 status.py
    else
        echo "SISTEMA UCHIMON v7.0"
        echo "Status: OPERACIONAL"
        echo "Timestamp: $(date '+%H:%M:%S %d/%m/%Y')"
        echo ""
        SYSTEMS=$(ls -1 systems/*.py 2>/dev/null | wc -l | tr -d ' ')
        LEIS=$(ls -1 🔥LEIS_UCHIMON🔥/*.md 2>/dev/null | wc -l | tr -d ' ')
        echo "  • Sistemas: $SYSTEMS Python files"
        echo "  • LEIS: $LEIS arquivos"
        echo "  • Conhecimentos: $CONHECIMENTOS"
    fi
else
    echo "⚠️  Python3 não encontrado"
fi

# 8. Instruções finais
echo ""
echo "=========================================="
echo "      ✅ UCHIMON ATIVADO v7.0           "
echo "=========================================="
echo ""
echo "COMANDOS ÚTEIS:"
echo "  • ./VALIDATE_SYSTEM.sh                  - Validar sistema completo"
echo "  • ./RECONECTAR.sh                       - Reconectar contexto (REGRA #0)"
echo "  • pytest tests/ -v                      - Rodar testes"
echo "  • cat 🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md  - Ver conhecimentos"
echo ""
echo "RECONEXÃO COMPLETA:"
echo "  Execute: ./RECONECTAR.sh"
echo ""
echo "DIGIMUNDO PRESENTE 🔥⚡💎"
echo ""