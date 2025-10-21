#!/bin/bash
#════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DE ACLs COM SUDO - PROTEÇÃO MÁXIMA
#════════════════════════════════════════════════════════════════

echo "🔐 CONFIGURANDO ACLs DE PROTEÇÃO MÁXIMA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Este script precisa de permissões de administrador (sudo)"
echo "Você será solicitado a digitar sua senha do macOS"
echo ""

PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"

# 1. Configura ACLs para negar exclusão
echo "📁 Protegendo diretório principal..."
sudo chmod +a "everyone deny delete,delete_child,write,append" "$PROTECTED_DIR"

# 2. Protege subdiretórios importantes
echo "📂 Protegendo subdiretórios..."
for dir in apps bin tests data config; do
    if [ -d "$PROTECTED_DIR/$dir" ]; then
        sudo chmod +a "everyone deny delete,delete_child" "$PROTECTED_DIR/$dir"
        echo "   ✅ $dir protegido"
    fi
done

# 3. Protege arquivos críticos
echo "📄 Protegendo arquivos críticos..."
for file in "$PROTECTED_DIR"/*.py "$PROTECTED_DIR"/*.sh "$PROTECTED_DIR"/*.json; do
    if [ -f "$file" ]; then
        sudo chmod +a "everyone deny delete,write" "$file" 2>/dev/null
    fi
done

# 4. Adiciona proteção especial para binários
echo "🔒 Proteção especial para executáveis..."
if [ -d "$PROTECTED_DIR/bin" ]; then
    sudo chmod +a "everyone deny delete,write,append" "$PROTECTED_DIR/bin/"* 2>/dev/null
fi

# 5. Cria flag de ACLs configuradas
echo "ACLS_CONFIGURED=$(date +%s)" | sudo tee /Users/clubproducoes/Digimundo/claude_code/protection/.acls_configured > /dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ACLs CONFIGURADAS COM SUCESSO!"
echo ""
echo "Proteções aplicadas:"
echo "  • Bloqueio contra exclusão de arquivos"
echo "  • Bloqueio contra modificação não autorizada"
echo "  • Proteção de subdiretórios críticos"
echo "  • Proteção especial para executáveis"
echo ""
echo "Para verificar as ACLs use: ls -le $PROTECTED_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"