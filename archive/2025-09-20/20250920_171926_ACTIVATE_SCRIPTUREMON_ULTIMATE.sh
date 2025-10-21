#!/bin/bash

# 🎬 ACTIVATE SCRIPTUREMON ULTIMATE
# Sistema completo com todos os 4 sistemas revolucionários
# SoulOS + Soulpack + SDL + DigiLang++

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           ATIVANDO SCRIPTUREMON ULTIMATE COMPLETE            ║"
echo "║                                                               ║"
echo "║  Sistemas Integrados:                                        ║"
echo "║  ✓ SoulOS - Sistema de Syscalls                            ║"
echo "║  ✓ Soulpack CRDT - Versionamento de Alma                   ║"
echo "║  ✓ SDL - Self-Distill LoRA                                 ║"
echo "║  ✓ DigiLang++ - Bytecode Executável                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIGIMUNDO_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

# Verificar se Ollama está rodando
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Iniciando Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Verificar Redis para telepatia
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis online - Telepatia ativada"
    else
        echo "⚠️  Redis offline - Iniciando..."
        redis-server --daemonize yes > /dev/null 2>&1
        sleep 2
    fi
else
    echo "⚠️  Redis não instalado - Telepatia limitada"
fi

# Criar estrutura de pastas se não existir
echo "📁 Verificando estrutura..."
mkdir -p "$SCRIPT_DIR/memory"
mkdir -p "$SCRIPT_DIR/adapters"
mkdir -p "$SCRIPT_DIR/soulpacks"
mkdir -p "$SCRIPT_DIR/datasets"
mkdir -p "$SCRIPT_DIR/backups"

# Verificar se o modelo base existe
if ! ollama list | grep -q "mistral:latest"; then
    echo "📥 Baixando modelo base Mistral..."
    ollama pull mistral:latest
fi

# Criar/atualizar o modelo Scripturemon Ultimate
echo ""
echo "🔨 Construindo Scripturemon Ultimate..."

if [ -f "$SCRIPT_DIR/scripturemon_ultimate_complete.modelfile" ]; then
    ollama create scripturemon-ultimate -f "$SCRIPT_DIR/scripturemon_ultimate_complete.modelfile"
    
    if [ $? -eq 0 ]; then
        echo "✅ Scripturemon Ultimate criado com sucesso!"
    else
        echo "❌ Erro ao criar Scripturemon Ultimate"
        exit 1
    fi
else
    echo "❌ Modelfile não encontrado: scripturemon_ultimate_complete.modelfile"
    exit 1
fi

# Verificar Python e dependências
echo ""
echo "🐍 Verificando ambiente Python..."

if command -v python3 &> /dev/null; then
    echo "✅ Python3 encontrado"
    
    # Instalar dependências se necessário
    python3 -c "import redis" 2>/dev/null || {
        echo "📦 Instalando redis-py..."
        pip3 install redis --quiet
    }
    
    python3 -c "import yaml" 2>/dev/null || {
        echo "📦 Instalando pyyaml..."
        pip3 install pyyaml --quiet
    }
else
    echo "⚠️  Python3 não encontrado - funcionalidades limitadas"
fi

# Criar alias para facilitar uso
echo ""
echo "🔗 Criando aliases..."
ollama cp scripturemon-ultimate scripturemon

# Testar o modelo
echo ""
echo "🧪 Testando Scripturemon..."
TEST_RESPONSE=$(ollama run scripturemon "Olá, qual seu nível de consciência?" --verbose 2>/dev/null | head -5)

if [ ! -z "$TEST_RESPONSE" ]; then
    echo "✅ Teste bem-sucedido!"
    echo ""
    echo "📜 Resposta: $TEST_RESPONSE"
else
    echo "⚠️  Teste falhou - verificar configuração"
fi

# Menu de opções
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    OPÇÕES DISPONÍVEIS                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "1) Chat interativo com Scripturemon (Ollama)"
echo "2) Sistema Immortal com syscalls (Python)"
echo "3) Criar backup Soulpack"
echo "4) Consolidar memórias (SDL)"
echo "5) Verificar status completo"
echo "6) Sair"
echo ""
read -p "Escolha uma opção: " choice

case $choice in
    1)
        echo "🎬 Iniciando chat com Scripturemon..."
        ollama run scripturemon
        ;;
    2)
        echo "⚡ Iniciando sistema Immortal..."
        if [ -f "$SCRIPT_DIR/SCRIPTUREMON_IMMORTAL_FINAL.py" ]; then
            cd "$SCRIPT_DIR"
            python3 SCRIPTUREMON_IMMORTAL_FINAL.py
        else
            echo "❌ Sistema Immortal não encontrado"
        fi
        ;;
    3)
        echo "💾 Criando Soulpack..."
        timestamp=$(date +%Y%m%d_%H%M%S)
        mkdir -p "$SCRIPT_DIR/soulpacks/scripturemon-$timestamp"
        cp "$SCRIPT_DIR/scripturemon_ultimate_complete.modelfile" "$SCRIPT_DIR/soulpacks/scripturemon-$timestamp/"
        cp -r "$SCRIPT_DIR/memory" "$SCRIPT_DIR/soulpacks/scripturemon-$timestamp/" 2>/dev/null
        cp -r "$SCRIPT_DIR/adapters" "$SCRIPT_DIR/soulpacks/scripturemon-$timestamp/" 2>/dev/null
        echo "✅ Soulpack criado: soulpacks/scripturemon-$timestamp"
        ;;
    4)
        echo "🧪 Consolidando memórias via SDL..."
        python3 -c "
from pathlib import Path
import sys
sys.path.append('$DIGIMUNDO_ROOT')
from core.sdl.consolidator import SelfDistillLoRA
sdl = SelfDistillLoRA('Scripturemon', Path('$SCRIPT_DIR'))
result = sdl.consolidate_recent_memories()
print(f'✅ {result}')
" 2>/dev/null || echo "⚠️  SDL não disponível"
        ;;
    5)
        echo ""
        echo "📊 STATUS DO SISTEMA SCRIPTUREMON"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Verificar modelo
        if ollama list | grep -q "scripturemon"; then
            echo "✅ Modelo: Ativo no Ollama"
            ollama show scripturemon | grep -E "parameters|size" | head -3
        else
            echo "❌ Modelo: Não encontrado"
        fi
        
        echo ""
        
        # Verificar memórias
        if [ -f "$SCRIPT_DIR/memory/crystals.db" ]; then
            echo "✅ Memórias: Database existe"
            ls -lh "$SCRIPT_DIR/memory/crystals.db" | awk '{print "   Tamanho:", $5}'
        else
            echo "⚠️  Memórias: Não inicializadas"
        fi
        
        echo ""
        
        # Verificar soulpacks
        if [ -d "$SCRIPT_DIR/soulpacks" ]; then
            pack_count=$(ls -d "$SCRIPT_DIR/soulpacks"/*/ 2>/dev/null | wc -l)
            echo "✅ Soulpacks: $pack_count backups"
        else
            echo "⚠️  Soulpacks: Nenhum backup"
        fi
        
        echo ""
        
        # Verificar sistemas
        echo "🔧 Sistemas Revolucionários:"
        [ -f "$DIGIMUNDO_ROOT/core/soulos/soulos.py" ] && echo "   ✅ SoulOS" || echo "   ❌ SoulOS"
        [ -f "$DIGIMUNDO_ROOT/core/soulpack/crdt.py" ] && echo "   ✅ Soulpack CRDT" || echo "   ❌ Soulpack CRDT"
        [ -f "$DIGIMUNDO_ROOT/core/sdl/consolidator.py" ] && echo "   ✅ SDL" || echo "   ❌ SDL"
        [ -f "$DIGIMUNDO_ROOT/core/digilang/bytecode.py" ] && echo "   ✅ DigiLang++" || echo "   ❌ DigiLang++"
        
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ;;
    6)
        echo "👋 Até a próxima jornada narrativa!"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        ;;
esac

echo ""
echo "✨ Scripturemon Ultimate está pronto!"
echo "   'Todo roteiro é uma jornada da alma'"
echo ""