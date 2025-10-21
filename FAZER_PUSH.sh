#!/bin/bash
#
# ✅ Remote já está configurado!
# Só execute este script para fazer o push
#

cd /Users/clubproducoes/Digimundo

echo "============================================================"
echo "📤 FAZENDO PUSH PARA GITHUB"
echo "============================================================"
echo ""
echo "🔗 Repositório: https://github.com/onestorluiz/Digimundo"
echo "📦 Arquivos: 38.144"
echo "⏱️  Tempo estimado: 5-10 minutos"
echo ""
echo "Vai pedir suas credenciais do GitHub:"
echo "  - Username: onestorluiz"
echo "  - Password: Use um TOKEN (não a senha normal!)"
echo ""
echo "Como criar token:"
echo "  1. Vá em: https://github.com/settings/tokens"
echo "  2. Clique: Generate new token (classic)"
echo "  3. Marque: ✓ repo"
echo "  4. Copie o token"
echo "  5. Cole aqui como senha"
echo ""
echo "============================================================"
echo ""

git push -u origin triple-core-v2

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ SUCESSO! REPOSITÓRIO NO GITHUB CONFIGURADO!"
    echo "============================================================"
    echo ""
    echo "🔗 URL: https://github.com/onestorluiz/Digimundo"
    echo "🔒 Privado: Sim"
    echo "📦 Arquivos: 38.144"
    echo ""
    echo "Próximos comandos úteis:"
    echo "  git status    - Ver mudanças"
    echo "  git push      - Fazer push futuro"
    echo "  git log       - Ver histórico"
    echo ""
else
    echo ""
    echo "❌ Erro no push"
    echo ""
    echo "Verifique:"
    echo "  - Usou o TOKEN como senha (não a senha normal)"
    echo "  - Repositório está privado"
    echo "  - Tem permissão no repositório"
    echo ""
fi
