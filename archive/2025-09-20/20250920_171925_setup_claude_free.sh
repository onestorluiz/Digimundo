#!/bin/bash

# 🆓 CONFIGURAR CLAUDE CODE COM SEU PLANO PRO (SEM API KEY!)

echo "🤖 CONFIGURAÇÃO DO CLAUDE CODE (GRÁTIS COM SEU PLANO PRO)"
echo "=========================================================="
echo ""
echo "✨ VOCÊ NÃO PRECISA DE API KEY!"
echo "✨ NÃO PRECISA COMPRAR CRÉDITOS!"
echo "✨ USA O MESMO LOGIN DO CLAUDE.AI!"
echo ""
echo "=========================================================="
echo ""

# Verificar se já está autenticado
echo "🔍 Verificando autenticação..."
AUTH_STATUS=$(npx @anthropic-ai/claude-code auth status 2>&1)

if echo "$AUTH_STATUS" | grep -q "Authenticated"; then
    echo "✅ Você já está autenticado!"
    echo ""
    
    # Testar
    echo "🧪 Testando conexão..."
    TEST=$(echo "Say OK" | npx @anthropic-ai/claude-code --print 2>&1)
    
    if echo "$TEST" | grep -qi "ok"; then
        echo "✅ Claude Code funcionando perfeitamente!"
        echo ""
        echo "🎉 Sistema híbrido pronto para usar!"
    else
        echo "⚠️ Autenticado mas não respondendo"
        echo "Tente fazer login novamente"
    fi
else
    echo "📝 Você precisa fazer login"
    echo ""
    echo "INSTRUÇÕES:"
    echo "-----------"
    echo "1. O comando abaixo abrirá seu navegador"
    echo "2. Faça login com sua conta do Claude.ai"
    echo "   (a mesma que você usa no site)"
    echo "3. Autorize o acesso"
    echo "4. Volte ao terminal"
    echo ""
    echo "Pressione ENTER para abrir o navegador e fazer login..."
    read
    
    # Fazer login
    echo "🌐 Abrindo navegador para login..."
    npx @anthropic-ai/claude-code auth login
    
    echo ""
    echo "✅ Login concluído!"
    echo ""
    
    # Testar
    echo "🧪 Testando conexão..."
    TEST=$(echo "Say OK" | npx @anthropic-ai/claude-code --print 2>&1)
    
    if echo "$TEST" | grep -qi "ok"; then
        echo "✅ Claude Code funcionando!"
        echo ""
        echo "🎉 Sistema híbrido configurado com sucesso!"
    else
        echo "⚠️ Algo deu errado. Tente novamente:"
        echo "npx @anthropic-ai/claude-code auth login"
    fi
fi

echo ""
echo "=========================================================="
echo "📊 COMO FUNCIONA O SISTEMA HÍBRIDO:"
echo ""
echo "• Perguntas simples → Ollama local (rápido, grátis)"
echo "• Perguntas complexas → Claude Pro (qualidade máxima)"
echo "• Tudo automático, sem custos extras!"
echo ""
echo "🚀 Para iniciar o Digimundo:"
echo "   npm run dev"
echo ""
echo "💡 O sistema decide automaticamente quando usar Claude"
echo "   baseado na complexidade da pergunta"
echo ""
echo "✨ Aproveite o poder completo do seu plano Pro!"
echo "=========================================================="