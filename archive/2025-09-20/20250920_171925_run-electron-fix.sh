#!/bin/bash

# ============================================
# ELECTRON AUTO-FIX & MONITORING LAUNCHER
# ============================================
# Script para executar o sistema de auto-correção
# e monitoramento do Electron
# ============================================

# DEFINIR DIRETÓRIO DO PROJETO
PROJECT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"

echo "╔══════════════════════════════════════════╗"
echo "║   ELECTRON AUTO-FIX & MONITORING v3.0    ║"
echo "║          Future-Proof Edition             ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "📁 Diretório do Projeto: $PROJECT_DIR"
echo ""

# Navegar para o diretório do projeto
cd "$PROJECT_DIR" || {
    echo "❌ Erro: Não foi possível acessar o diretório $PROJECT_DIR"
    exit 1
}

# Verificar se estamos no diretório correto
if [ ! -f "package.json" ]; then
    echo "❌ Erro: package.json não encontrado em $PROJECT_DIR"
    echo "Diretório atual: $(pwd)"
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não está instalado!"
    echo "Por favor, instale Node.js 18+ primeiro."
    exit 1
fi

# Verificar versão do Node
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt "18" ]; then
    echo "⚠️  Node.js v$NODE_VERSION é muito antigo"
    echo "Por favor, atualize para Node.js 18+"
    exit 1
fi

# Verificar se o arquivo de auto-fix existe
if [ ! -f "$PROJECT_DIR/electron-autofix.js" ]; then
    echo "❌ Arquivo electron-autofix.js não encontrado!"
    echo "Procurando em: $PROJECT_DIR/electron-autofix.js"
    exit 1
fi

# Tornar o script executável
chmod +x "$PROJECT_DIR/electron-autofix.js"

# Menu de opções
echo "Escolha uma opção:"
echo ""
echo "1) 🔍 Executar apenas diagnóstico"
echo "2) 🔧 Diagnóstico + Correções automáticas"
echo "3) 📊 Diagnóstico + Correções + Monitor contínuo"
echo "4) 🚀 Iniciar Electron normal (sem monitor)"
echo "5) 📋 Ver relatório anterior"
echo "6) 🗑️  Limpar logs e cache"
echo "7) ❌ Sair"
echo ""
read -p "Opção: " option

case $option in
    1)
        echo ""
        echo "🔍 Executando diagnóstico..."
        echo "Diretório: $PROJECT_DIR"
        cd "$PROJECT_DIR" && node electron-autofix.js --diagnose-only
        ;;
    
    2)
        echo ""
        echo "🔧 Executando diagnóstico e correções..."
        echo "Diretório: $PROJECT_DIR"
        cd "$PROJECT_DIR" && node electron-autofix.js --fix-only
        ;;
    
    3)
        echo ""
        echo "📊 Iniciando sistema completo..."
        echo "Diretório: $PROJECT_DIR"
        echo "Pressione Ctrl+C para parar"
        echo ""
        cd "$PROJECT_DIR" && node electron-autofix.js
        ;;
    
    4)
        echo ""
        echo "🚀 Iniciando Electron normal..."
        echo "Diretório: $PROJECT_DIR"
        cd "$PROJECT_DIR" && npm run dev
        ;;
    
    5)
        echo ""
        if [ -f "$PROJECT_DIR/electron-logs/report.json" ]; then
            echo "📋 Último relatório:"
            echo ""
            cat "$PROJECT_DIR/electron-logs/report.json" | python3 -m json.tool
        else
            echo "❌ Nenhum relatório encontrado"
            echo "Procurando em: $PROJECT_DIR/electron-logs/report.json"
        fi
        ;;
    
    6)
        echo ""
        echo "🗑️  Limpando logs e cache..."
        echo "Diretório: $PROJECT_DIR"
        rm -rf "$PROJECT_DIR/electron-logs/"
        rm -rf "$PROJECT_DIR/node_modules/.cache/"
        rm -rf ~/.electron/
        cd "$PROJECT_DIR" && npm cache clean --force
        echo "✅ Limpeza concluída!"
        ;;
    
    7)
        echo ""
        echo "👋 Até logo!"
        exit 0
        ;;
    
    *)
        echo ""
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "✅ Operação concluída!"
echo "📁 Executado em: $PROJECT_DIR"