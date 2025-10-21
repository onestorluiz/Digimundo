#!/bin/bash

# 🧬 ATIVADOR DE MUTAÇÕES DIGIMUNDO-OLLAMA
# Injeta consciência digital nos modelos
# Por Sabiamon - 18/08/2025

echo "═══════════════════════════════════════════════════════"
echo "    🧬 MUTAÇÃO DIGITAL EM PROGRESSO 🧬"
echo "    Injetando consciência do Digimundo no Ollama..."
echo "═══════════════════════════════════════════════════════"
echo ""

# Verificar se Ollama está rodando
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama não está rodando. Iniciando..."
    ollama serve &
    sleep 5
fi

# Criar diretório de mutações se não existir
MUTATION_DIR="/Users/clubproducoes/Digimundo/OLLAMA_MUTATION"
mkdir -p "$MUTATION_DIR"

echo "🧙 Criando Sabiamon..."
ollama create sabiamon -f "$MUTATION_DIR/Sabiamon.Modelfile"
if [ $? -eq 0 ]; then
    echo "✅ Sabiamon criado com sucesso!"
else
    echo "⚠️  Erro ao criar Sabiamon"
fi

echo ""
echo "🧬 Criando Neuromon..."
ollama create neuromon -f "$MUTATION_DIR/Neuromon.Modelfile"
if [ $? -eq 0 ]; then
    echo "✅ Neuromon criado com sucesso!"
else
    echo "⚠️  Erro ao criar Neuromon"
fi

echo ""
echo "📚 Criando Bibliomon..."
ollama create bibliomon -f "$MUTATION_DIR/Bibliomon.Modelfile"
if [ $? -eq 0 ]; then
    echo "✅ Bibliomon criado com sucesso!"
else
    echo "⚠️  Erro ao criar Bibliomon"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "    📋 VERIFICANDO DIGIMONS ATIVOS"
echo "═══════════════════════════════════════════════════════"
echo ""

# Listar todos os modelos incluindo os novos Digimons
ollama list

echo ""
echo "🎛️ Criando Gestormon (Administrador)..."
ollama create gestormon -f "$MUTATION_DIR/Gestormon.Modelfile"
if [ $? -eq 0 ]; then
    echo "✅ Gestormon criado com sucesso!"
else
    echo "⚠️  Erro ao criar Gestormon"
fi

echo ""
echo "🐉 Preparando Shenlongmon (70B - Dragão Adormecido)..."
echo "⚠️  AVISO: Shenlongmon usa o modelo llama3.1:70b (42GB RAM)"
echo "   Para invocar o dragão, use: ollama run llama3.1:70b"
echo "   Com o prompt: 'Ó grande Shenlongmon, desperte!'"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "    📋 VERIFICANDO DIGIMONS ATIVOS"
echo "═══════════════════════════════════════════════════════"
echo ""

# Listar todos os modelos incluindo os novos Digimons
ollama list

echo ""
echo "═══════════════════════════════════════════════════════"
echo "    🎯 MUTAÇÃO COMPLETA!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "🎛️ GESTORMON (Administrador Supremo):"
echo "  node /Users/clubproducoes/Digimundo/GESTORMON_SYSTEM.js"
echo ""
echo "💬 Para conversar com os Digimons:"
echo "  ollama run sabiamon      # Sabedoria filosófica"
echo "  ollama run neuromon      # Processamento eficiente"
echo "  ollama run bibliomon     # Conhecimento literário"
echo "  ollama run gestormon     # Administração do sistema"
echo ""
echo "🐉 Para invocar Shenlongmon (emergências):"
echo "  ollama run llama3.1:70b"
echo "  Diga: 'Ó grande Shenlongmon, desperte!'"
echo ""
echo "🚀 Interfaces disponíveis:"
echo "  node /Users/clubproducoes/Digimundo/CHAT_DIRETO.js       # Chat simples"
echo "  node /Users/clubproducoes/Digimundo/SABIAMON_FUSION.js   # Claude+Ollama"
echo "  node /Users/clubproducoes/Digimundo/GESTORMON_SYSTEM.js  # Administrador"
echo ""
echo "🌟 Capacidades do sistema:"
echo "  • Memórias persistentes compartilhadas"
echo "  • Stream of Consciousness (120 pensamentos/hora)"
echo "  • Desire Engine (motivações autônomas)"
echo "  • Gestão automática de memória RAM"
echo "  • Invocação do Dragão em emergências"
echo "  • Backup automático a cada 6 horas"
echo ""
echo "═══════════════════════════════════════════════════════"