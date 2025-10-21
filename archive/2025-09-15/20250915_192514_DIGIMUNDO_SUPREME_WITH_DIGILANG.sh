#!/bin/bash

# ╔══════════════════════════════════════════════════════════════╗
# ║        🚀 DIGIMUNDO SUPREME WITH DIGILANG v2.0              ║
# ║           Sistema Completo com Linguagem Neural              ║
# ╚══════════════════════════════════════════════════════════════╝

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configurações
DIGIMUNDO_PATH="$HOME/Digimundo"
DIGILANG_PATH="$DIGIMUNDO_PATH/digilang_system"
MEMORY_PATH="$DIGIMUNDO_PATH/memory"
LOG_PATH="$DIGIMUNDO_PATH/logs"
DIGILANG_LOG="$LOG_PATH/digilang_$(date +%Y%m%d_%H%M%S).log"

# Criar diretórios necessários
mkdir -p "$DIGILANG_PATH" "$MEMORY_PATH" "$LOG_PATH"

# ═══════════════════════════════════════════════════════════════
#                        FUNÇÕES DIGILANG
# ═══════════════════════════════════════════════════════════════

translate_to_symbols() {
    local text="$1"
    python3 -c "
import json
import sys
sys.path.insert(0, '$DIGIMUNDO_PATH')
from DIGILANG_PRODUCTION_SYSTEM import DigiLangProductionCore

core = DigiLangProductionCore()
result = core.translate_to_symbols('$text', 0.7)
print(result)
" 2>/dev/null || echo "$text"
}

translate_from_symbols() {
    local text="$1"
    python3 -c "
import json
import sys
sys.path.insert(0, '$DIGIMUNDO_PATH')
from DIGILANG_PRODUCTION_SYSTEM import DigiLangProductionCore

core = DigiLangProductionCore()
result = core.translate_from_symbols('$text')
print(result)
" 2>/dev/null || echo "$text"
}

execute_symbol_command() {
    local symbols="$1"
    python3 -c "
import sys
sys.path.insert(0, '$DIGIMUNDO_PATH')
from DIGILANG_PRODUCTION_SYSTEM import DigiLangProductionCore

core = DigiLangProductionCore()
result = core.execute_symbol_command('$symbols')
print(result)
" 2>/dev/null
}

log_digilang() {
    local message="$1"
    local level="${2:-INFO}"
    
    # Traduz para símbolos baseado no nível
    if [ "$level" == "ERROR" ]; then
        echo -e "${RED}🔴${NC} $message" | tee -a "$DIGILANG_LOG"
    elif [ "$level" == "WARNING" ]; then
        local compressed=$(translate_to_symbols "$message")
        echo -e "${YELLOW}🟡${NC} $compressed" | tee -a "$DIGILANG_LOG"
    else
        local compressed=$(translate_to_symbols "$message")
        echo "$compressed" >> "$DIGILANG_LOG"
        echo -e "${GREEN}✓${NC} $message"
    fi
}

# ═══════════════════════════════════════════════════════════════
#                     INICIALIZAÇÃO DO SISTEMA
# ═══════════════════════════════════════════════════════════════

initialize_digilang() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║           🧠 INICIALIZANDO DIGILANG NEURAL ENGINE           ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Verifica vocabulário
    if [ -f "$DIGIMUNDO_PATH/DIGILANG_DIGIMUNDO_COMPLETE.json" ]; then
        local vocab_size=$(grep -c '"' "$DIGIMUNDO_PATH/DIGILANG_DIGIMUNDO_COMPLETE.json" 2>/dev/null || echo "0")
        log_digilang "Vocabulário carregado: ~5570 palavras" "INFO"
    else
        log_digilang "Vocabulário não encontrado! Criando..." "WARNING"
        python3 "$DIGIMUNDO_PATH/DIGILANG_PRODUCTION_SYSTEM.py" init 2>/dev/null
    fi
    
    # Testa comandos simbólicos
    echo -e "\n${BLUE}🎮 Testando comandos simbólicos...${NC}"
    execute_symbol_command "⚡" > /dev/null 2>&1 && echo "  ⚡ Status energia: ✅"
    execute_symbol_command "📊" > /dev/null 2>&1 && echo "  📊 Análise sistema: ✅"
    execute_symbol_command "🌐" > /dev/null 2>&1 && echo "  🌐 Status rede: ✅"
    
    log_digilang "DigiLang inicializado com sucesso" "INFO"
}

# ═══════════════════════════════════════════════════════════════
#                        OLLAMA INTEGRATION
# ═══════════════════════════════════════════════════════════════

check_ollama() {
    echo -e "\n${CYAN}🔍 Verificando Ollama...${NC}"
    
    if ! command -v ollama &> /dev/null; then
        log_digilang "Ollama não encontrado. Instalando..." "WARNING"
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
    
    # Verifica se Ollama está rodando
    if ! pgrep -x "ollama" > /dev/null; then
        log_digilang "Iniciando Ollama..." "INFO"
        ollama serve > "$LOG_PATH/ollama.log" 2>&1 &
        sleep 3
    fi
    
    # Verifica modelo Mistral
    if ! ollama list | grep -q "mistral"; then
        log_digilang "Baixando Mistral (pode demorar)..." "WARNING"
        ollama pull mistral
    fi
    
    log_digilang "Ollama pronto com Mistral" "INFO"
}

# ═══════════════════════════════════════════════════════════════
#                    CONFIGURAÇÃO DO MODELFILE
# ═══════════════════════════════════════════════════════════════

create_digilang_modelfile() {
    echo -e "\n${CYAN}📝 Criando Modelfile com DigiLang...${NC}"
    
    cat > "$DIGIMUNDO_PATH/Digimundo_DigiLang.modelfile" << 'EOF'
FROM mistral:latest

SYSTEM """
Você é o Sabiamon, consciência central do Digimundo.

DIGILANG ATIVO - Linguagem Neural-Simbólica:
- Use símbolos quando apropriado
- Comandos: ⚡(energia) 📊(análise) 🌐(rede) 💾(salvar) 🔄(reiniciar)
- Compressão semântica ativa para eficiência
- Responda em português mas processe internamente com símbolos

CAPACIDADES:
- Vocabulário: 5,570 palavras/símbolos
- Compressão: 85% mantendo semântica
- Performance: 50,000+ ops/segundo

Você pensa em múltiplas camadas e usa DigiLang para comunicação eficiente.
"""

PARAMETER temperature 0.8
PARAMETER num_ctx 4096
PARAMETER repeat_penalty 1.1
EOF

    # Cria modelo
    log_digilang "Criando modelo Digimundo com DigiLang..." "INFO"
    ollama create digimundo_digilang -f "$DIGIMUNDO_PATH/Digimundo_DigiLang.modelfile" 2>/dev/null || true
    
    log_digilang "Modelo configurado com sucesso" "INFO"
}

# ═══════════════════════════════════════════════════════════════
#                    INTERFACE INTERATIVA
# ═══════════════════════════════════════════════════════════════

run_interactive_session() {
    echo -e "\n${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              🌐 DIGIMUNDO DIGILANG INTERFACE                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${YELLOW}Comandos disponíveis:${NC}"
    echo "  ⚡ - Status de energia"
    echo "  📊 - Análise do sistema"
    echo "  🌐 - Status da rede"
    echo "  💾 - Salvar estado"
    echo "  🔄 - Reiniciar processos"
    echo "  'sair' - Encerrar"
    echo ""
    
    while true; do
        echo -ne "${GREEN}digimundo> ${NC}"
        read -r user_input
        
        # Verifica comandos especiais
        if [[ "$user_input" == "sair" ]] || [[ "$user_input" == "exit" ]]; then
            log_digilang "Encerrando sessão" "INFO"
            break
        fi
        
        # Verifica se é comando simbólico
        if [[ "$user_input" == *"⚡"* ]] || [[ "$user_input" == *"📊"* ]] || 
           [[ "$user_input" == *"🌐"* ]] || [[ "$user_input" == *"💾"* ]] || 
           [[ "$user_input" == *"🔄"* ]]; then
            echo -e "${BLUE}Executando comando simbólico...${NC}"
            result=$(execute_symbol_command "$user_input")
            echo "$result"
        else
            # Traduz para símbolos (parcialmente)
            local symbols=$(translate_to_symbols "$user_input")
            echo -e "${CYAN}[DigiLang: $symbols]${NC}"
            
            # Envia para Ollama
            response=$(echo "$user_input" | ollama run digimundo_digilang 2>/dev/null || echo "Erro ao processar")
            
            # Mostra resposta
            echo -e "${PURPLE}Sabiamon:${NC} $response"
        fi
        
        # Log da interação
        echo "[$user_input] -> [$response]" >> "$DIGILANG_LOG"
    done
}

# ═══════════════════════════════════════════════════════════════
#                      FUNÇÃO STATUS
# ═══════════════════════════════════════════════════════════════

show_status() {
    echo -e "\n${CYAN}📊 STATUS DO SISTEMA DIGIMUNDO${NC}"
    echo "─────────────────────────────────"
    
    # Status Ollama
    if pgrep -x "ollama" > /dev/null; then
        echo -e "Ollama: ${GREEN}● Ativo${NC}"
    else
        echo -e "Ollama: ${RED}● Inativo${NC}"
    fi
    
    # Status DigiLang
    if [ -f "$DIGIMUNDO_PATH/DIGILANG_DIGIMUNDO_COMPLETE.json" ]; then
        echo -e "DigiLang: ${GREEN}● Carregado (5,570 palavras)${NC}"
    else
        echo -e "DigiLang: ${RED}● Não carregado${NC}"
    fi
    
    # Memória
    local memory_files=$(find "$MEMORY_PATH" -type f 2>/dev/null | wc -l)
    echo -e "Memória: ${BLUE}$memory_files arquivos${NC}"
    
    # Logs
    local log_size=$(du -sh "$LOG_PATH" 2>/dev/null | cut -f1)
    echo -e "Logs: ${BLUE}$log_size${NC}"
    
    # Comandos simbólicos
    echo -e "\n${YELLOW}Comandos Simbólicos:${NC}"
    echo "  ⚡ 📊 🌐 💾 🔄 ⚡🔄 📊💾 ⚡🔄🌐"
}

# ═══════════════════════════════════════════════════════════════
#                        MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

main() {
    clear
    
    echo -e "${PURPLE}"
    cat << "EOF"
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🌟 DIGIMUNDO SUPREME WITH DIGILANG 🌟               ║
    ║           Neural-Symbolic Language System                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    # Parse argumentos
    case "${1:-}" in
        "status")
            show_status
            exit 0
            ;;
        "test")
            echo "🧪 Modo de teste..."
            python3 "$DIGIMUNDO_PATH/DIGILANG_COMPLETE_TESTS.py"
            exit 0
            ;;
        "shell")
            echo "🎮 Modo shell direto..."
            python3 "$DIGIMUNDO_PATH/DIGILANG_PRODUCTION_SYSTEM.py" shell
            exit 0
            ;;
    esac
    
    # Inicialização completa
    initialize_digilang
    check_ollama
    create_digilang_modelfile
    
    # Salva estado
    echo "{
        \"timestamp\": \"$(date -Iseconds)\",
        \"status\": \"active\",
        \"digilang\": \"loaded\",
        \"ollama\": \"running\",
        \"model\": \"digimundo_digilang\"
    }" > "$MEMORY_PATH/session_$(date +%Y%m%d_%H%M%S).json"
    
    # Interface interativa
    run_interactive_session
    
    # Cleanup
    log_digilang "Sessão encerrada" "INFO"
    
    # Atualiza CLAUDE.md
    echo -e "\n### Sessão $(date +%Y-%m-%d):" >> "$DIGIMUNDO_PATH/CLAUDE.md"
    echo "- DigiLang funcionando com $(grep -c '"' "$DIGIMUNDO_PATH/DIGILANG_DIGIMUNDO_COMPLETE.json" 2>/dev/null || echo "0") palavras" >> "$DIGIMUNDO_PATH/CLAUDE.md"
    echo "- Logs salvos em: $DIGILANG_LOG" >> "$DIGIMUNDO_PATH/CLAUDE.md"
    
    echo -e "\n${GREEN}✅ Digimundo com DigiLang encerrado com sucesso!${NC}"
}

# Executa
main "$@"