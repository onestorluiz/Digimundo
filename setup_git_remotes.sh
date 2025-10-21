#!/bin/bash
#
# Script para configurar git remotes privados
# Opção 1: GitHub privado (nuvem)
# Opção 2: Backup local (HD externo/NAS)
#

set -e

echo "============================================================"
echo "🔒 CONFIGURAÇÃO DE GIT REMOTES PRIVADOS"
echo "============================================================"
echo ""

# Diretório do projeto
PROJECT_DIR="/Users/clubproducoes/Digimundo"
cd "$PROJECT_DIR"

echo "📂 Projeto: $PROJECT_DIR"
echo ""

# Verificar se já tem remotes
echo "🔍 Verificando remotes existentes..."
if git remote -v | grep -q origin; then
    echo "⚠️  Remote 'origin' já existe:"
    git remote -v | grep origin
    echo ""
    read -p "❓ Deseja substituir? [s/N]: " replace
    if [[ ! "$replace" =~ ^[Ss]$ ]]; then
        echo "❌ Cancelado pelo usuário"
        exit 0
    fi
    git remote remove origin
fi

echo ""
echo "Escolha o tipo de remote:"
echo "1) GitHub PRIVADO (gratuito, recomendado)"
echo "2) Backup LOCAL (HD externo/NAS)"
echo "3) AMBOS (GitHub + Backup Local)"
echo ""
read -p "Opção [1-3]: " option

case $option in
    1)
        echo ""
        echo "📋 INSTRUÇÕES PARA GITHUB PRIVADO:"
        echo ""
        echo "1. Acesse: https://github.com/new"
        echo "2. Nome do repositório: digimundo"
        echo "3. ⚠️  Marque: ✓ Private (IMPORTANTE!)"
        echo "4. NÃO adicione README, .gitignore ou licença"
        echo "5. Clique em 'Create repository'"
        echo ""
        read -p "Pressione ENTER quando o repositório estiver criado..."
        echo ""
        read -p "Cole a URL do repositório (https://github.com/...): " github_url

        git remote add origin "$github_url"

        echo ""
        echo "✅ Remote 'origin' configurado!"
        echo ""
        echo "🔑 IMPORTANTE: Configure seu token de acesso"
        echo "1. Vá em: https://github.com/settings/tokens"
        echo "2. Clique em 'Generate new token (classic)'"
        echo "3. Marque: repo (Full control)"
        echo "4. Copie o token gerado"
        echo ""
        read -p "Pressione ENTER para fazer o primeiro push..."

        echo ""
        echo "📤 Fazendo push inicial..."
        git push -u origin triple-core-v2

        echo ""
        echo "✅ Repositório privado no GitHub configurado!"
        echo "🔗 URL: $github_url"
        ;;

    2)
        echo ""
        echo "📋 CONFIGURAÇÃO DE BACKUP LOCAL:"
        echo ""
        read -p "Caminho do HD externo/NAS (ex: /Volumes/MeuHD): " backup_path

        if [ ! -d "$backup_path" ]; then
            echo "❌ Caminho não encontrado: $backup_path"
            exit 1
        fi

        BACKUP_REPO="$backup_path/git-backups/digimundo.git"
        echo ""
        echo "📁 Criando repositório bare em: $BACKUP_REPO"

        mkdir -p "$(dirname "$BACKUP_REPO")"
        git init --bare "$BACKUP_REPO"

        git remote add backup "$BACKUP_REPO"

        echo ""
        echo "📤 Fazendo push inicial..."
        git push backup triple-core-v2

        echo ""
        echo "✅ Backup local configurado!"
        echo "📂 Local: $BACKUP_REPO"
        ;;

    3)
        echo ""
        echo "📋 CONFIGURAÇÃO DUPLA: GitHub + Backup Local"
        echo ""

        # GitHub
        echo "=== GITHUB ==="
        echo "1. Acesse: https://github.com/new"
        echo "2. Nome: digimundo"
        echo "3. ⚠️  Marque: ✓ Private"
        echo "4. Clique em 'Create repository'"
        echo ""
        read -p "Pressione ENTER quando pronto..."
        echo ""
        read -p "Cole a URL do GitHub: " github_url

        git remote add origin "$github_url"

        # Backup Local
        echo ""
        echo "=== BACKUP LOCAL ==="
        read -p "Caminho do HD externo/NAS: " backup_path

        if [ ! -d "$backup_path" ]; then
            echo "❌ Caminho não encontrado: $backup_path"
            exit 1
        fi

        BACKUP_REPO="$backup_path/git-backups/digimundo.git"
        mkdir -p "$(dirname "$BACKUP_REPO")"
        git init --bare "$BACKUP_REPO"
        git remote add backup "$BACKUP_REPO"

        # Push para ambos
        echo ""
        echo "📤 Fazendo push para GitHub..."
        git push -u origin triple-core-v2

        echo ""
        echo "📤 Fazendo push para backup local..."
        git push backup triple-core-v2

        echo ""
        echo "✅ Ambos configurados!"
        echo "🔗 GitHub: $github_url"
        echo "📂 Local: $BACKUP_REPO"
        ;;

    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "📊 STATUS DOS REMOTES"
echo "============================================================"
git remote -v

echo ""
echo "============================================================"
echo "📝 COMANDOS ÚTEIS"
echo "============================================================"
echo ""
echo "# Ver status do git"
echo "git status"
echo ""
echo "# Fazer push para o remote principal"
echo "git push origin triple-core-v2"
echo ""

if git remote | grep -q backup; then
    echo "# Fazer push para backup local"
    echo "git push backup triple-core-v2"
    echo ""
fi

echo "# Push para todos os remotes de uma vez"
echo "git push --all"
echo ""
echo "# Ver histórico"
echo "git log --oneline -10"
echo ""

echo "============================================================"
echo "✅ CONFIGURAÇÃO CONCLUÍDA!"
echo "============================================================"
echo ""
echo "⚠️  LEMBRE-SE:"
echo "- Repositório GitHub é PRIVADO (só você vê)"
echo "- Faça commits regularmente: git add . && git commit -m 'mensagem'"
echo "- Faça push regularmente: git push"
echo ""
