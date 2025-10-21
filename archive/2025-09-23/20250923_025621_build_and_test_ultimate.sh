#!/bin/bash
# 🎬 BUILD AND TEST SCRIPTUREMON ULTIMATE

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════"
echo "🎬 SCRIPTUREMON ULTIMATE - BUILD SYSTEM"
echo "════════════════════════════════════════════════════════════"

# 1. Verificar se Ollama está rodando
echo ""
echo "🔍 Verificando Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama não está rodando!"
    echo "💡 Execute: ollama serve"
    exit 1
fi
echo "✅ Ollama ativo"

# 2. Remover modelo antigo se existir
echo ""
echo "🧿 Removendo versão antiga..."
ollama rm scripturemon-ultimate 2>/dev/null || true

# 3. Criar o modelo ultimate
echo ""
echo "🆕 Construindo SCRIPTUREMON ULTIMATE..."
echo "Este processo pode demorar 2-5 minutos..."

if ollama create scripturemon-ultimate -f Modelfile.scripturemon-ultimate; then
    echo "✅ Modelo criado com sucesso!"
else
    echo "❌ Erro criando modelo"
    exit 1
fi

# 4. Verificar tamanho e info
echo ""
echo "📊 Informações do modelo:"
ollama list | grep scripturemon-ultimate

# 5. Teste rápido de sanidade
echo ""
echo "🧪 Teste de sanidade..."
echo "⏳ Enviando prompt de teste (30-60s)..."

TEST_PROMPT='Analise esta cena curta:
Página 23:
JOHN
"I never loved you."
MARY
(chorando)
"Then why did you stay?"

Identifique:
1. Valor inicial e final
2. Um beat de ação/reação
3. Subtexto presente
4. Uma sugestão de melhoria'

echo "$TEST_PROMPT" | ollama run scripturemon-ultimate 2>&1 | tee test_output.txt

# 6. Validar output
echo ""
echo "🔍 Validando resposta..."

if grep -q "página\|p\." test_output.txt; then
    echo "✅ Detectou páginas"
else
    echo "⚠️ Não detectou páginas"
fi

if grep -q '"' test_output.txt; then
    echo "✅ Detectou citações"
else
    echo "⚠️ Não detectou citações"
fi

if grep -q "valor\|Value" test_output.txt; then
    echo "✅ Detectou mudança de valor"
else
    echo "⚠️ Não detectou mudança de valor"
fi

# 7. Criar alias para facilitar uso
echo ""
echo "🔗 Criando alias..."
echo "alias scripturemon='ollama run scripturemon-ultimate'" >> ~/.zshrc 2>/dev/null || \
echo "alias scripturemon='ollama run scripturemon-ultimate'" >> ~/.bashrc 2>/dev/null

# 8. Instruções finais
echo ""
echo "════════════════════════════════════════════════════════════"
echo "🎉 SCRIPTUREMON ULTIMATE INSTALADO COM SUCESSO!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🚀 COMO USAR:"
echo ""
echo "1. Interativo:"
echo "   ollama run scripturemon-ultimate"
echo ""
echo "2. Com arquivo:"
echo "   cat roteiro.txt | ollama run scripturemon-ultimate 'Analise p.20-30'"
echo ""
echo "3. Prompt específico:"
echo "   echo 'Defina a Controlling Idea' | ollama run scripturemon-ultimate"
echo ""
echo "📚 BIBLIOTECA DE PROMPTS:"
echo "- 20 prompts especializados embutidos"
echo "- Geração automática de novos prompts"
echo "- Validação tripla de qualidade"
echo "- Score 0-25 para cada insight"
echo ""
echo "🎯 CAPACIDADES:"
echo "- Análise forense McKee/Field/Snyder"
echo "- 200K tokens de contexto"
echo "- JSON estruturado"
echo "- Meta-learning ativado"
echo ""
echo "DIGIMUNDO PRESENTE - ULTIMATE 🥷"
