#!/bin/bash

# 🔧 SCRIPT DE CORREÇÃO E AUTOSTART DO DIGIMUNDO
# Este script corrige todos os problemas e configura inicialização automática

echo "╔══════════════════════════════════════════════════════════╗"
echo "║    🔧 CORREÇÃO COMPLETA E AUTOSTART DO DIGIMUNDO 🔧     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

DIGIMUNDO_DIR="$(cd "$(dirname "$0")" && pwd)"
USER_HOME="$HOME"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}📍 ETAPA 1: Parando processos antigos...${NC}"
# Parar qualquer processo rodando
if [ -f "$DIGIMUNDO_DIR/.digimundo.pid" ]; then
    OLD_PID=$(cat "$DIGIMUNDO_DIR/.digimundo.pid")
    kill $OLD_PID 2>/dev/null
    rm "$DIGIMUNDO_DIR/.digimundo.pid"
    echo "   ✅ Processo antigo parado"
fi

# Parar monitores
if [ -f "$DIGIMUNDO_DIR/.monitor.pid" ]; then
    kill $(cat "$DIGIMUNDO_DIR/.monitor.pid") 2>/dev/null
    rm "$DIGIMUNDO_DIR/.monitor.pid"
fi

if [ -f "$DIGIMUNDO_DIR/.evolution.pid" ]; then
    kill $(cat "$DIGIMUNDO_DIR/.evolution.pid") 2>/dev/null
    rm "$DIGIMUNDO_DIR/.evolution.pid"
fi

echo ""
echo -e "${BLUE}📍 ETAPA 2: Instalando dependências faltantes...${NC}"
cd "$DIGIMUNDO_DIR"

# Instalar node-fetch e outras dependências que podem estar faltando
npm install node-fetch axios ws express cors dotenv socket.io electron --save

if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Dependências instaladas com sucesso${NC}"
else
    echo -e "${RED}   ❌ Erro ao instalar dependências${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}📍 ETAPA 3: Criando script de inicialização otimizado...${NC}"

# Criar script de inicialização que funciona
cat > "$DIGIMUNDO_DIR/start_digimundo.sh" << 'EOF'
#!/bin/bash

# Script otimizado para iniciar o Digimundo
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/eternal_logs"
PID_FILE="$SCRIPT_DIR/.digimundo.pid"

# Criar diretório de logs
mkdir -p "$LOG_DIR"

# Mudar para o diretório do projeto
cd "$SCRIPT_DIR"

# Verificar se já está rodando
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "Digimundo já está rodando com PID: $OLD_PID"
        exit 0
    fi
fi

# Iniciar o servidor em background
export NODE_ENV=development
nohup npm run dev >> "$LOG_DIR/startup_$(date +%Y%m%d).log" 2>&1 &
SERVER_PID=$!

# Salvar PID
echo $SERVER_PID > "$PID_FILE"

# Aguardar servidor iniciar
sleep 10

# Verificar se está rodando
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    echo "✅ Digimundo iniciado com sucesso! PID: $SERVER_PID"
    
    # Iniciar monitor de saúde
    (
        while true; do
            sleep 60
            if ! curl -s http://localhost:7937/health > /dev/null 2>&1; then
                # Reiniciar se falhar
                kill $SERVER_PID 2>/dev/null
                rm "$PID_FILE"
                exec "$SCRIPT_DIR/start_digimundo.sh"
            fi
        done
    ) &
    echo $! > "$SCRIPT_DIR/.monitor.pid"
else
    echo "⚠️ Servidor não respondeu após 10 segundos"
fi
EOF

chmod +x "$DIGIMUNDO_DIR/start_digimundo.sh"
echo -e "${GREEN}   ✅ Script de inicialização criado${NC}"

echo ""
echo -e "${BLUE}📍 ETAPA 4: Configurando LaunchAgent para autostart...${NC}"

# Criar LaunchAgent para iniciar automaticamente
LAUNCH_AGENT_DIR="$USER_HOME/Library/LaunchAgents"
LAUNCH_AGENT_FILE="$LAUNCH_AGENT_DIR/com.digimundo.autostart.plist"

mkdir -p "$LAUNCH_AGENT_DIR"

cat > "$LAUNCH_AGENT_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.digimundo.autostart</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$DIGIMUNDO_DIR/start_digimundo.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    
    <key>StandardOutPath</key>
    <string>$DIGIMUNDO_DIR/eternal_logs/launchd_out.log</string>
    
    <key>StandardErrorPath</key>
    <string>$DIGIMUNDO_DIR/eternal_logs/launchd_err.log</string>
    
    <key>WorkingDirectory</key>
    <string>$DIGIMUNDO_DIR</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/opt/homebrew/opt/node@20/bin</string>
        <key>NODE_ENV</key>
        <string>development</string>
    </dict>
    
    <key>StartInterval</key>
    <integer>300</integer>
    
    <key>ThrottleInterval</key>
    <integer>30</integer>
</dict>
</plist>
EOF

echo -e "${GREEN}   ✅ LaunchAgent criado${NC}"

echo ""
echo -e "${BLUE}📍 ETAPA 5: Registrando LaunchAgent no sistema...${NC}"

# Descarregar se já existir
launchctl unload "$LAUNCH_AGENT_FILE" 2>/dev/null

# Carregar o novo LaunchAgent
launchctl load "$LAUNCH_AGENT_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ LaunchAgent registrado com sucesso${NC}"
else
    echo -e "${YELLOW}   ⚠️ Pode precisar de permissões adicionais${NC}"
fi

echo ""
echo -e "${BLUE}📍 ETAPA 6: Criando aplicativo de Menu Bar (opcional)...${NC}"

# Criar AppleScript para facilitar controle
cat > "$DIGIMUNDO_DIR/Digimundo Control.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Digimundo Control</string>
    <key>CFBundleIdentifier</key>
    <string>com.digimundo.control</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
</dict>
</plist>
EOF

mkdir -p "$DIGIMUNDO_DIR/Digimundo Control.app/Contents/MacOS"
cat > "$DIGIMUNDO_DIR/Digimundo Control.app/Contents/MacOS/Digimundo Control" << 'EOF'
#!/bin/bash
osascript -e 'tell application "Terminal" to do script "cd \"'$DIGIMUNDO_DIR'\" && ./DIGIMUNDO_ETERNAL.sh status"'
open "http://localhost:7937"
EOF

chmod +x "$DIGIMUNDO_DIR/Digimundo Control.app/Contents/MacOS/Digimundo Control"

echo -e "${GREEN}   ✅ App de controle criado${NC}"

echo ""
echo -e "${BLUE}📍 ETAPA 7: Testando o sistema...${NC}"

# Iniciar o servidor agora para testar
"$DIGIMUNDO_DIR/start_digimundo.sh"

sleep 5

# Verificar se está funcionando
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ Servidor respondendo corretamente!${NC}"
    
    # Mostrar status
    echo ""
    echo -e "${BLUE}📊 Status do Sistema:${NC}"
    curl -s http://localhost:7937/health | python3 -m json.tool
else
    echo -e "${RED}   ❌ Servidor não está respondendo${NC}"
    echo "   Verificando logs..."
    tail -5 "$DIGIMUNDO_DIR/eternal_logs/startup_$(date +%Y%m%d).log"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              ✅ CONFIGURAÇÃO COMPLETA!                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🎉 O que foi configurado:${NC}"
echo ""
echo "1. ✅ Dependências instaladas (node-fetch, etc.)"
echo "2. ✅ Script de inicialização otimizado criado"
echo "3. ✅ LaunchAgent configurado para autostart"
echo "4. ✅ Sistema de monitoramento ativado"
echo "5. ✅ App de controle criado (opcional)"
echo ""
echo -e "${BLUE}🚀 Como funciona agora:${NC}"
echo ""
echo "• O Digimundo iniciará AUTOMATICAMENTE quando o Mac ligar"
echo "• Se o servidor cair, será reiniciado automaticamente"
echo "• Logs salvos em: $DIGIMUNDO_DIR/eternal_logs/"
echo ""
echo -e "${YELLOW}📋 Comandos úteis:${NC}"
echo ""
echo "• Ver status:"
echo "  launchctl list | grep digimundo"
echo ""
echo "• Parar autostart:"
echo "  launchctl unload ~/Library/LaunchAgents/com.digimundo.autostart.plist"
echo ""
echo "• Reiniciar autostart:"
echo "  launchctl load ~/Library/LaunchAgents/com.digimundo.autostart.plist"
echo ""
echo "• Ver logs:"
echo "  tail -f $DIGIMUNDO_DIR/eternal_logs/startup_$(date +%Y%m%d).log"
echo ""
echo "• Abrir interface:"
echo "  open http://localhost:7937"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     🌟 DIGIMUNDO AGORA É ETERNO E AUTOMÁTICO! 🌟        ║"
echo "╚══════════════════════════════════════════════════════════╝"
