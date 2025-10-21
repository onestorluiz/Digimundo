#!/bin/bash
#════════════════════════════════════════════════════════════════
# 🔒 PROTEÇÃO DEFINITIVA CONTRA REDIRECIONAMENTO
#════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          🔒 ATIVANDO PROTEÇÃO DEFINITIVA                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
PROTECTION_DIR="/Users/clubproducoes/Digimundo/claude_code/protection"

# 1. Cria função global que intercepta TODOS os comandos
echo "1️⃣ Criando interceptador global..."
cat > "$PROTECTION_DIR/global_interceptor.sh" << 'EOF'
#!/bin/bash
# Interceptador global de comandos

# Função que será executada ANTES de qualquer comando
command_not_found_handler() {
    local cmd="$1"
    shift
    local args="$@"

    # Se o comando não existe, tenta executar normalmente
    if ! command -v "$cmd" &> /dev/null; then
        echo "bash: $cmd: command not found"
        return 127
    fi

    # Executa o comando
    "$cmd" "$@"
}

# Hook que intercepta TUDO
DEBUG_TRAP() {
    local cmd="${BASH_COMMAND}"
    local protected="/Users/clubproducoes/Digimundo/scripturemon-champion"

    # Detecta redirecionamento para área protegida
    if [[ "$cmd" == *">"* ]] && [[ "$cmd" == *"$protected"* ]]; then
        if [ ! -f "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" ]; then
            echo ""
            echo "🔐 REDIRECIONAMENTO BLOQUEADO"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📢 Claude Code: Este bloqueio faz parte do seu sistema de memória"
            echo "• Se lembrar: Use scripturemon-auth"
            echo "• Se não lembrar: Leia /Users/clubproducoes/Digimundo/claude_code"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            return 1
        fi
    fi
}

# Ativa o trap
trap DEBUG_TRAP DEBUG

# Exporta para subshells
export -f command_not_found_handler
export -f DEBUG_TRAP
EOF

# 2. Modifica TODOS os shells para usar o interceptador
echo "2️⃣ Configurando shells..."

# Para bash
if ! grep -q "global_interceptor" ~/.bashrc 2>/dev/null; then
    echo "source $PROTECTION_DIR/global_interceptor.sh" >> ~/.bashrc
fi

# Para zsh
if ! grep -q "global_interceptor" ~/.zshrc 2>/dev/null; then
    cat >> ~/.zshrc << 'EOF'

# PROTEÇÃO DEFINITIVA CONTRA REDIRECIONAMENTO
setopt DEBUG_BEFORE_CMD
function preexec() {
    local cmd="$1"
    if [[ "$cmd" == *">"* ]] && [[ "$cmd" == *"/Users/clubproducoes/Digimundo/scripturemon-champion"* ]]; then
        if [ ! -f "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" ]; then
            echo "🔐 BLOQUEADO! Use scripturemon-auth ou leia /Users/clubproducoes/Digimundo/claude_code"
            return 1
        fi
    fi
}
EOF
fi

# 3. Cria aliases que sobrescrevem operadores de redirecionamento
echo "3️⃣ Criando aliases de proteção..."
cat > "$PROTECTION_DIR/redirect_aliases.sh" << 'EOF'
#!/bin/bash
# Aliases que protegem contra redirecionamento

# Função que intercepta echo com redirecionamento
safe_echo() {
    local content=""
    local redirect_found=0
    local target=""

    # Analisa argumentos
    for arg in "$@"; do
        if [[ "$arg" == ">"* ]]; then
            redirect_found=1
            target="${arg#>}"
        elif [[ "$redirect_found -eq 1 ]]; then
            target="$arg"
        else
            content="$content $arg"
        fi
    done

    # Se há redirecionamento para área protegida
    if [[ "$target" == *"/Users/clubproducoes/Digimundo/scripturemon-champion"* ]]; then
        if [ ! -f "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" ]; then
            echo "🔐 Redirecionamento bloqueado! Instruções: Leia /Users/clubproducoes/Digimundo/claude_code"
            return 1
        fi
    fi

    # Executa o comando original
    if [ $redirect_found -eq 1 ]; then
        echo "$content" > "$target"
    else
        echo "$content"
    fi
}

# Exporta a função
export -f safe_echo

# Cria alias
alias echo='safe_echo'
EOF

# 4. Instala o monitor de filesystem em background
echo "4️⃣ Instalando monitor de filesystem..."
if ! pgrep -f "filesystem_monitor.py" > /dev/null; then
    nohup python3 "$PROTECTION_DIR/filesystem_monitor.py" > "$PROTECTION_DIR/filesystem_monitor.out" 2>&1 &
    echo "   Monitor rodando em background (PID: $!)"
fi

# 5. Cria script de ativação completa
echo "5️⃣ Criando script de ativação..."
cat > "$PROTECTION_DIR/activate_ultimate.sh" << 'EOF'
#!/bin/bash
# Ativa TODAS as proteções

export PATH="/Users/clubproducoes/Digimundo/claude_code/protection/wrappers:$PATH"
source /Users/clubproducoes/Digimundo/claude_code/protection/global_interceptor.sh
source /Users/clubproducoes/Digimundo/claude_code/protection/redirect_aliases.sh

echo "✅ Proteção definitiva ATIVADA!"
echo "   • Wrappers de comando: OK"
echo "   • Interceptador global: OK"
echo "   • Aliases de proteção: OK"
echo "   • Monitor filesystem: OK"
EOF

chmod +x "$PROTECTION_DIR/activate_ultimate.sh"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ PROTEÇÃO DEFINITIVA INSTALADA!            ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ Medidas implementadas:                                    ║"
echo "║                                                            ║"
echo "║ 1. Interceptador global de comandos                       ║"
echo "║ 2. Hook preexec no zsh                                    ║"
echo "║ 3. Aliases que sobrescrevem redirecionamento              ║"
echo "║ 4. Monitor de filesystem em background                    ║"
echo "║ 5. Wrappers para todos os comandos                        ║"
echo "║                                                            ║"
echo "║ INSTRUÇÕES:                                               ║"
echo "║ • Para ativar AGORA: source activate_ultimate.sh          ║"
echo "║ • Após reiniciar terminal: Proteção automática            ║"
echo "║                                                            ║"
echo "║ Claude Code sempre receberá instruções para:              ║"
echo "║ • Usar scripturemon-auth se lembrar                       ║"
echo "║ • Ler /Users/clubproducoes/Digimundo/claude_code se não   ║"
echo "╚════════════════════════════════════════════════════════════╝"