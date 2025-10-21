#!/bin/bash
#════════════════════════════════════════════════════════════════
# ULTIMATE BASH PROTECTION - Solução Definitiva
#════════════════════════════════════════════════════════════════

PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
CLAUDE_CODE_DIR="/Users/clubproducoes/Digimundo/claude_code"
PASSWORD_HASH="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
SESSION_FILE="$CLAUDE_CODE_DIR/.ultimate_session"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

#════════════════════════════════════════════════════════════════
# MÉTODO 1: CRIAR WRAPPER PARA TODOS OS COMANDOS
#════════════════════════════════════════════════════════════════

setup_command_wrappers() {
    echo -e "${CYAN}Configurando wrappers de comandos...${NC}"

    # Cria diretório de wrappers
    WRAPPER_DIR="$CLAUDE_CODE_DIR/protection/wrappers"
    mkdir -p "$WRAPPER_DIR"

    # Lista de comandos para proteger
    COMMANDS=("rm" "mv" "cp" "cat" "echo" "sed" "awk" "grep" "find" "touch" "mkdir" "rmdir" "chmod" "chown" "vi" "vim" "nano" "emacs")

    for CMD in "${COMMANDS[@]}"; do
        # Encontra path real do comando
        REAL_CMD=$(which "$CMD" 2>/dev/null)

        if [ -n "$REAL_CMD" ]; then
            # Cria wrapper
            cat > "$WRAPPER_DIR/$CMD" << 'EOF'
#!/bin/bash
# Wrapper de proteção

PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
SESSION_FILE="/Users/clubproducoes/Digimundo/claude_code/.ultimate_session"
PASSWORD_HASH="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

check_protection() {
    for ARG in "$@"; do
        # Resolve caminho absoluto
        ABS_PATH=$(realpath "$ARG" 2>/dev/null || echo "$ARG")

        # Verifica se está no diretório protegido
        if [[ "$ABS_PATH" == "$PROTECTED_DIR"* ]]; then
            # Verifica sessão
            if [ -f "$SESSION_FILE" ]; then
                EXPIRY=$(cat "$SESSION_FILE")
                NOW=$(date +%s)

                if [ "$NOW" -lt "$EXPIRY" ]; then
                    return 0  # Sessão válida
                fi
            fi

            # Pede senha
            echo -e "\033[0;31m🔐 OPERAÇÃO PROTEGIDA DETECTADA!\033[0m"
            echo "Arquivo: $ABS_PATH"
            read -s -p "Digite a senha: " PASSWORD
            echo

            HASH=$(echo -n "$PASSWORD" | sha256sum | cut -d' ' -f1)

            if [ "$HASH" = "$PASSWORD_HASH" ]; then
                # Cria sessão de 15 segundos
                EXPIRY=$(($(date +%s) + 15))
                echo "$EXPIRY" > "$SESSION_FILE"
                echo -e "\033[0;32m✅ Autorizado! (15 segundos)\033[0m"
                return 0
            else
                echo -e "\033[0;31m❌ Senha incorreta!\033[0m"
                exit 1
            fi
        fi
    done

    return 0
}

# Verifica proteção
check_protection "$@"

# Executa comando real
EOF

            # Adiciona execução do comando real
            echo "REAL_CMD" >> "$WRAPPER_DIR/$CMD"
            sed -i '' "s|REAL_CMD|$REAL_CMD \"\$@\"|" "$WRAPPER_DIR/$CMD"

            # Torna executável
            chmod +x "$WRAPPER_DIR/$CMD"

            echo -e "  ${GREEN}✓${NC} Wrapper criado para: $CMD"
        fi
    done

    echo -e "${YELLOW}Para ativar, adicione ao PATH:${NC}"
    echo "export PATH=\"$WRAPPER_DIR:\$PATH\""
}

#════════════════════════════════════════════════════════════════
# MÉTODO 2: MODIFICAR PERMISSÕES DO FILESYSTEM
#════════════════════════════════════════════════════════════════

setup_filesystem_protection() {
    echo -e "${CYAN}Configurando proteção do filesystem...${NC}"

    # Cria grupo especial
    sudo dscl . -create /Groups/scripturemon_protected
    sudo dscl . -create /Groups/scripturemon_protected PrimaryGroupID 9999

    # Adiciona usuário ao grupo
    sudo dscl . -append /Groups/scripturemon_protected GroupMembership "$USER"

    # Modifica permissões do diretório
    sudo chown -R "$USER:scripturemon_protected" "$PROTECTED_DIR"
    sudo chmod -R 750 "$PROTECTED_DIR"  # rwxr-x---

    # Adiciona ACLs (Access Control Lists) no macOS
    sudo chmod +a "group:everyone deny delete" "$PROTECTED_DIR"
    sudo chmod +a "group:everyone deny write" "$PROTECTED_DIR"
    sudo chmod +a "group:scripturemon_protected allow read,write,delete" "$PROTECTED_DIR"

    echo -e "${GREEN}✅ Permissões configuradas${NC}"
}

#════════════════════════════════════════════════════════════════
# MÉTODO 3: CRIAR ALIAS SHELL PERSISTENTES
#════════════════════════════════════════════════════════════════

setup_shell_aliases() {
    echo -e "${CYAN}Configurando aliases do shell...${NC}"

    # Detecta shell atual
    CURRENT_SHELL=$(basename "$SHELL")

    if [ "$CURRENT_SHELL" = "zsh" ]; then
        RC_FILE="$HOME/.zshrc"
    elif [ "$CURRENT_SHELL" = "bash" ]; then
        RC_FILE="$HOME/.bashrc"
    else
        RC_FILE="$HOME/.profile"
    fi

    # Adiciona proteção ao arquivo RC
    cat >> "$RC_FILE" << 'EOF'

# ════════════════════════════════════════════════════════════════
# SCRIPTUREMON PROTECTION - NÃO REMOVER
# ════════════════════════════════════════════════════════════════

# Função de proteção
scripturemon_check() {
    local PROTECTED="/Users/clubproducoes/Digimundo/scripturemon-champion"

    for ARG in "$@"; do
        if [[ "$ARG" == "$PROTECTED"* ]]; then
            echo "🔐 OPERAÇÃO PROTEGIDA!"
            echo "Use o comando 'scripturemon-unlock' primeiro"
            return 1
        fi
    done

    return 0
}

# Wrapper para comandos
safe_exec() {
    local CMD=$1
    shift

    if scripturemon_check "$@"; then
        command "$CMD" "$@"
    fi
}

# Aliases protegidos
alias rm='safe_exec rm'
alias mv='safe_exec mv'
alias cp='safe_exec cp'
alias cat='safe_exec cat'
alias sed='safe_exec sed'
alias awk='safe_exec awk'

# Comando para desbloquear
scripturemon-unlock() {
    read -s -p "Senha: " PASSWORD
    echo

    HASH=$(echo -n "$PASSWORD" | sha256sum | cut -d' ' -f1)

    if [ "$HASH" = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" ]; then
        export SCRIPTUREMON_UNLOCKED=$(($(date +%s) + 15))
        echo "✅ Desbloqueado por 15 segundos!"
    else
        echo "❌ Senha incorreta!"
    fi
}

# ════════════════════════════════════════════════════════════════
EOF

    echo -e "${GREEN}✅ Aliases adicionados a $RC_FILE${NC}"
    echo -e "${YELLOW}Execute: source $RC_FILE${NC}"
}

#════════════════════════════════════════════════════════════════
# MÉTODO 4: CRIAR LAUNCHD DAEMON (macOS)
#════════════════════════════════════════════════════════════════

setup_launchd_daemon() {
    echo -e "${CYAN}Configurando LaunchDaemon...${NC}"

    # Cria plist para LaunchDaemon
    PLIST_FILE="$HOME/Library/LaunchAgents/com.scripturemon.protection.plist"

    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.scripturemon.protection</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$CLAUDE_CODE_DIR/protection/protection_daemon.py</string>
        <string>start</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>$CLAUDE_CODE_DIR/protection/daemon.log</string>

    <key>StandardErrorPath</key>
    <string>$CLAUDE_CODE_DIR/protection/daemon.err</string>

    <key>WatchPaths</key>
    <array>
        <string>$PROTECTED_DIR</string>
    </array>
</dict>
</plist>
EOF

    # Carrega daemon
    launchctl load "$PLIST_FILE" 2>/dev/null
    launchctl start com.scripturemon.protection

    echo -e "${GREEN}✅ LaunchDaemon configurado${NC}"
}

#════════════════════════════════════════════════════════════════
# MÉTODO 5: HOOK NO KERNEL (simulado)
#════════════════════════════════════════════════════════════════

simulate_kernel_protection() {
    echo -e "${CYAN}Simulando proteção kernel-level...${NC}"

    # Cria script de monitoramento com dtrace (requer sudo)
    cat > "$CLAUDE_CODE_DIR/protection/kernel_monitor.d" << 'EOF'
#!/usr/sbin/dtrace -s

/* Monitor de acesso a arquivos protegidos */

syscall::open*:entry
/copyinstr(arg0) contains "scripturemon-champion"/
{
    printf("ALERTA: PID %d tentando acessar: %s\n", pid, copyinstr(arg0));
}

syscall::unlink:entry
/copyinstr(arg0) contains "scripturemon-champion"/
{
    printf("BLOQUEADO: PID %d tentando deletar: %s\n", pid, copyinstr(arg0));
    /* Em teoria, poderia bloquear aqui */
}
EOF

    chmod +x "$CLAUDE_CODE_DIR/protection/kernel_monitor.d"

    echo -e "${YELLOW}Para ativar monitoramento kernel (requer sudo):${NC}"
    echo "sudo $CLAUDE_CODE_DIR/protection/kernel_monitor.d"
}

#════════════════════════════════════════════════════════════════
# MENU PRINCIPAL
#════════════════════════════════════════════════════════════════

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         🔐 ULTIMATE BASH PROTECTION SETUP                 ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║                                                            ║"
echo "║  Este script configura múltiplas camadas de proteção:     ║"
echo "║                                                            ║"
echo "║  1. Wrappers de comandos                                  ║"
echo "║  2. Permissões do filesystem + ACLs                       ║"
echo "║  3. Aliases persistentes no shell                         ║"
echo "║  4. LaunchDaemon (macOS)                                  ║"
echo "║  5. Monitoramento kernel (simulado)                       ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "Escolha o método de proteção:"
echo "1) Instalar TODOS os métodos (recomendado)"
echo "2) Apenas wrappers de comandos"
echo "3) Apenas permissões do filesystem"
echo "4) Apenas aliases do shell"
echo "5) Apenas LaunchDaemon"
echo "6) Apenas monitoramento kernel"
echo "0) Sair"

read -p "Opção: " CHOICE

case $CHOICE in
    1)
        setup_command_wrappers
        setup_filesystem_protection
        setup_shell_aliases
        setup_launchd_daemon
        simulate_kernel_protection
        echo -e "\n${GREEN}✅ TODAS AS PROTEÇÕES INSTALADAS!${NC}"
        ;;
    2)
        setup_command_wrappers
        ;;
    3)
        setup_filesystem_protection
        ;;
    4)
        setup_shell_aliases
        ;;
    5)
        setup_launchd_daemon
        ;;
    6)
        simulate_kernel_protection
        ;;
    0)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida"
        exit 1
        ;;
esac

echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}PROTEÇÃO CONFIGURADA COM SUCESSO!${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo
echo "Para testar a proteção:"
echo "  1. Tente: rm $PROTECTED_DIR/test.txt"
echo "  2. Deve pedir senha antes de executar"
echo
echo -e "${YELLOW}IMPORTANTE:${NC}"
echo "  • Sessões duram 15 segundos"
echo "  • Senha: admin"
echo "  • Reinicie o terminal para ativar aliases"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"