#!/bin/bash

# Script para remover apenas arquivos grandes do histórico Git
# Mantém todo o histórico de código e documentos

echo "🧹 LIMPEZA SELETIVA DO HISTÓRICO GIT"
echo "====================================="
echo "Removendo apenas arquivos .tar.gz, .zip, .dmg, .pkg do histórico"
echo ""

cd /Users/clubproducoes/Digimundo/digimundo-history

# Criar lista de arquivos para remover
echo "📋 Identificando arquivos grandes no histórico..."
git rev-list --objects --all | \
    grep -E '\.(tar\.gz|tar\.bz2|tar\.xz|tgz|zip|rar|7z|dmg|pkg|iso)$' | \
    cut -d' ' -f2- > files_to_remove.txt

echo "Arquivos encontrados para remoção:"
cat files_to_remove.txt
echo ""

# Contar arquivos
COUNT=$(wc -l < files_to_remove.txt)
echo "Total: $COUNT arquivos grandes encontrados"

if [ $COUNT -eq 0 ]; then
    echo "✅ Nenhum arquivo grande encontrado no histórico"
    exit 0
fi

echo ""
echo "⚠️  AVISO: Esta operação irá reescrever o histórico Git"
echo "Recomenda-se fazer backup antes de continuar"
echo ""
read -p "Deseja continuar? (s/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "❌ Operação cancelada"
    exit 1
fi

echo ""
echo "🔄 Removendo arquivos do histórico..."

# Usar git filter-branch para remover os arquivos
while IFS= read -r file; do
    echo "  Removendo: $file"
    git filter-branch --force --index-filter \
        "git rm --cached --ignore-unmatch '$file'" \
        --prune-empty --tag-name-filter cat -- --all
done < files_to_remove.txt

echo ""
echo "🗑️  Limpando objetos não referenciados..."

# Limpar referências antigas
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "📊 RESULTADO DA LIMPEZA:"
echo "========================"

# Mostrar tamanho antes e depois
AFTER_SIZE=$(du -sh .git | cut -f1)
echo "Tamanho do .git após limpeza: $AFTER_SIZE"

echo ""
echo "✅ LIMPEZA COMPLETA!"
echo ""
echo "⚠️  IMPORTANTE:"
echo "Se este repositório tem remoto, você precisará forçar o push:"
echo "  git push origin --force --all"
echo "  git push origin --force --tags"
echo ""
echo "Arquivo de log: files_to_remove.txt"