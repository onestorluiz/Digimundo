#!/bin/bash

# =================================================================
# SCRIPTUREMON - INICIALIZAÇÃO COMPLETA
# =================================================================
# Garante que TUDO esteja rodando antes de iniciar
# =================================================================

echo "🎬 INICIANDO SISTEMA SCRIPTUREMON COMPLETO..."

# 1. Garantir que Ollama está rodando
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Iniciando servidor Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# 2. Verificar modelos essenciais
echo "🤖 Verificando modelos..."
for model in "llama3.2:3b" "mistral:latest"; do
    if ! ollama list | grep -q "${model%:*}"; then
        echo "  📥 Baixando $model..."
        ollama pull "$model"
    fi
done

# 3. Verificar modelo Scripturemon
if ! ollama list | grep -q "scripturemon-maestro"; then
    echo "  🧬 Criando Scripturemon Maestro..."
    MODELFILE="/Users/clubproducoes/Digimundo/digimons/scripturemon/scripturemon_maestro_brutal.modelfile"
    if [ -f "$MODELFILE" ]; then
        ollama create scripturemon-maestro -f "$MODELFILE"
    fi
fi

# 4. Processar PDFs se necessário
CHROMA_DIR="/Users/clubproducoes/Digimundo/digimons/scripturemon/conhecimento/chroma"
if [ ! -d "$CHROMA_DIR" ] || [ -z "$(ls -A $CHROMA_DIR 2>/dev/null)" ]; then
    echo "📚 Processando biblioteca de roteiros (primeira vez)..."
    echo "   ⚠️ Isso pode demorar ~30 minutos"
    
    cd /Users/clubproducoes/Digimundo/digimons/scripturemon
    source venv/bin/activate
    python process_all_pdfs.py 2>/dev/null || echo "⚠️ Processamento manual necessário"
fi

# 5. Iniciar Scripturemon
echo ""
echo "✅ SISTEMA PRONTO!"
echo ""
exec ~/bin/scripturemon "$@"