#!/bin/bash

# SCRIPT CORRIGIDO PARA INICIAR DIGIMUNDO SEM LOOP
# Criado em: 16/08/2025

echo "🚀 Iniciando Digimundo (Versão Corrigida)..."

# Limpar processos antigos
pkill -f "Electron.*digimundo" 2>/dev/null
pkill -f "node.*digimundo" 2>/dev/null
sleep 1

# Ir para o diretório
cd /Users/clubproducoes/Digimundo/digimundo_starter

# Verificar dependências
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    npm install
fi

# Iniciar aplicação
echo "✨ Iniciando aplicação..."
npm run dev

echo "✅ Digimundo iniciado com sucesso!"