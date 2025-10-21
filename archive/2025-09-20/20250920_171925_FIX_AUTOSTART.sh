#!/bin/bash

# 🔧 FIX AUTOSTART - Corrige inicialização automática do Digimundo

echo "🔧 CONFIGURANDO INICIALIZAÇÃO AUTOMÁTICA DO DIGIMUNDO"
echo "====================================================="
echo ""

# Diretório do projeto
SCRIPT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"

# 1. Criar script de inicialização correto
cat > "$SCRIPT_DIR/autostart_fixed.sh" << 'AUTOSTART_SCRIPT'
#!/bin/bash

# Configurar PATH completo
export PATH="/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
export NODE_PATH="/opt/homebrew/opt/node@20/bin/node"

# Diretório do projeto
SCRIPT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"
cd "$SCRIPT_DIR"

# Criar diretório de logs
mkdir -p "$SCRIPT_DIR/eternal_logs"
LOG_FILE="$SCRIPT_DIR/eternal_logs/autostart_$(date +%Y%m%d).log"

# Log inicial
echo "[$(date)] ========== AUTOSTART DIGIMUNDO ==========" >> "$LOG_FILE"
echo "[$(date)] Iniciando sistema..." >> "$LOG_FILE"

# Aguardar sistema estar pronto (30 segundos após boot)
sleep 30

# Função para iniciar servidor
start_server() {
    echo "[$(date)] Tentando iniciar servidor..." >> "$LOG_FILE"
    
    # Verificar se já está rodando
    if curl -s http://localhost:7937/health > /dev/null 2>&1; then
        echo "[$(date)] Servidor já está rodando" >> "$LOG_FILE"
        return 0
    fi
    
    # Limpar PID antigo
    rm -f "$SCRIPT_DIR/.digimundo.pid"
    
    # Iniciar servidor
    cd "$SCRIPT_DIR"
    /opt/homebrew/opt/node@20/bin/node app/server/index.js >> "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
    echo $SERVER_PID > "$SCRIPT_DIR/.digimundo.pid"
    echo "[$(date)] Servidor iniciado com PID: $SERVER_PID" >> "$LOG_FILE"
    
    # Aguardar inicialização
    for i in {1..30}; do
        sleep 1
        if curl -s http://localhost:7937/health > /dev/null 2>&1; then
            echo "[$(date)] ✅ Servidor ONLINE!" >> "$LOG_FILE"
            return 0
        fi
    done
    
    echo "[$(date)] ⚠️ Servidor não respondeu após 30 segundos" >> "$LOG_FILE"
    return 1
}

# Tentar iniciar até 3 vezes
for attempt in {1..3}; do
    echo "[$(date)] Tentativa $attempt de 3..." >> "$LOG_FILE"
    if start_server; then
        echo "[$(date)] ✅ Digimundo iniciado com sucesso!" >> "$LOG_FILE"
        
        # Iniciar monitor
        (
            while true; do
                sleep 60
                if ! curl -s http://localhost:7937/health > /dev/null 2>&1; then
                    echo "[$(date)] Monitor: Servidor caiu, reiniciando..." >> "$LOG_FILE"
                    start_server
                fi
            done
        ) &
        echo $! > "$SCRIPT_DIR/.monitor.pid"
        echo "[$(date)] Monitor iniciado" >> "$LOG_FILE"
        
        exit 0
    fi
    
    # Aguardar antes de tentar novamente
    sleep 10
done

echo "[$(date)] ❌ Falha ao iniciar após 3 tentativas" >> "$LOG_FILE"
exit 1
AUTOSTART_SCRIPT

# Dar permissão de execução
chmod +x "$SCRIPT_DIR/autostart_fixed.sh"

# 2. Criar/Atualizar LaunchAgent
LAUNCH_AGENT="$HOME/Library/LaunchAgents/com.digimundo.autostart.plist"

cat > "$LAUNCH_AGENT" << PLIST_CONTENT
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.digimundo.autostart</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/clubproducoes/Digimundo/digimundo_starter/autostart_fixed.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    
    <key>StartInterval</key>
    <integer>300</integer>
    
    <key>StandardOutPath</key>
    <string>/Users/clubproducoes/Digimundo/digimundo_starter/eternal_logs/launch_out.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/clubproducoes/Digimundo/digimundo_starter/eternal_logs/launch_err.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
PLIST_CONTENT

echo "✅ Script de autostart criado: autostart_fixed.sh"
echo "✅ LaunchAgent criado: com.digimundo.autostart.plist"

# 3. Descarregar LaunchAgent antigo se existir
launchctl unload "$HOME/Library/LaunchAgents/com.digimundo.plist" 2>/dev/null
launchctl unload "$LAUNCH_AGENT" 2>/dev/null

# 4. Carregar novo LaunchAgent
launchctl load "$LAUNCH_AGENT"

echo ""
echo "🔄 Verificando status..."
sleep 2

if launchctl list | grep -q "com.digimundo.autostart"; then
    echo "✅ LaunchAgent carregado com sucesso!"
else
    echo "⚠️ Erro ao carregar LaunchAgent"
fi

# 5. Criar aplicativo .app para lançamento manual
echo ""
echo "📱 Criando aplicativo Digimundo.app..."

APP_DIR="$HOME/Desktop/Digimundo.app"
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Script principal do app
cat > "$APP_DIR/Contents/MacOS/Digimundo" << 'APP_SCRIPT'
#!/bin/bash

# Abrir Terminal e executar launcher
osascript -e '
tell application "Terminal"
    activate
    do script "cd /Users/clubproducoes/Digimundo/digimundo_starter && bash ULTIMATE_LAUNCHER.sh"
end tell
'
APP_SCRIPT

chmod +x "$APP_DIR/Contents/MacOS/Digimundo"

# Info.plist
cat > "$APP_DIR/Contents/Info.plist" << 'INFO_PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Digimundo</string>
    <key>CFBundleDisplayName</key>
    <string>Digimundo</string>
    <key>CFBundleIdentifier</key>
    <string>com.digimundo.launcher</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleExecutable</key>
    <string>Digimundo</string>
    <key>CFBundleIconFile</key>
    <string>digimundo</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>
INFO_PLIST

echo "✅ Aplicativo criado: $APP_DIR"

echo ""
echo "=========================================="
echo "✨ CONFIGURAÇÃO COMPLETA!"
echo "=========================================="
echo ""
echo "📊 O QUE FOI CONFIGURADO:"
echo ""
echo "1. ✅ Script de autostart corrigido"
echo "2. ✅ LaunchAgent configurado para iniciar no boot"
echo "3. ✅ Aplicativo Digimundo.app no Desktop"
echo ""
echo "🚀 COMO FUNCIONA AGORA:"
echo ""
echo "• AUTOMÁTICO: Digimundo inicia ao ligar o Mac"
echo "• MANUAL: Clique duplo em Digimundo.app no Desktop"
echo "• TERMINAL: bash ULTIMATE_LAUNCHER.sh"
echo ""
echo "📁 ARQUIVOS CRIADOS:"
echo ""
echo "• $SCRIPT_DIR/autostart_fixed.sh"
echo "• $LAUNCH_AGENT"
echo "• $APP_DIR"
echo ""
echo "🔍 VERIFICAR LOGS:"
echo ""
echo "• tail -f $SCRIPT_DIR/eternal_logs/autostart_*.log"
echo "• tail -f $SCRIPT_DIR/eternal_logs/launch_*.log"
echo ""
echo "=========================================="
echo "✅ Digimundo agora iniciará automaticamente!"
echo "=========================================="
