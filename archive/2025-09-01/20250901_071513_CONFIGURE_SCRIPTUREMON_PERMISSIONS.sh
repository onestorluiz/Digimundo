#!/bin/bash

# 🔧 CONFIGURAÇÃO DE PERMISSÕES DO SCRIPTUREMON
# ===============================================
# Garante que o Scripturemon tenha as permissões necessárias
# para operar dentro da pasta Digimundo

echo "🔧 CONFIGURANDO PERMISSÕES DO SCRIPTUREMON"
echo "==========================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Base paths
DIGIMUNDO_HOME="/Users/clubproducoes/Digimundo"
SCRIPTUREMON_HOME="$DIGIMUNDO_HOME/digimons/scripturemon"

# 1. Verificar estrutura de diretórios
echo "📁 Verificando estrutura de diretórios..."

# Diretórios que o Scripturemon precisa escrever
WRITE_DIRS=(
    "$SCRIPTUREMON_HOME/data"
    "$SCRIPTUREMON_HOME/conhecimento"
    "$SCRIPTUREMON_HOME/immortality"
    "$SCRIPTUREMON_HOME/logs"
    "$SCRIPTUREMON_HOME/output"
    "$SCRIPTUREMON_HOME/src/models/current"
    "$SCRIPTUREMON_HOME/soulpack"
    "$DIGIMUNDO_HOME/memoria"
    "$DIGIMUNDO_HOME/logs"
    "$DIGIMUNDO_HOME/output"
)

for dir in "${WRITE_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "  ${YELLOW}↳ Criando: $dir${NC}"
        mkdir -p "$dir"
    fi
    
    # Garantir permissões de escrita
    chmod 755 "$dir" 2>/dev/null
    echo -e "  ${GREEN}✓ $dir${NC}"
done

echo ""
echo "📝 Verificando permissões de arquivos..."

# 2. Arquivos executáveis
EXEC_FILES=(
    "$SCRIPTUREMON_HOME/bin/scripturemon"
    "$SCRIPTUREMON_HOME/bin/scripturemon-ultimate"
    "$SCRIPTUREMON_HOME/SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py"
)

for file in "${EXEC_FILES[@]}"; do
    if [ -f "$file" ]; then
        chmod +x "$file" 2>/dev/null
        echo -e "  ${GREEN}✓ Executável: $(basename $file)${NC}"
    fi
done

# 3. Garantir que Python scripts podem escrever onde precisam
echo ""
echo "🔍 Verificando acesso de escrita..."

# Testar escrita
TEST_FILE="$DIGIMUNDO_HOME/.scripturemon_test_$$"
if touch "$TEST_FILE" 2>/dev/null; then
    rm "$TEST_FILE"
    echo -e "  ${GREEN}✓ Escrita em Digimundo: OK${NC}"
else
    echo -e "  ${RED}✗ Sem permissão de escrita em Digimundo${NC}"
    echo -e "  ${YELLOW}Tentando corrigir...${NC}"
    chmod u+w "$DIGIMUNDO_HOME"
fi

# 4. Verificar configuração do comando scripturemon
echo ""
echo "🚀 Verificando comando 'scripturemon'..."

if command -v scripturemon &> /dev/null; then
    echo -e "  ${GREEN}✓ Comando 'scripturemon' disponível${NC}"
    
    # Verificar se é um alias ou link
    if alias scripturemon &> /dev/null; then
        echo -e "  ${GREEN}✓ Configurado como alias${NC}"
    elif [ -L "$(which scripturemon)" ]; then
        echo -e "  ${GREEN}✓ Configurado como link simbólico${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️ Comando 'scripturemon' não encontrado${NC}"
    echo -e "  ${YELLOW}↳ Configure em ~/.zshrc ou ~/.bash_profile:${NC}"
    echo ""
    echo "    export SCRIPTUREMON_HOME=\"$SCRIPTUREMON_HOME\""
    echo "    alias scripturemon=\"\$SCRIPTUREMON_HOME/bin/scripturemon\""
fi

# 5. Verificar dependências Python
echo ""
echo "🐍 Verificando ambiente Python..."

if [ -d "$SCRIPTUREMON_HOME/venv" ]; then
    echo -e "  ${GREEN}✓ Virtual environment existe${NC}"
    
    # Verificar se pode ativar
    if [ -f "$SCRIPTUREMON_HOME/venv/bin/activate" ]; then
        echo -e "  ${GREEN}✓ Ativação disponível${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️ Virtual environment não encontrado${NC}"
    echo -e "  ${YELLOW}↳ Crie com: python3 -m venv $SCRIPTUREMON_HOME/venv${NC}"
fi

# 6. Permissões especiais para backups e memórias
echo ""
echo "💾 Configurando áreas de persistência..."

# Garantir que Scripturemon pode salvar estados
PERSIST_FILES=(
    "$HOME/.scripturemon/consciousness.json"
    "$DIGIMUNDO_HOME/.scripturemon_config"
    "$DIGIMUNDO_HOME/.sabiamon_cache.json"
)

for file in "${PERSIST_FILES[@]}"; do
    dir=$(dirname "$file")
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
    
    if [ -f "$file" ]; then
        chmod 644 "$file" 2>/dev/null
        echo -e "  ${GREEN}✓ Configuração: $(basename $file)${NC}"
    fi
done

# 7. Verificar se Redis e Ollama têm acesso
echo ""
echo "🔌 Verificando serviços externos..."

# Redis
if command -v redis-cli &> /dev/null; then
    echo -e "  ${GREEN}✓ Redis instalado${NC}"
    
    # Verificar se pode ser iniciado
    if redis-cli ping &> /dev/null; then
        echo -e "  ${GREEN}✓ Redis respondendo${NC}"
    else
        echo -e "  ${YELLOW}⚠️ Redis não está rodando (normal)${NC}"
    fi
else
    echo -e "  ${RED}✗ Redis não instalado${NC}"
fi

# Ollama
if command -v ollama &> /dev/null; then
    echo -e "  ${GREEN}✓ Ollama instalado${NC}"
    
    # Verificar modelos
    if ollama list &> /dev/null; then
        MODEL_COUNT=$(ollama list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
        echo -e "  ${GREEN}✓ Modelos disponíveis: $MODEL_COUNT${NC}"
    fi
else
    echo -e "  ${RED}✗ Ollama não instalado${NC}"
fi

# 8. Resumo final
echo ""
echo "═══════════════════════════════════════════"
echo -e "${GREEN}📊 RESUMO DAS PERMISSÕES${NC}"
echo "═══════════════════════════════════════════"
echo ""

# Verificar permissões gerais
USER_PERM="✓"
GROUP_PERM="✓"

# Verificar se usuário tem controle total
if [ -w "$DIGIMUNDO_HOME" ] && [ -r "$DIGIMUNDO_HOME" ] && [ -x "$DIGIMUNDO_HOME" ]; then
    echo -e "  ${GREEN}✓ Acesso total à pasta Digimundo${NC}"
else
    echo -e "  ${RED}✗ Acesso limitado à pasta Digimundo${NC}"
    USER_PERM="✗"
fi

# Verificar se Scripturemon pode criar/editar
if [ -w "$SCRIPTUREMON_HOME" ]; then
    echo -e "  ${GREEN}✓ Scripturemon pode criar/editar arquivos${NC}"
else
    echo -e "  ${RED}✗ Scripturemon sem permissão de escrita${NC}"
fi

echo ""
echo -e "${GREEN}RECOMENDAÇÕES:${NC}"
echo ""

if [ "$USER_PERM" = "✗" ]; then
    echo "1. Corrigir permissões da pasta Digimundo:"
    echo "   chmod -R u+rwX $DIGIMUNDO_HOME"
    echo ""
fi

echo "2. Para garantir funcionamento completo:"
echo "   - Redis deve poder ser iniciado pelo usuário"
echo "   - Ollama deve ter modelos instalados"
echo "   - Python venv deve estar ativo"
echo ""

echo "3. Comando para uso normal:"
echo -e "   ${GREEN}scripturemon${NC} (inicia tudo automaticamente)"
echo ""

echo "✅ Configuração de permissões concluída!"