#!/bin/bash

cd /Users/clubproducoes/Digimundo

clear
echo "════════════════════════════════════════════════════════════"
echo "📤 PUSH PARA GITHUB - VERSÃO SIMPLIFICADA"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🔗 Destino: https://github.com/onestorluiz/Digimundo"
echo "📦 Arquivos: 38.144"
echo "⏱️  Tempo: 5-10 minutos"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Vai pedir:"
echo "  Username: onestorluiz"
echo "  Password: [COLE SEU TOKEN AQUI]"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Iniciando push em 3 segundos..."
sleep 3

git push -u origin triple-core-v2

echo ""
echo "════════════════════════════════════════════════════════════"
if [ $? -eq 0 ]; then
    echo "✅ SUCESSO!"
    echo ""
    echo "Verifique em: https://github.com/onestorluiz/Digimundo"
else
    echo "❌ ERRO!"
    echo ""
    echo "Possíveis causas:"
    echo "  1. Token inválido ou expirado"
    echo "  2. Token sem permissão 'repo'"
    echo "  3. Problemas de conexão"
    echo ""
    echo "Tente criar um novo token em:"
    echo "  https://github.com/settings/tokens/new"
fi
echo "════════════════════════════════════════════════════════════"
