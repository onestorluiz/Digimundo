#!/bin/bash

# 🔑 CONFIGURADOR DE CHAVE DO CLAUDE CODE
# Script para facilitar a configuração da API Key

echo "🤖 CONFIGURAÇÃO DO CLAUDE CODE PARA DIGIMUNDO"
echo "============================================="
echo ""
echo "📝 INSTRUÇÕES:"
echo ""
echo "1. Acesse: https://console.anthropic.com/settings/keys"
echo "2. Clique em 'Create Key'"
echo "3. Dê um nome (ex: 'Digimundo')"
echo "4. Copie a chave que começar com 'sk-ant-api...'"
echo ""
echo "============================================="
echo ""

# Criar diretório de config se não existir
CONFIG_DIR="$HOME/.config/claude-code"
mkdir -p "$CONFIG_DIR"

# Perguntar pela chave
echo "Cole sua API Key do Claude aqui e pressione ENTER:"
echo "(A chave será ocultada por segurança)"
echo ""
read -s -p "API Key: " API_KEY
echo ""

# Validar formato básico da chave
if [[ ! "$API_KEY" =~ ^sk-ant-api ]]; then
    echo "❌ Erro: A chave deve começar com 'sk-ant-api'"
    echo "   Verifique se copiou a chave correta"
    exit 1
fi

# Criar arquivo de configuração
CONFIG_FILE="$CONFIG_DIR/config.json"
cat > "$CONFIG_FILE" << EOF
{
  "apiKey": "$API_KEY",
  "model": "claude-3-5-sonnet-20241022",
  "verbose": false,
  "temperature": 0.7,
  "maxTokens": 4096
}
EOF

# Definir permissões seguras
chmod 600 "$CONFIG_FILE"

echo "✅ Chave configurada com sucesso!"
echo ""

# Testar a configuração
echo "🧪 Testando conexão..."
echo ""

# Criar variável de ambiente temporária
export ANTHROPIC_API_KEY="$API_KEY"

# Teste simples
TEST_RESULT=$(npx @anthropic-ai/claude-code --print "Say OK" 2>&1)

if echo "$TEST_RESULT" | grep -q "OK"; then
    echo "✅ SUCESSO! Claude Code está funcionando!"
    echo ""
    echo "🎉 Sistema híbrido agora está completo!"
    echo ""
    echo "Próximos passos:"
    echo "1. Reinicie o Digimundo: npm run dev"
    echo "2. O sistema detectará automaticamente o Claude"
    echo "3. Aproveite o poder híbrido completo!"
else
    echo "⚠️  Não foi possível validar a chave"
    echo "Possíveis causas:"
    echo "- Chave incorreta"
    echo "- Sem créditos na conta"
    echo "- Problema de conexão"
    echo ""
    echo "Verifique em: https://console.anthropic.com/settings/keys"
fi

echo ""
echo "📁 Configuração salva em: $CONFIG_FILE"
echo ""