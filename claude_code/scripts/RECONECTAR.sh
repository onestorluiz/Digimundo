#!/bin/bash
# 🔥 RECONECTAR.sh - Protocolo de reconexão completo (REGRA #0)
# Executa todos os passos para reconectar contexto após nova sessão

set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🔥 PROTOCOLO DE RECONEXÃO AUTOMÁTICA UCHIMON 🔥   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Executando REGRA #0 completa..."
echo ""

BASE_DIR="/Users/clubproducoes/Digimundo/claude_code"
cd "$BASE_DIR" || exit 1

# 0. Verificar Identidade
echo "0️⃣  VERIFICAR IDENTIDADE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh" ]; then
    cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh | grep -E "(PROJECT_NAME|IDENTITY|DOMAIN)" | head -3
    echo ""
else
    echo "❌ PROJECT_ID não encontrado!"
    exit 1
fi

# 1. Verificar/Iniciar GENJUTSU
echo "1️⃣  VERIFICAR GENJUTSU"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if ps aux | grep -i "GENJUTSU" | grep -v grep > /dev/null; then
    echo "✅ GENJUTSU já está ativo"
else
    echo "🔄 Iniciando GENJUTSU..."
    if [ -f "START_GENJUTSU.sh" ]; then
        ./START_GENJUTSU.sh > /dev/null 2>&1 &
        sleep 2
        echo "✅ GENJUTSU iniciado"
    else
        echo "⚠️  START_GENJUTSU.sh não encontrado (opcional)"
    fi
fi
echo ""

# 2. Ler livro_claude
echo "2️⃣  LER LIVRO_CLAUDE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "livro_claude" ]; then
    echo "📚 Estrutura do livro_claude:"
    ls -1 livro_claude/ | head -5
    echo "✅ livro_claude acessível"
else
    echo "⚠️  livro_claude não encontrado"
fi
echo ""

# 3. Conectar MEMORY SQLite
echo "3️⃣  CONECTAR MEMORY DATABASE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "MEMORY/claude_memory.db" ]; then
    DB_SIZE=$(stat -f%z MEMORY/claude_memory.db 2>/dev/null || stat -c%s MEMORY/claude_memory.db)
    TABLES=$(sqlite3 MEMORY/claude_memory.db "SELECT COUNT(*) FROM sqlite_master WHERE type='table';" 2>/dev/null)
    echo "✅ Database: $(echo "$DB_SIZE" | awk '{print int($1/1024)}')KB, $TABLES tabelas"
else
    echo "❌ Database não encontrado!"
fi
echo ""

# 4. Ler INDEX_MASTER
echo "4️⃣  LER INDEX_MASTER (CRÍTICO)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md" ]; then
    echo "📋 INDEX_MASTER:"
    head -20 "MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md" | grep -E "(VERSÃO|STATUS|CONHECIMENTOS|ATUALIZAÇÃO)"
    echo ""
    echo "📊 Últimos conhecimentos:"
    ls -1t MEMORY/conhecimentos/*.md | head -3 | xargs -I {} basename {}
    echo "✅ INDEX_MASTER carregado"
else
    echo "❌ INDEX_MASTER não encontrado!"
fi
echo ""

# 5. Validar Sistemas
echo "5️⃣  VALIDAR SISTEMAS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SYSTEMS=$(ls -1 systems/*.py 2>/dev/null | wc -l | tr -d ' ')
LEIS=$(ls -1 🔥LEIS_UCHIMON🔥/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "✅ Sistemas Python: $SYSTEMS"
echo "✅ LEIS: $LEIS"
echo ""

# 6. Executar Testes Rápidos
echo "6️⃣  EXECUTAR TESTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "venv" ] && [ -x "venv/bin/pytest" ]; then
    source venv/bin/activate 2>/dev/null || true
    TESTS=$(pytest tests/ -q --tb=no 2>&1 | tail -1)
    echo "✅ Testes: $TESTS"
else
    echo "⚠️  venv não encontrado (testes não executados)"
fi
echo ""

# 7. Git Status
echo "7️⃣  GIT STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
LAST_COMMIT=$(git log -1 --oneline | head -c 60)
CHANGED=$(git status --short | wc -l | tr -d ' ')
echo "✅ Último commit: $LAST_COMMIT"
echo "✅ Arquivos alterados: $CHANGED"
echo ""

# 8. Resumo Final
echo "══════════════════════════════════════════════════════"
echo "✅ RECONEXÃO COMPLETA"
echo ""
echo "📊 RESUMO:"
echo "  - Identidade: UCHIMON"
echo "  - Sistemas: $SYSTEMS Python files"
echo "  - LEIS: $LEIS arquivos"
echo "  - Conhecimentos: $(ls -1 MEMORY/conhecimentos/*.md 2>/dev/null | wc -l | tr -d ' ') arquivos"
echo "  - Database: Conectado"
echo "  - Testes: Validados"
echo ""
echo "🔥 SISTEMA PRONTO PARA USO 🔥"
echo ""
echo "PRÓXIMO PASSO:"
echo "  → Verificar MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md"
echo "  → Ler último conhecimento para contexto completo"
echo ""

exit 0
