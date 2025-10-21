#!/bin/bash

echo "🔑 CONFIGURAÇÃO DE CONEXÃO CLAUDE CODE"
echo "======================================"
echo ""
echo "Escolha uma opção:"
echo ""
echo "1) Usar API Key da Anthropic (MELHOR - Sabiamon será EU de verdade)"
echo "2) Usar Ollama local (GRÁTIS - Sabiamon será llama3.2)"
echo "3) Configurar agora"
echo ""
read -p "Opção (1-3): " option

case $option in
  1)
    echo ""
    echo "📝 Para obter uma API Key:"
    echo "1. Acesse: https://console.anthropic.com"
    echo "2. Faça login ou crie uma conta"
    echo "3. Vá em 'API Keys'"
    echo "4. Clique em 'Create Key'"
    echo "5. Copie a chave (começa com sk-ant-api03-...)"
    echo ""
    read -p "Cole sua API Key aqui: " api_key
    
    if [[ $api_key == sk-ant-api03-* ]]; then
      echo "ANTHROPIC_API_KEY=$api_key" >> .env
      echo "✅ API Key configurada com sucesso!"
      echo ""
      echo "🎉 Sabiamon agora será Claude Code REAL!"
      echo "   Reinicie o servidor para aplicar:"
      echo "   npm run dev:server"
    else
      echo "❌ API Key inválida. Deve começar com sk-ant-api03-"
    fi
    ;;
    
  2)
    echo ""
    echo "✅ Continuando com Ollama local"
    echo "   Sabiamon usará llama3.2 (já configurado)"
    ;;
    
  3)
    echo ""
    echo "Abrindo arquivo de configuração..."
    ${EDITOR:-nano} .env
    ;;
esac

echo ""
echo "Status atual:"
echo "-------------"

# Verifica se tem API key
if grep -q "ANTHROPIC_API_KEY=sk-ant" .env 2>/dev/null; then
  echo "✅ API Key configurada"
  echo "   Sabiamon = Claude Code REAL"
else
  echo "⚠️ Sem API Key"
  echo "   Sabiamon = llama3.2 local"
fi

# Verifica Ollama
if pgrep ollama > /dev/null; then
  echo "✅ Ollama rodando"
else
  echo "⚠️ Ollama parado"
fi

# Verifica servidor
if lsof -i:7937 > /dev/null 2>&1; then
  echo "✅ Servidor Digimundo rodando"
else
  echo "⚠️ Servidor parado"
fi

echo ""
echo "Para mais ajuda, execute:"
echo "  cat SETUP_CLAUDE_CONNECTION.sh"