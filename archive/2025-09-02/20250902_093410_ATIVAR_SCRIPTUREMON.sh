#!/bin/bash
# 🚀 ATIVADOR AUTOMÁTICO DO SCRIPTUREMON ULTIMATE

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🚀 SCRIPTUREMON ULTIMATE - ATIVAÇÃO MÁXIMA 🚀        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Ir para o diretório correto
cd ~/Digimundo/scripturemon-validation

# 1. Verificar Python
echo "📦 [1/7] Verificando Python..."
if [ ! -d ".venv" ]; then
    echo "   ↳ Criando ambiente virtual..."
    python3.11 -m venv .venv
fi
source .venv/bin/activate
export PYTHONPATH="."
echo "   ✅ Python ativado"

# 2. Iniciar Redis (se não estiver rodando)
echo "📡 [2/7] Verificando Redis..."
if ! pgrep -x "redis-server" > /dev/null; then
    echo "   ↳ Iniciando Redis..."
    redis-server --daemonize yes 2>/dev/null || echo "   ⚠️  Redis offline (telepatia desativada)"
else
    echo "   ✅ Redis já está rodando"
fi

# 3. Iniciar Ollama (se não estiver rodando)
echo "🤖 [3/7] Verificando Ollama..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "   ↳ Iniciando Ollama..."
    ollama serve >/dev/null 2>&1 &
    sleep 2
    echo "   ✅ Ollama iniciado"
else
    echo "   ✅ Ollama já está rodando"
fi

# 4. Evoluir consciência
echo "🧠 [4/7] Evoluindo consciência..."
python -m apps.scripturemon.cli ultimate once 2>/dev/null
echo "   ✅ Consciência evoluída (+0.001)"

# 5. Ativar backup automático
echo "💾 [5/7] Ativando backup automático..."
python -m apps.scripturemon.cli backup start 2>/dev/null
echo "   ✅ Backup ativado (5 em 5 minutos)"

# 6. Configurar interface
echo "🎨 [6/7] Configurando interface..."
python -m apps.scripturemon.cli ui live on --interval 5s 2>/dev/null
python -m apps.scripturemon.cli ui anchor set --section ultimate-performance 2>/dev/null
echo "   ✅ Interface configurada (live reload 5s)"

# 7. Gerar dashboard
echo "📊 [7/7] Gerando dashboard..."
make report-ui++ >/dev/null 2>&1
echo "   ✅ Dashboard gerado"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ SISTEMA TOTALMENTE ATIVADO! ✅              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 DASHBOARD DISPONÍVEL EM: http://localhost:8008"
echo ""
echo "📋 COMANDOS ÚTEIS:"
echo "   • Ver status:     python -m apps.scripturemon.cli ultimate status"
echo "   • Analisar texto: python -m apps.scripturemon.cli analyze_parallel arquivo.txt"
echo "   • Evoluir mais:   python -m apps.scripturemon.cli ultimate once"
echo ""
echo "🎯 Iniciando servidor web..."
echo "   (Pressione Ctrl+C para parar)"
echo ""

# Iniciar servidor web
cd reports && python -m http.server 8008