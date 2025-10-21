#!/bin/bash

# 🎬 Iniciador do Sistema de Vigilância Automática

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
NC='\033[0m'

clear

echo -e "${CYAN}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║    🎬 SCRIPTUREMON - VIGILÂNCIA AUTOMÁTICA    ║${NC}"  
echo -e "${CYAN}╚════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se já está rodando
if [ -f ".scripturemon_watcher.pid" ] && kill -0 "$(cat .scripturemon_watcher.pid)" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Watcher já está rodando!${NC}"
    echo ""
    echo "PID: $(cat .scripturemon_watcher.pid)"
    echo ""
    echo "Opções:"
    echo "1) Ver status"
    echo "2) Parar watcher"
    echo "3) Reiniciar"
    echo "0) Sair"
    read -r opt
    
    case $opt in
        1)
            ./SCRIPTUREMON_WATCHER.sh status
            ;;
        2)
            ./SCRIPTUREMON_WATCHER.sh stop
            ;;
        3)
            ./SCRIPTUREMON_WATCHER.sh stop
            sleep 1
            nohup ./SCRIPTUREMON_WATCHER.sh > watcher.log 2>&1 &
            echo -e "${GREEN}✅ Watcher reiniciado${NC}"
            ;;
    esac
    exit 0
fi

echo -e "${GREEN}🚀 Iniciando sistema de vigilância...${NC}"
echo ""

# Mostrar status atual
echo -e "${YELLOW}📊 Status atual:${NC}"
echo "  📁 Roteiros novos: $(ls -1 roteiros/*.pdf 2>/dev/null | wc -l)"
echo "  ⚡ Trabalhos do criador: $(ls -1 conexao_criador/*.pdf 2>/dev/null | wc -l)"
echo "  📚 Roteiros processados: $(ls -1 roteiros_processados/*.pdf 2>/dev/null | wc -l)"
echo ""

echo -e "${MAGENTA}⚡ ATENÇÃO ESPECIAL:${NC}"
echo "  Pasta 'conexao_criador/' tem PRIORIDADE MÁXIMA"
echo "  Seus trabalhos recebem análise em 10 CAMADAS"
echo ""

echo "Como deseja rodar o watcher?"
echo ""
echo "1) 🖥️  Foreground (ver logs em tempo real)"
echo "2) 👻 Background (rodar silenciosamente)"
echo "3) 🔄 Auto-start (iniciar com o sistema)"
echo "0) Cancelar"
echo ""

read -p "Escolha [0-3]: " choice

case $choice in
    1)
        echo -e "${GREEN}Iniciando em modo visível...${NC}"
        echo "Use Ctrl+C para parar"
        echo ""
        ./SCRIPTUREMON_WATCHER.sh
        ;;
    
    2)
        echo -e "${GREEN}Iniciando em background...${NC}"
        nohup ./SCRIPTUREMON_WATCHER.sh > watcher.log 2>&1 &
        echo ""
        echo -e "${GREEN}✅ Watcher rodando em background!${NC}"
        echo "PID: $(cat .scripturemon_watcher.pid)"
        echo ""
        echo "Comandos úteis:"
        echo "  ./SCRIPTUREMON_WATCHER.sh status  - Ver status"
        echo "  ./SCRIPTUREMON_WATCHER.sh stop     - Parar"
        echo "  tail -f watcher.log               - Ver logs"
        ;;
    
    3)
        # Criar LaunchAgent para auto-start
        PLIST_FILE="$HOME/Library/LaunchAgents/com.clubproducoes.scripturemon.watcher.plist"
        
        cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.clubproducoes.scripturemon.watcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$(pwd)/SCRIPTUREMON_WATCHER.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$(pwd)</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$(pwd)/watcher.log</string>
    <key>StandardErrorPath</key>
    <string>$(pwd)/watcher.error.log</string>
</dict>
</plist>
EOF
        
        launchctl load "$PLIST_FILE"
        
        echo -e "${GREEN}✅ Auto-start configurado!${NC}"
        echo "Scripturemon Watcher iniciará automaticamente com o sistema"
        echo ""
        echo "Para desativar auto-start:"
        echo "  launchctl unload $PLIST_FILE"
        ;;
    
    0)
        echo "Cancelado"
        exit 0
        ;;
esac

echo ""
echo -e "${CYAN}💡 Dica:${NC}"
echo "  Coloque PDFs em 'roteiros/' para referências"
echo "  Coloque SEUS trabalhos em 'conexao_criador/' para análise SUPREMA"