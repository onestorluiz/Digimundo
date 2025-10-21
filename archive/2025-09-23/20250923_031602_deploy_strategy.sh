#!/bin/bash
# 🎬 SCRIPTUREMON - Estratégia de Deploy 3 Camadas

echo "════════════════════════════════════════════════"
echo "🎯 SCRIPTUREMON - SISTEMA DE 3 CAMADAS"
echo "════════════════════════════════════════════════"

# 1. Build dos 3 modelos
echo "🔨 Construindo modelos..."

# Hybrid - Para produção (rápido e preciso)
ollama create scripturemon-hybrid -f Modelfile.scripturemon-hybrid
echo "✅ Hybrid criado (produção)"

# V2 - Para análise McKee profunda
ollama create scripturemon-v2 -f Modelfile.scripturemon-v2
echo "✅ V2 criado (McKee puro)"

# Ultimate - Para laboratório e evolução
ollama create scripturemon-ultimate -f Modelfile.scripturemon-ultimate
echo "✅ Ultimate criado (laboratório)"

# 2. Criar aliases para uso fácil
echo ""
echo "🔗 Configurando aliases..."

cat >> ~/.zshrc << 'EOF'

# SCRIPTUREMON - Sistema 3 Camadas
alias script="ollama run scripturemon-hybrid"      # Produção (90% dos casos)
alias script-mckee="ollama run scripturemon-v2"    # Análise McKee profunda
alias script-lab="ollama run scripturemon-ultimate" # Laboratório/Evolução

# Função para escolher modelo baseado no contexto
scripturemon() {
    local prompt="$1"

    # Se pedir meta-learning ou evolução -> ULTIMATE
    if [[ "$prompt" == *"gere prompt"* ]] || [[ "$prompt" == *"meta-learning"* ]]; then
        echo "🧪 Usando ULTIMATE (laboratório)..."
        ollama run scripturemon-ultimate "$prompt"

    # Se pedir análise McKee específica -> V2
    elif [[ "$prompt" == *"McKee"* ]] || [[ "$prompt" == *"controlling idea"* ]]; then
        echo "📚 Usando V2 (McKee puro)..."
        ollama run scripturemon-v2 "$prompt"

    # Caso padrão -> HYBRID
    else
        echo "🎯 Usando HYBRID (produção)..."
        ollama run scripturemon-hybrid "$prompt"
    fi
}
EOF

echo "✅ Aliases configurados"

# 3. Teste rápido dos 3 modelos
echo ""
echo "🧪 Testando modelos..."

TEST_PROMPT="Analise: p.10 - JOHN: 'I quit.' Identifique o valor."

echo "Testing HYBRID..."
echo "$TEST_PROMPT" | timeout 30 ollama run scripturemon-hybrid 2>&1 | head -5

echo ""
echo "Testing V2..."
echo "$TEST_PROMPT" | timeout 30 ollama run scripturemon-v2 2>&1 | head -5

echo ""
echo "Testing ULTIMATE..."
echo "$TEST_PROMPT" | timeout 30 ollama run scripturemon-ultimate 2>&1 | head -5

echo ""
echo "════════════════════════════════════════════════"
echo "✅ SISTEMA 3 CAMADAS INSTALADO!"
echo "════════════════════════════════════════════════"
echo ""
echo "USO RECOMENDADO:"
echo ""
echo "1. 🎯 PRODUÇÃO (90% dos casos):"
echo "   script 'analise página 20-30'"
echo ""
echo "2. 📚 ANÁLISE MCKEE PROFUNDA:"
echo "   script-mckee 'defina controlling idea'"
echo ""
echo "3. 🧪 LABORATÓRIO/EVOLUÇÃO:"
echo "   script-lab 'gere 5 novos prompts para diálogo'"
echo ""
echo "4. 🤖 AUTO-SELEÇÃO:"
echo "   scripturemon 'seu prompt aqui'"
echo ""
echo "DIGIMUNDO PRESENTE 🥷"