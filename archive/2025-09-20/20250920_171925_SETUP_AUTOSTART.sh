#!/bin/bash

# 🚀 CONFIGURAÇÃO AUTOMÁTICA DO DIGIMUNDO - VERSÃO SIMPLIFICADA
# Este script configura o Digimundo para iniciar automaticamente

echo "╔══════════════════════════════════════════════════════════╗"
echo "║        🚀 AUTOSTART DO DIGIMUNDO - CONFIGURAÇÃO          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Configurar PATH para encontrar Node e npm
export PATH="/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

DIGIMUNDO_DIR="$(cd "$(dirname "$0")" && pwd)"
USER_HOME="$HOME"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}📍 PASSO 1: Instalando dependências faltantes...${NC}"
cd "$DIGIMUNDO_DIR"

# Usar o npm com PATH completo
/opt/homebrew/opt/node@20/bin/npm install node-fetch 2>/dev/null

echo -e "${GREEN}   ✅ Dependências verificadas${NC}"

echo ""
echo -e "${BLUE}📍 PASSO 2: Criando script de inicialização...${NC}"

# Criar script que inicia o Digimundo
cat > "$DIGIMUNDO_DIR/autostart.sh" << 'EOF'
#!/bin/bash

# Configurar PATH
export PATH="/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

# Diretório do projeto
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Criar diretório de logs
mkdir -p "$SCRIPT_DIR/eternal_logs"
LOG_FILE="$SCRIPT_DIR/eternal_logs/digimundo_$(date +%Y%m%d).log"

# Função para iniciar o servidor
start_server() {
    echo "[$(date)] Iniciando Digimundo..." >> "$LOG_FILE"
    
    # Iniciar servidor principal
    cd "$SCRIPT_DIR"
    npm run dev >> "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
    echo $SERVER_PID > "$SCRIPT_DIR/.digimundo.pid"
    echo "[$(date)] Servidor iniciado com PID: $SERVER_PID" >> "$LOG_FILE"
    
    # Aguardar inicialização
    sleep 10
    
    # Verificar se está rodando
    if curl -s http://localhost:7937/health > /dev/null 2>&1; then
        echo "[$(date)] ✅ Digimundo está ONLINE!" >> "$LOG_FILE"
        return 0
    else
        echo "[$(date)] ⚠️ Servidor não respondeu" >> "$LOG_FILE"
        return 1
    fi
}

# Verificar se já está rodando
if [ -f "$SCRIPT_DIR/.digimundo.pid" ]; then
    OLD_PID=$(cat "$SCRIPT_DIR/.digimundo.pid")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "[$(date)] Digimundo já está rodando (PID: $OLD_PID)" >> "$LOG_FILE"
        exit 0
    fi
fi

# Iniciar o servidor
start_server

# Monitor em background
(
    while true; do
        sleep 60
        if ! curl -s http://localhost:7937/health > /dev/null 2>&1; then
            echo "[$(date)] ⚠️ Servidor não responde, reiniciando..." >> "$LOG_FILE"
            if [ -f "$SCRIPT_DIR/.digimundo.pid" ]; then
                kill $(cat "$SCRIPT_DIR/.digimundo.pid") 2>/dev/null
            fi
            start_server
        fi
    done
) &

echo $! > "$SCRIPT_DIR/.monitor.pid"
echo "[$(date)] Monitor iniciado" >> "$LOG_FILE"
EOF

chmod +x "$DIGIMUNDO_DIR/autostart.sh"
echo -e "${GREEN}   ✅ Script criado${NC}"

echo ""
echo -e "${BLUE}📍 PASSO 3: Configurando inicialização automática...${NC}"

# Criar LaunchAgent
LAUNCH_AGENT="$USER_HOME/Library/LaunchAgents/com.digimundo.plist"
mkdir -p "$USER_HOME/Library/LaunchAgents"

cat > "$LAUNCH_AGENT" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.digimundo</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$DIGIMUNDO_DIR/autostart.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$DIGIMUNDO_DIR/eternal_logs/launch.log</string>
    
    <key>StandardErrorPath</key>
    <string>$DIGIMUNDO_DIR/eternal_logs/launch_err.log</string>
</dict>
</plist>
EOF

# Descarregar versão antiga se existir
launchctl unload "$LAUNCH_AGENT" 2>/dev/null

# Carregar nova versão
launchctl load "$LAUNCH_AGENT"

echo -e "${GREEN}   ✅ Autostart configurado${NC}"

echo ""
echo -e "${BLUE}📍 PASSO 4: Iniciando o Digimundo agora...${NC}"

# Executar o script agora
"$DIGIMUNDO_DIR/autostart.sh"

sleep 5

# Verificar status
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ Servidor online!${NC}"
    RESPONSE=$(curl -s http://localhost:7937/health)
    echo "   Status: $RESPONSE"
else
    echo -e "${YELLOW}   ⚠️ Verificando logs...${NC}"
    tail -3 "$DIGIMUNDO_DIR/eternal_logs/digimundo_$(date +%Y%m%d).log"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║           ✅ CONFIGURAÇÃO COMPLETA!                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 O Digimundo agora:"
echo "   • Inicia automaticamente quando o Mac liga"
echo "   • Reinicia se travar"
echo "   • Salva logs em eternal_logs/"
echo ""
echo "📋 Comandos úteis:"
echo ""
echo "Ver status:"
echo "  curl http://localhost:7937/health"
echo ""
echo "Ver logs:"
echo "  tail -f ~/Digimundo/digimundo_starter/eternal_logs/*.log"
echo ""
echo "Parar autostart:"
echo "  launchctl unload ~/Library/LaunchAgents/com.digimundo.plist"
echo ""
echo "Reiniciar:"
echo "  launchctl unload ~/Library/LaunchAgents/com.digimundo.plist"
echo "  launchctl load ~/Library/LaunchAgents/com.digimundo.plist"
echo ""
echo "🌟 Interface web:"
echo "  http://localhost:7937"
echo ""
