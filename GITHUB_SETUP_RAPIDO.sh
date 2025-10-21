#!/bin/bash
#
# ✅ TUDO JÁ ESTÁ PRONTO!
# Este script só precisa da URL do seu repositório GitHub PRIVADO
#

set -e

clear
echo "============================================================"
echo "🚀 SETUP RÁPIDO - GITHUB PRIVADO"
echo "============================================================"
echo ""
echo "✅ JÁ FIZ PARA VOCÊ:"
echo "  - .gitignore otimizado"
echo "  - 38.144 arquivos commitados"
echo "  - Archive reorganizado (32.977 duplicatas removidas)"
echo "  - Branch: triple-core-v2"
echo ""
echo "============================================================"
echo ""
echo "📋 SIGA ESTES 3 PASSOS:"
echo ""
echo "PASSO 1: Criar repositório PRIVADO no GitHub"
echo "  → Acesse: https://github.com/new"
echo "  → Nome: digimundo"
echo "  → ⚠️  MARQUE: ✓ Private"
echo "  → NÃO adicione README, .gitignore ou licença"
echo "  → Clique em 'Create repository'"
echo ""
read -p "Pressione ENTER quando o repositório estiver criado..."

echo ""
echo "PASSO 2: Cole a URL do repositório"
echo "  (exemplo: https://github.com/seu_usuario/digimundo.git)"
echo ""
read -p "URL: " GITHUB_URL

if [[ -z "$GITHUB_URL" ]]; then
    echo "❌ URL vazia. Cancelado."
    exit 1
fi

echo ""
echo "PASSO 3: Configurando remote e fazendo push..."
echo ""

# Remover remote antigo se existir
git remote remove origin 2>/dev/null || true

# Adicionar novo remote
git remote add origin "$GITHUB_URL"

echo "✅ Remote configurado!"
echo ""
echo "📤 Fazendo push para GitHub..."
echo "   (Pode demorar alguns minutos - são 38.144 arquivos)"
echo ""

# Fazer push
if git push -u origin triple-core-v2; then
    echo ""
    echo "============================================================"
    echo "✅ SUCESSO! REPOSITÓRIO CONFIGURADO!"
    echo "============================================================"
    echo ""
    echo "🔗 URL: $GITHUB_URL"
    echo "🔒 Privado: Sim (só você vê)"
    echo "📦 Arquivos: 38.144 commitados"
    echo "🗂️  Archive: Organizado e otimizado"
    echo ""
    echo "============================================================"
    echo "📝 COMANDOS ÚTEIS:"
    echo "============================================================"
    echo ""
    echo "# Ver status"
    echo "git status"
    echo ""
    echo "# Fazer push futuro"
    echo "git push"
    echo ""
    echo "# Ver remotes"
    echo "git remote -v"
    echo ""
    echo "# Ver histórico"
    echo "git log --oneline -10"
    echo ""
    echo "============================================================"
else
    echo ""
    echo "❌ ERRO no push"
    echo ""
    echo "Possíveis causas:"
    echo "1. Credenciais incorretas"
    echo "2. Repositório não é privado"
    echo "3. URL incorreta"
    echo ""
    echo "Tente novamente ou use token de acesso:"
    echo "  https://github.com/settings/tokens"
    exit 1
fi
