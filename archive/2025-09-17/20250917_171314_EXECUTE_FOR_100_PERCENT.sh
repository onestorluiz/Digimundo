#!/bin/bash
#════════════════════════════════════════════════════════════════
# 🔐 SCRIPT PARA ATINGIR 100% DE PROTEÇÃO
#════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         🔐 CONFIGURANDO PROTEÇÃO MÁXIMA 100%              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
PROTECTION_DIR="/Users/clubproducoes/Digimundo/claude_code/protection"

# 1. Limpa autorizações antigas
echo "🧹 Limpando autorizações antigas..."
rm -f "$PROTECTION_DIR/.authorized" "$PROTECTION_DIR/.python_auth" 2>/dev/null

# 2. Configura ACLs com sudo
echo ""
echo "🔐 Configurando ACLs (vai pedir senha)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ACLs principais
sudo chmod +a "everyone deny delete,delete_child,write,append" "$PROTECTED_DIR"

# Protege subdiretórios
for dir in apps bin tests data config; do
    if [ -d "$PROTECTED_DIR/$dir" ]; then
        sudo chmod +a "everyone deny delete,delete_child" "$PROTECTED_DIR/$dir"
    fi
done

# Marca como configurado
echo "ACLS_CONFIGURED=$(date +%s)" > "$PROTECTION_DIR/.acls_configured"

echo "✅ ACLs configuradas!"

# 3. Reinicia o daemon de proteção
echo ""
echo "🔄 Reiniciando daemon de proteção..."
pkill -f "protection_daemon.py" 2>/dev/null
sleep 1
python3 "$PROTECTION_DIR/protection_daemon.py" &
echo "✅ Daemon reiniciado!"

# 4. Garante que o monitor está rodando
echo ""
echo "📊 Iniciando monitor..."
"$PROTECTION_DIR/monitor_background.sh" &
echo "✅ Monitor ativo!"

# 5. Verifica o status final
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Verificando proteção..."
echo ""
sleep 2

# Executa verificação
"$PROTECTION_DIR/verify_maximum_protection.sh"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ✅ CONFIGURAÇÃO COMPLETA!                ║"
echo "║                                                            ║"
echo "║   Para testar a proteção:                                 ║"
echo "║   1. Feche TODOS os terminais                             ║"
echo "║   2. Abra um novo terminal                                ║"
echo "║   3. Tente acessar o diretório protegido                  ║"
echo "║   4. Use 'scripturemon-auth' quando solicitado            ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"