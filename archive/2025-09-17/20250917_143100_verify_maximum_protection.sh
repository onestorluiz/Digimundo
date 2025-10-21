#!/bin/bash
#════════════════════════════════════════════════════════════════
# VERIFICAÇÃO DO SISTEMA DE PROTEÇÃO MÁXIMA
#════════════════════════════════════════════════════════════════

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       🔐 VERIFICAÇÃO DO MAXIMUM PROTECTION SYSTEM         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# 1. Verifica Daemon
echo -e "${YELLOW}1. DAEMON STATUS:${NC}"
PID_FILE="/Users/clubproducoes/Digimundo/claude_code/protection/.maximum_protection.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo -e "  ${GREEN}✅ Daemon rodando (PID: $PID)${NC}"
    else
        echo -e "  ${RED}❌ Daemon não está rodando${NC}"
    fi
else
    echo -e "  ${RED}❌ PID file não encontrado${NC}"
fi

# 2. Verifica LaunchDaemon
echo -e "\n${YELLOW}2. LAUNCHDAEMON:${NC}"
if launchctl list | grep -q "com.scripturemon.maximum.protection"; then
    echo -e "  ${GREEN}✅ LaunchDaemon instalado e ativo${NC}"
    echo "     Para iniciar no boot do sistema"
else
    echo -e "  ${RED}❌ LaunchDaemon não instalado${NC}"
fi

# 3. Verifica Wrappers
echo -e "\n${YELLOW}3. COMMAND WRAPPERS:${NC}"
WRAPPER_DIR="/Users/clubproducoes/Digimundo/claude_code/protection/wrappers"

if [ -d "$WRAPPER_DIR" ]; then
    WRAPPER_COUNT=$(ls "$WRAPPER_DIR" | wc -l)
    echo -e "  ${GREEN}✅ $WRAPPER_COUNT wrappers instalados${NC}"

    # Lista alguns wrappers
    echo "     Comandos protegidos:"
    for cmd in rm mv cp cat sed; do
        if [ -f "$WRAPPER_DIR/$cmd" ]; then
            echo -e "       ${GREEN}•${NC} $cmd"
        fi
    done
else
    echo -e "  ${RED}❌ Diretório de wrappers não encontrado${NC}"
fi

# 4. Verifica Perfil do Shell
echo -e "\n${YELLOW}4. SHELL PROFILE:${NC}"
if grep -q "MAXIMUM PROTECTION SYSTEM" ~/.zshrc 2>/dev/null; then
    echo -e "  ${GREEN}✅ Proteção adicionada ao .zshrc${NC}"
elif grep -q "MAXIMUM PROTECTION SYSTEM" ~/.bashrc 2>/dev/null; then
    echo -e "  ${GREEN}✅ Proteção adicionada ao .bashrc${NC}"
else
    echo -e "  ${RED}❌ Proteção não encontrada no perfil do shell${NC}"
fi

# 5. Verifica Hooks Python
echo -e "\n${YELLOW}5. PYTHON HOOKS:${NC}"
SITECUSTOMIZE="/opt/homebrew/lib/python3.13/site-packages/sitecustomize.py"

if [ -f "$SITECUSTOMIZE" ]; then
    if grep -q "MAXIMUM PROTECTION" "$SITECUSTOMIZE" 2>/dev/null; then
        echo -e "  ${GREEN}✅ Hooks Python instalados${NC}"
        echo "     Proteção automática em scripts Python"
    else
        echo -e "  ${YELLOW}⚠️ sitecustomize.py existe mas sem proteção${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️ sitecustomize.py não encontrado${NC}"
fi

# 6. Verifica Processos Monitorados
echo -e "\n${YELLOW}6. PROCESSOS MONITORADOS:${NC}"
MONITOR_LOG="/Users/clubproducoes/Digimundo/claude_code/protection/monitor.log"

if [ -f "$MONITOR_LOG" ]; then
    RECENT_LOGS=$(tail -5 "$MONITOR_LOG" 2>/dev/null | wc -l)
    echo -e "  ${GREEN}✅ Monitor log ativo${NC}"
    echo "     $RECENT_LOGS entradas recentes"
else
    echo -e "  ${YELLOW}⚠️ Log de monitoramento não iniciado${NC}"
fi

# 7. Verifica ACLs do Filesystem
echo -e "\n${YELLOW}7. FILESYSTEM ACLs:${NC}"
PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"

if ls -le "$PROTECTED_DIR" 2>/dev/null | grep -q "deny"; then
    echo -e "  ${GREEN}✅ ACLs configuradas no diretório protegido${NC}"
    echo "     Proteção adicional contra modificações"
else
    echo -e "  ${YELLOW}⚠️ ACLs não configuradas${NC}"
fi

# 8. Teste de Proteção
echo -e "\n${YELLOW}8. TESTE DE PROTEÇÃO:${NC}"
echo -e "  Tentando criar arquivo de teste..."

# Tenta criar arquivo sem autorização
TEST_FILE="$PROTECTED_DIR/test_protection_$(date +%s).txt"

# Usa o wrapper se disponível
if [ -d "$WRAPPER_DIR" ]; then
    export PATH="$WRAPPER_DIR:$PATH"
fi

# Tenta operação
echo "teste" > "$TEST_FILE" 2>&1

if [ -f "$TEST_FILE" ]; then
    echo -e "  ${YELLOW}⚠️ Arquivo criado (sessão pode estar ativa)${NC}"
    rm -f "$TEST_FILE" 2>/dev/null
else
    echo -e "  ${GREEN}✅ Operação protegida funcionando${NC}"
fi

# RESUMO FINAL
echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}                    📊 RESUMO DO SISTEMA                       ${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"

TOTAL_CHECKS=8
PASSED=0

# Conta verificações bem-sucedidas
[ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null 2>&1 && PASSED=$((PASSED + 1))
launchctl list | grep -q "com.scripturemon.maximum.protection" 2>/dev/null && PASSED=$((PASSED + 1))
[ -d "$WRAPPER_DIR" ] && PASSED=$((PASSED + 1))
grep -q "MAXIMUM PROTECTION SYSTEM" ~/.zshrc 2>/dev/null && PASSED=$((PASSED + 1))
[ -f "$SITECUSTOMIZE" ] && grep -q "MAXIMUM PROTECTION" "$SITECUSTOMIZE" 2>/dev/null && PASSED=$((PASSED + 1))
[ -f "$MONITOR_LOG" ] && PASSED=$((PASSED + 1))
ls -le "$PROTECTED_DIR" 2>/dev/null | grep -q "deny" && PASSED=$((PASSED + 1))

PERCENTAGE=$((PASSED * 100 / TOTAL_CHECKS))

echo -e "\n${PURPLE}Status Geral: ${PASSED}/${TOTAL_CHECKS} verificações OK (${PERCENTAGE}%)${NC}"

if [ $PERCENTAGE -eq 100 ]; then
    echo -e "${GREEN}🏆 SISTEMA DE PROTEÇÃO MÁXIMA 100% OPERACIONAL!${NC}"
elif [ $PERCENTAGE -ge 75 ]; then
    echo -e "${GREEN}✅ Sistema operacional com pequenos ajustes necessários${NC}"
elif [ $PERCENTAGE -ge 50 ]; then
    echo -e "${YELLOW}⚠️ Sistema parcialmente operacional${NC}"
else
    echo -e "${RED}❌ Sistema precisa de configuração${NC}"
fi

echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Para usar o sistema:${NC}"
echo "  1. Reinicie o terminal para ativar todas as proteções"
echo "  2. Use 'scripturemon-auth' quando solicitado"
echo "  3. Sessões duram 15 segundos"
echo "  4. Daemon reinicia automaticamente no boot"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"