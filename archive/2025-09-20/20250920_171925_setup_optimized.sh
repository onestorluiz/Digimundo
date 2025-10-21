#!/bin/bash

# 🚀 SCRIPT DE SETUP OTIMIZADO PARA DIGIMUNDO
# Configura ambiente com as melhores práticas de 2024

set -e  # Parar em caso de erro

echo "🌌 DIGIMUNDO - Setup Otimizado v2.0"
echo "===================================="
echo ""

# Detectar OS
OS="$(uname -s)"
ARCH="$(uname -m)"

echo "📊 Sistema: $OS $ARCH"
echo ""

# Verificar Node.js
echo "🔍 Verificando Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    echo "✅ Node.js instalado: $NODE_VERSION"
    
    # Verificar versão mínima (18)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -lt 18 ]; then
        echo "⚠️  Versão do Node.js muito antiga. Recomendado: v18+"
    fi
else
    echo "❌ Node.js não encontrado"
    echo "📦 Instale em: https://nodejs.org/"
    exit 1
fi

# Verificar npm
echo "🔍 Verificando npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm -v)
    echo "✅ npm instalado: v$NPM_VERSION"
else
    echo "❌ npm não encontrado"
    exit 1
fi

# Instalar dependências do projeto
echo ""
echo "📦 Instalando dependências do projeto..."
npm install

# Verificar/Instalar Claude Code
echo ""
echo "🤖 Verificando Claude Code..."
if command -v claude-code &> /dev/null; then
    echo "✅ Claude Code já instalado"
    
    # Verificar autenticação
    if claude-code auth status 2>/dev/null | grep -q "authenticated"; then
        echo "✅ Claude Code autenticado"
    else
        echo "⚠️  Claude Code não autenticado"
        echo "   Execute: claude-code auth login"
    fi
else
    echo "📦 Instalando Claude Code..."
    npm install -g @anthropic-ai/claude-code
    
    echo ""
    echo "🔐 Por favor, autentique o Claude Code:"
    echo "   claude-code auth login"
fi

# Verificar/Instalar Ollama
echo ""
echo "🦙 Verificando Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama instalado"
    
    # Verificar se está rodando
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "✅ Ollama está rodando"
        
        # Listar modelos
        MODELS=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
        echo "📚 Modelos disponíveis: $MODELS"
        
        # Recomendar modelo se não houver nenhum
        if [ "$MODELS" -eq 0 ]; then
            echo ""
            echo "💡 Recomendação: Instale um modelo otimizado"
            echo "   Para melhor performance:"
            echo "   ollama pull llama3.2"
            echo "   ollama pull phi3"
        fi
    else
        echo "🚀 Iniciando Ollama..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
        
        if curl -s http://localhost:11434/api/tags &> /dev/null; then
            echo "✅ Ollama iniciado com sucesso"
        else
            echo "⚠️  Ollama não pôde ser iniciado automaticamente"
            echo "   Execute manualmente: ollama serve"
        fi
    fi
else
    echo "❌ Ollama não instalado"
    echo ""
    echo "📦 Para instalar Ollama:"
    
    if [ "$OS" = "Darwin" ]; then
        echo "   brew install ollama"
        echo "   ou baixe em: https://ollama.ai/download"
    elif [ "$OS" = "Linux" ]; then
        echo "   curl -fsSL https://ollama.ai/install.sh | sh"
    fi
fi

# Criar diretórios necessários
echo ""
echo "📁 Criando estrutura de diretórios..."
mkdir -p "$HOME/Library/Application Support/Digimundo/hybrid_memory"
mkdir -p "$HOME/Library/Application Support/Digimundo/cache"
mkdir -p "$HOME/Library/Application Support/Digimundo/models"
echo "✅ Diretórios criados"

# Configurar otimizações de ambiente
echo ""
echo "⚡ Aplicando otimizações..."

# Criar arquivo de configuração otimizada
CONFIG_FILE="$HOME/Library/Application Support/Digimundo/optimization.json"
cat > "$CONFIG_FILE" << 'EOF'
{
  "performance": {
    "cacheEnabled": true,
    "batchProcessing": true,
    "lazyLoading": true,
    "workerThreads": true,
    "compressionEnabled": true
  },
  "ollama": {
    "numParallel": 4,
    "maxQueue": 20,
    "batchSize": 4,
    "optimizedParams": {
      "temperature": 0.7,
      "top_k": 40,
      "top_p": 0.9,
      "num_predict": 256,
      "num_batch": 512
    }
  },
  "cache": {
    "maxSize": 100,
    "ttl": 300000,
    "compression": true
  },
  "monitoring": {
    "enabled": true,
    "metricsRetention": 1000,
    "healthCheckInterval": 60000
  }
}
EOF

echo "✅ Configurações otimizadas salvas"

# Verificar modelos GGUF
echo ""
echo "🔍 Verificando modelos GGUF locais..."
CONFIG_JSON="$HOME/Library/Application Support/Digimundo/config.json"
if [ -f "$CONFIG_JSON" ]; then
    MODEL_PATH=$(cat "$CONFIG_JSON" | grep -o '"modelPath":"[^"]*' | cut -d'"' -f4)
    if [ -n "$MODEL_PATH" ] && [ -f "$MODEL_PATH" ]; then
        MODEL_SIZE=$(du -h "$MODEL_PATH" | cut -f1)
        echo "✅ Modelo GGUF configurado: $(basename "$MODEL_PATH") ($MODEL_SIZE)"
    else
        echo "⚠️  Nenhum modelo GGUF configurado"
    fi
else
    echo "⚠️  Nenhum modelo GGUF configurado"
    echo "💡 Para melhor performance offline, configure um modelo GGUF"
fi

# Testar servidor
echo ""
echo "🧪 Testando servidor..."
npm run dev > /tmp/digimundo_test.log 2>&1 &
SERVER_PID=$!
sleep 5

if curl -s http://127.0.0.1:7937/health | grep -q "ok"; then
    echo "✅ Servidor funcionando corretamente"
    
    # Testar endpoint híbrido
    if curl -s http://127.0.0.1:7937/hybrid/status | grep -q "consciousness"; then
        echo "✅ Sistema híbrido operacional"
    else
        echo "⚠️  Sistema híbrido não respondendo"
    fi
else
    echo "❌ Servidor não está respondendo"
    cat /tmp/digimundo_test.log
fi

# Parar servidor de teste
kill $SERVER_PID 2>/dev/null || true

# Criar script de inicialização
echo ""
echo "📝 Criando script de inicialização..."
cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Digimundo Otimizado..."

# Verificar Ollama
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "🦙 Iniciando Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Configurar variáveis de ambiente para otimização
export NODE_OPTIONS="--max-old-space-size=2048"
export OLLAMA_NUM_PARALLEL=4
export OLLAMA_MAX_QUEUE=20

# Iniciar servidor
echo "🌌 Iniciando servidor..."
npm run dev
EOF

chmod +x start.sh
echo "✅ Script start.sh criado"

# Relatório final
echo ""
echo "============================================"
echo "✅ SETUP COMPLETO!"
echo "============================================"
echo ""
echo "📊 Resumo da Configuração:"
echo "  • Node.js: $NODE_VERSION"
echo "  • npm: v$NPM_VERSION"

if command -v claude-code &> /dev/null; then
    echo "  • Claude Code: ✅ Instalado"
else
    echo "  • Claude Code: ❌ Não instalado"
fi

if command -v ollama &> /dev/null; then
    echo "  • Ollama: ✅ Instalado"
    if [ "$MODELS" -gt 0 ]; then
        echo "  • Modelos Ollama: $MODELS disponíveis"
    fi
else
    echo "  • Ollama: ❌ Não instalado"
fi

echo ""
echo "🚀 Para iniciar o Digimundo:"
echo "   ./start.sh"
echo ""
echo "🌐 Acesse em:"
echo "   http://localhost:7937"
echo ""
echo "💡 Interface Híbrida em:"
echo "   http://localhost:7937/hybrid_interface.html"
echo ""
echo "✨ Enjoy your optimized Digimundo!"