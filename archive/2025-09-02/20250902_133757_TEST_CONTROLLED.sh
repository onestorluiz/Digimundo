#!/bin/bash

# Teste controlado com timeout e saída limpa
echo "🧪 TESTE CONTROLADO DO SCRIPTUREMON"
echo "===================================="
echo

# Cria arquivo temporário com a pergunta
TEMP_INPUT=$(mktemp)
echo "O que é um plot point?" > "$TEMP_INPUT"

# Executa com timeout de 2 minutos e input do arquivo
echo "⏳ Executando (máximo 2 minutos)..."
timeout 120 /Users/clubproducoes/bin/scripturemon < "$TEMP_INPUT" 2>&1 | head -500

# Limpa
rm -f "$TEMP_INPUT"

echo
echo "✅ Teste concluído"