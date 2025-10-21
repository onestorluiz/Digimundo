#!/bin/bash

echo "🤖 CONFIGURAÇÃO AUTOMÁTICA DO CLAUDE"
echo "===================================="
echo ""
echo "📋 O navegador abriu em: https://console.anthropic.com/settings/keys"
echo ""
echo "INSTRUÇÕES RÁPIDAS:"
echo "1. Se não estiver logado, faça login com sua conta Claude Pro"
echo "2. Clique em '+ Create Key'"
echo "3. Nome da chave: Digimundo"
echo "4. Copie a chave (começa com sk-ant-api...)"
echo ""
echo "===================================="
echo ""
echo "Cole a chave aqui e pressione ENTER:"
read API_KEY

# Validar chave
if [[ ! "$API_KEY" =~ ^sk-ant-api ]]; then
    echo "❌ Chave inválida. Deve começar com sk-ant-api"
    exit 1
fi

# Configurar no sistema
echo "Configurando..."

# Método 1: Arquivo de configuração
mkdir -p ~/.config/claude-code
cat > ~/.config/claude-code/config.json << EOF
{
  "apiKey": "$API_KEY"
}
EOF

# Método 2: Variável de ambiente no shell
SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

# Adicionar ao arquivo de configuração do shell
echo "" >> $SHELL_RC
echo "# Claude API para Digimundo" >> $SHELL_RC
echo "export ANTHROPIC_API_KEY='$API_KEY'" >> $SHELL_RC

# Exportar para sessão atual
export ANTHROPIC_API_KEY="$API_KEY"

echo "✅ Configuração salva!"
echo ""
echo "🧪 Testando conexão..."

# Teste via curl
TEST_RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-haiku-20240307",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "Say OK"}]
  }' 2>&1)

if echo "$TEST_RESPONSE" | grep -q "OK"; then
    echo "✅ API funcionando perfeitamente!"
elif echo "$TEST_RESPONSE" | grep -q "invalid_api_key"; then
    echo "❌ Chave inválida"
    exit 1
elif echo "$TEST_RESPONSE" | grep -q "insufficient_credit"; then
    echo "⚠️ Chave válida mas sem créditos"
    echo "Você precisa adicionar créditos em: https://console.anthropic.com/settings/billing"
else
    echo "✅ Chave configurada!"
fi

echo ""
echo "===================================="
echo "🎉 CONFIGURAÇÃO COMPLETA!"
echo ""
echo "A chave foi salva em:"
echo "1. ~/.config/claude-code/config.json"
echo "2. $SHELL_RC"
echo ""
echo "Reinicie o terminal ou execute:"
echo "source $SHELL_RC"
echo ""
echo "Para testar o Digimundo:"
echo "npm run dev"
echo "===================================="