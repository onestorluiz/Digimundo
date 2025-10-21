#!/bin/bash
#════════════════════════════════════════════════════════════════
# SECURE BASH WRAPPER - Interceptador de Comandos
#════════════════════════════════════════════════════════════════

PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
SESSION_FILE="/Users/clubproducoes/Digimundo/claude_code/.bash_session"
LOG_FILE="/Users/clubproducoes/Digimundo/claude_code/protection/bash_audit.log"
PASSWORD_HASH="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

#════════════════════════════════════════════════════════════════
# FUNÇÕES DE SEGURANÇA
#════════════════════════════════════════════════════════════════

check_session() {
    if [ -f "$SESSION_FILE" ]; then
        EXPIRY=$(cat "$SESSION_FILE")
        NOW=$(date +%s)

        if [ "$NOW" -lt "$EXPIRY" ]; then
            REMAINING=$((EXPIRY - NOW))
            if [ "$REMAINING" -le 5 ]; then
                echo -e "${YELLOW}⚡ Sessão expira em $REMAINING segundos!${NC}"
            fi
            return 0
        else
            rm -f "$SESSION_FILE"
            echo -e "${RED}⏰ SESSÃO EXPIRADA!${NC}"
        fi
    fi
    return 1
}

authenticate() {
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}🔐 AUTENTICAÇÃO BASH WRAPPER REQUERIDA${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"

    read -s -p "🔑 Digite a senha: " PASSWORD
    echo

    # Verifica hash da senha
    HASH=$(echo -n "$PASSWORD" | sha256sum | cut -d' ' -f1)

    if [ "$HASH" != "$PASSWORD_HASH" ]; then
        echo -e "${RED}❌ Senha incorreta${NC}"

        # Log de tentativa falha
        echo "$(date): Failed auth attempt" >> "$LOG_FILE"

        # Delay progressivo
        sleep 2
        return 1
    fi

    # Cria sessão de 15 segundos
    EXPIRY=$(($(date +%s) + 15))
    echo "$EXPIRY" > "$SESSION_FILE"

    echo -e "${GREEN}✅ Autenticado! Sessão de 15 segundos.${NC}"

    # Log de sucesso
    echo "$(date): Successful authentication" >> "$LOG_FILE"

    return 0
}

is_protected_path() {
    local PATH_TO_CHECK="$1"

    # Resolve caminho absoluto
    ABSOLUTE_PATH=$(realpath "$PATH_TO_CHECK" 2>/dev/null || echo "$PATH_TO_CHECK")

    # Verifica se está no diretório protegido
    if [[ "$ABSOLUTE_PATH" == "$PROTECTED_DIR"* ]]; then
        return 0
    fi

    return 1
}

log_operation() {
    local OPERATION="$1"
    local FILE="$2"
    local STATUS="$3"

    echo "$(date): $OPERATION on $FILE - $STATUS" >> "$LOG_FILE"
}

show_honeypot_warning() {
    echo -e "${RED}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                    🍯 HONEYPOT DETECTADO! 🍯              ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║  AVISO: Você está tentando acessar um arquivo isca!       ║"
    echo "║  Esta ação foi registrada e reportada.                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

#════════════════════════════════════════════════════════════════
# INTERCEPTADORES DE COMANDOS
#════════════════════════════════════════════════════════════════

# Função wrapper para comandos perigosos
secure_exec() {
    local CMD="$1"
    shift
    local ARGS="$@"

    # Verifica se algum argumento é path protegido
    for ARG in $ARGS; do
        if is_protected_path "$ARG"; then

            # Verifica honeypots
            if [[ "$ARG" == *".honeypot_"* ]]; then
                show_honeypot_warning
                log_operation "$CMD" "$ARG" "HONEYPOT_TRIGGERED"
                return 1
            fi

            # Verifica sessão
            if ! check_session; then
                if ! authenticate; then
                    log_operation "$CMD" "$ARG" "AUTH_FAILED"
                    return 1
                fi
            fi

            log_operation "$CMD" "$ARG" "AUTHORIZED"
            break
        fi
    done

    # Executa comando original
    command "$CMD" $ARGS
}

#════════════════════════════════════════════════════════════════
# ALIASES SEGUROS
#════════════════════════════════════════════════════════════════

# Sobrescreve comandos perigosos
alias rm='secure_exec rm'
alias mv='secure_exec mv'
alias cp='secure_exec cp'
alias cat='secure_exec cat'
alias nano='secure_exec nano'
alias vim='secure_exec vim'
alias vi='secure_exec vi'
alias sed='secure_exec sed'
alias awk='secure_exec awk'
alias grep='secure_exec grep'
alias find='secure_exec find'
alias chmod='secure_exec chmod'
alias chown='secure_exec chown'

# Comandos de escrita
alias echo='secure_exec echo'
alias printf='secure_exec printf'
alias tee='secure_exec tee'

#════════════════════════════════════════════════════════════════
# MONITOR DE COMANDOS
#════════════════════════════════════════════════════════════════

# Hook para capturar todos os comandos
trap 'log_operation "COMMAND" "$BASH_COMMAND" "EXECUTED"' DEBUG

#════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO
#════════════════════════════════════════════════════════════════

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🛡️  SECURE BASH WRAPPER ATIVO 🛡️               ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║  • Diretório protegido: scripturemon-champion             ║"
echo "║  • Sessões de 15 segundos                                 ║"
echo "║  • Todos os comandos são auditados                        ║"
echo "║  • Honeypots ativos                                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Para ativar este wrapper:
# source /Users/clubproducoes/Digimundo/claude_code/protection/secure_bash_wrapper.sh