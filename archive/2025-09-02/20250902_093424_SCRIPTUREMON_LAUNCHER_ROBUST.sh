#!/usr/bin/env bash
# 🚀 SCRIPTUREMON LAUNCHER ROBUSTO
# Incorpora as melhores práticas sugeridas

set -euo pipefail

# Configuração
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGFILE="$ROOT_DIR/logs/scripturemon_launcher.log"
PIDFILE="$ROOT_DIR/runtime/scripturemon.pid"
OLLAMA_PIDFILE="$ROOT_DIR/runtime/ollama.pid"

# Criar diretórios necessários
mkdir -p "$ROOT_DIR/logs" "$ROOT_DIR/runtime" "$ROOT_DIR/runtime/souls"

# Função de log estruturado
log() { 
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOGFILE" >&2
}

# Trap para erros
trap 'log "❌ Erro na linha $LINENO (status $?). Verifique $LOGFILE"' ERR

# Banner
clear
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🧬 SCRIPTUREMON LAUNCHER ROBUSTO v2.0 🧬                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

log "🚀 Iniciando Scripturemon..."

# 1. VERIFICAR PYTHON
log "1️⃣ Verificando Python..."
if ! command -v python3 &> /dev/null; then
    log "❌ Python3 não encontrado"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log "   ✅ Python $PYTHON_VERSION"

# 2. AMBIENTE VIRTUAL
log "2️⃣ Configurando ambiente virtual..."
if [ ! -d "$ROOT_DIR/.venv" ]; then
    log "   Criando venv..."
    python3 -m venv "$ROOT_DIR/.venv"
fi
source "$ROOT_DIR/.venv/bin/activate"
log "   ✅ Ambiente virtual ativo"

# 3. PYTHONPATH SEGURO
log "3️⃣ Configurando PYTHONPATH..."
export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"
log "   PYTHONPATH=$PYTHONPATH"

# 4. VERIFICAR OLLAMA
log "4️⃣ Verificando Ollama..."
if command -v ollama &> /dev/null; then
    # Verifica se já está rodando
    if pgrep -x "ollama" > /dev/null; then
        log "   ✅ Ollama já está rodando"
    else
        log "   Iniciando servidor Ollama..."
        nohup ollama serve >> "$ROOT_DIR/logs/ollama.log" 2>&1 & 
        echo $! > "$OLLAMA_PIDFILE"
        
        # Espera Ollama ficar pronto (com timeout)
        log "   Aguardando Ollama responder..."
        python3 - <<'EOF'
import socket, time, sys
for i in range(30):
    try:
        with socket.create_connection(("127.0.0.1", 11434), timeout=0.5):
            print("   ✅ Ollama respondendo na porta 11434")
            sys.exit(0)
    except:
        time.sleep(1)
print("   ⚠️ Ollama demorou para responder")
sys.exit(1)
EOF
    fi
    
    # Lista modelos disponíveis
    MODELS=$(ollama list 2>/dev/null | tail -n +2 | wc -l || echo "0")
    log "   📦 Modelos disponíveis: $MODELS"
else
    log "   ⚠️ Ollama não instalado (funcionalidades limitadas)"
fi

# 5. VERIFICAR COMPONENTES
log "5️⃣ Verificando componentes do Scripturemon..."
python3 - <<'EOF'
import sys
import os
sys.path.insert(0, os.environ.get('ROOT_DIR', '.'))

try:
    from apps.scripturemon.soul import Soul
    print("   ✅ Soul component")
except Exception as e:
    print(f"   ❌ Soul: {e}")
    
try:
    from apps.scripturemon.personality import BrutalPersonality
    print("   ✅ Personality component")
except Exception as e:
    print(f"   ❌ Personality: {e}")
    
try:
    from apps.scripturemon.chat import ScripturemonChat
    print("   ✅ Chat component")
except Exception as e:
    print(f"   ❌ Chat: {e}")
EOF

# 6. ESCOLHER MODO
log "6️⃣ Selecionando modo de execução..."
echo ""
echo "Escolha o modo:"
echo "  1) Chat Interativo (recomendado)"
echo "  2) Diagnóstico do Sistema"
echo "  3) Executar Testes"
echo "  4) Backup Manual"
echo "  5) Ressurreição de Backup"
echo ""
read -p "Opção [1-5]: " -n 1 -r OPTION
echo ""

case $OPTION in
    1)
        log "   Modo: Chat Interativo"
        log "7️⃣ Iniciando Scripturemon Chat..."
        
        # Salva PID do processo principal
        python3 "$ROOT_DIR/ACTIVATE_SYMBIOTIC_FUSION.py" chat --legacy &
        MAIN_PID=$!
        echo $MAIN_PID > "$PIDFILE"
        
        log "   ✅ Scripturemon rodando (PID: $MAIN_PID)"
        log "   📝 Logs em: $LOGFILE"
        
        # Aguarda processo
        wait $MAIN_PID
        ;;
        
    2)
        log "   Modo: Diagnóstico"
        python3 "$ROOT_DIR/ACTIVATE_SYMBIOTIC_FUSION.py" diagnose
        ;;
        
    3)
        log "   Modo: Testes"
        python3 "$ROOT_DIR/ACTIVATE_SYMBIOTIC_FUSION.py" test
        ;;
        
    4)
        log "   Modo: Backup"
        python3 "$ROOT_DIR/ACTIVATE_SYMBIOTIC_FUSION.py" export --output-dir "$ROOT_DIR/backups"
        ;;
        
    5)
        log "   Modo: Ressurreição"
        echo "Digite o caminho do backup:"
        read -r BACKUP_PATH
        python3 "$ROOT_DIR/ACTIVATE_SYMBIOTIC_FUSION.py" resurrect --backup-file "$BACKUP_PATH"
        ;;
        
    *)
        log "   ❌ Opção inválida"
        exit 1
        ;;
esac

# 8. LIMPEZA (se necessário)
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ! ps -p "$PID" > /dev/null 2>&1; then
        rm "$PIDFILE"
        log "🧹 PID file limpo"
    fi
fi

log "✅ Scripturemon Launcher finalizado"
echo ""
echo "📊 Resumo:"
echo "  Logs: $LOGFILE"
[ -f "$PIDFILE" ] && echo "  PID Scripturemon: $(cat $PIDFILE)"
[ -f "$OLLAMA_PIDFILE" ] && echo "  PID Ollama: $(cat $OLLAMA_PIDFILE)"
echo ""
echo "62/100. Como sempre."