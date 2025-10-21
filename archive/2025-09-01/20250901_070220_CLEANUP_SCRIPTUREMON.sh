#!/bin/bash

# 🧹 SCRIPT DE LIMPEZA SEGURA DO SCRIPTUREMON
# Mata todos os processos e limpa recursos

echo "🧹 Limpando processos do Scripturemon..."

# 1. Matar Redis
echo "   ↳ Parando Redis..."
redis-cli shutdown 2>/dev/null || true
pkill -f redis-server 2>/dev/null || true

# 2. Matar Ollama
echo "   ↳ Parando Ollama..."
pkill -f "ollama serve" 2>/dev/null || true
pkill -f ollama 2>/dev/null || true

# 3. Matar processos Python relacionados
echo "   ↳ Parando processos Python..."
pkill -f scripturemon 2>/dev/null || true
pkill -f SCRIPTUREMON 2>/dev/null || true
pkill -f "python.*Digimundo" 2>/dev/null || true

# 4. Limpar portas
echo "   ↳ Liberando portas..."
lsof -ti:6379 | xargs kill -9 2>/dev/null || true
lsof -ti:8008 | xargs kill -9 2>/dev/null || true
lsof -ti:11434 | xargs kill -9 2>/dev/null || true

# 5. Limpar arquivos temporários
echo "   ↳ Limpando temporários..."
rm -f /tmp/scripturemon* 2>/dev/null || true
rm -f /tmp/ollama* 2>/dev/null || true

# 6. Verificar status
echo ""
echo "📊 Status após limpeza:"
echo "   Redis: $(pgrep redis-server > /dev/null && echo '❌ Ainda rodando' || echo '✅ Parado')"
echo "   Ollama: $(pgrep ollama > /dev/null && echo '❌ Ainda rodando' || echo '✅ Parado')"
echo "   Python/Scripturemon: $(pgrep -f scripturemon > /dev/null && echo '❌ Ainda rodando' || echo '✅ Parado')"

echo ""
echo "✅ Limpeza concluída!"
echo ""
echo "⚠️  IMPORTANTE: Se o Mac travar no boot novamente:"
echo "   1. Segure Command+R durante o boot para entrar no Recovery Mode"
echo "   2. Abra o Terminal do Recovery"
echo "   3. Execute: csrutil disable (temporariamente)"
echo "   4. Reinicie e delete a pasta /Users/clubproducoes/Digimundo/scripturemon-validation"
echo "   5. Execute: csrutil enable (reativar proteção)"