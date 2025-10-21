#!/bin/bash

# Teste rápido da versão natural

echo "🧪 Testando Scripturemon Natural..."
echo ""

# Pergunta simples sobre roteiro
echo "Como aplicar o midpoint em uma série?" | ollama run scripturemon-natural

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Pergunta sobre ele mesmo
echo "Quem é você e qual sua missão?" | ollama run scripturemon-natural