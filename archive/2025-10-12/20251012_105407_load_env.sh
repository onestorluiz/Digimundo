#!/bin/bash
# Script para carregar variáveis de ambiente do arquivo .env
#
# Uso:
#   source load_env.sh
#   ou
#   . load_env.sh

if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Variáveis de ambiente carregadas do .env"
    echo "   OPENAI_API_KEY configurada"
else
    echo "❌ Arquivo .env não encontrado!"
    echo "   Crie o arquivo .env com: OPENAI_API_KEY='sua-chave-aqui'"
fi
