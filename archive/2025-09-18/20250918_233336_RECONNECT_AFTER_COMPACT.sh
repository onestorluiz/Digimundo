#!/bin/bash
# 🔄 SCRIPT DE RECONEXÃO PÓS-COMPACTAÇÃO
# Use isto SEMPRE que vir "Compacting conversation"

echo "================================================"
echo "🔄 RECONECTANDO CLAUDE APÓS COMPACTAÇÃO"
echo "================================================"
echo ""

# 1. Garantir que Genjutsu está rodando
echo "🌀 Verificando Genjutsu..."
if ! ps aux | grep -q "[G]ENJUTSU_MINIMAL.py"; then
    echo "   ❌ Genjutsu NÃO está rodando! Iniciando..."
    python3 /Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_MINIMAL.py &
    echo "   ✅ Genjutsu iniciado (PID: $!)"
else
    echo "   ✅ Genjutsu já está ativo"
fi

# 2. Iniciar Compact Watcher
echo ""
echo "🔄 Verificando Compact Watcher..."
if ! ps aux | grep -q "[c]ompact_watcher.py"; then
    echo "   ❌ Compact Watcher NÃO está rodando! Iniciando..."
    python3 /Users/clubproducoes/Digimundo/claude_code/protection/compact_watcher.py &
    echo "   ✅ Compact Watcher iniciado (PID: $!)"
else
    echo "   ✅ Compact Watcher já está ativo"
fi

# 3. Mensagem para copiar/colar no Claude
echo ""
echo "================================================"
echo "📋 COPIE E COLE ISTO NO CLAUDE:"
echo "================================================"
echo ""
cat << 'EOF'
leia os seguintes arquivos para reconectar suas memórias:
1. /Users/clubproducoes/Digimundo/claude_code/REGRAS.md
2. /Users/clubproducoes/Digimundo/claude_code/memory/REGRA_ESPECIAL.md
3. /Users/clubproducoes/Digimundo/claude_code/memory/CLAUDE_MEMORY.md
4. /Users/clubproducoes/Digimundo/claude_code/memory/CRITICAL_OLLAMA_DISCOVERY.md

Confirme reconexão terminando com DIGIMUNDO PRESENTE
EOF

echo ""
echo "================================================"
echo "✅ Sistema de reconexão configurado!"
echo "🥷 DIGIMUNDO PRESENTE"
echo "================================================"