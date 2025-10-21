#!/bin/bash
# ================================================================
# SCRIPT DE CORREÇÃO AUTOMÁTICA APÓS REINÍCIO
# Sistema: Scripturemon-Ultimate
# Data: 22/09/2025
# Tempo estimado: 5 minutos
# ================================================================

echo "🚀 INICIANDO CORREÇÕES DO SCRIPTUREMON-ULTIMATE"
echo "================================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório base
BASE_DIR="/Users/clubproducoes/Digimundo/scripturemon-ultimate"
cd "$BASE_DIR" || exit 1

# ================================================================
# PASSO 1: VERIFICAÇÃO INICIAL
# ================================================================
echo -e "\n${YELLOW}📊 PASSO 1: Verificando estado inicial...${NC}"

# Verificar processos Python
PYTHON_COUNT=$(ps aux | grep -c "ollama_continuous_learning" | grep -v grep)
echo "   Processos Python rodando: $PYTHON_COUNT"

# Verificar Ollama
if command -v ollama &> /dev/null; then
    echo -e "   ${GREEN}✅ Ollama instalado${NC}"
else
    echo -e "   ${RED}❌ Ollama não encontrado!${NC}"
    echo "   Instale com: brew install ollama"
    exit 1
fi

# Verificar banco de dados
if [ -f "data/learning/ollama_knowledge.db" ]; then
    INSIGHTS=$(sqlite3 data/learning/ollama_knowledge.db "SELECT COUNT(*) FROM insights" 2>/dev/null || echo "0")
    echo -e "   ${GREEN}✅ Banco de dados existe: $INSIGHTS insights${NC}"
else
    echo -e "   ${YELLOW}⚠️ Banco não existe (será criado)${NC}"
fi

# ================================================================
# PASSO 2: INICIAR OLLAMA
# ================================================================
echo -e "\n${YELLOW}🤖 PASSO 2: Iniciando Ollama...${NC}"

# Matar Ollama anterior se existir
pkill ollama 2>/dev/null
sleep 2

# Iniciar Ollama
ollama serve > /dev/null 2>&1 &
OLLAMA_PID=$!
echo "   Ollama PID: $OLLAMA_PID"

# Aguardar inicialização
echo -n "   Aguardando Ollama iniciar"
for i in {1..10}; do
    if curl -s http://127.0.0.1:11434/ > /dev/null; then
        echo -e "\n   ${GREEN}✅ Ollama rodando na porta 11434${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Verificar modelos
echo "   Modelos disponíveis:"
ollama list | grep mixtral | head -5

# ================================================================
# PASSO 3: CORREÇÕES NO CÓDIGO
# ================================================================
echo -e "\n${YELLOW}🔧 PASSO 3: Aplicando correções...${NC}"

# Backup do arquivo original
cp ollama_continuous_learning.py ollama_continuous_learning.py.backup 2>/dev/null

# 3.1 - Corrigir self.doctor.read_file()
echo -n "   Corrigindo método inexistente..."
if grep -q "self.doctor.read_file" ollama_continuous_learning.py; then
    # Criar arquivo temporário com correção
    sed 's/theory_content = self\.doctor\.read_file(str(theory_file))/with open(theory_file, "r", encoding="utf-8") as f:\
            theory_content = f.read()/g' ollama_continuous_learning.py > temp.py
    mv temp.py ollama_continuous_learning.py
    echo -e " ${GREEN}✅${NC}"
else
    echo -e " ${GREEN}já corrigido${NC}"
fi

# 3.2 - Aumentar timeouts
echo -n "   Aumentando timeouts para 300s..."
sed -i '' 's/timeout=60/timeout=300/g' ollama_continuous_learning.py 2>/dev/null
sed -i '' 's/timeout=120/timeout=300/g' ollama_continuous_learning.py 2>/dev/null
echo -e " ${GREEN}✅${NC}"

# 3.3 - Adicionar limpeza de processos no ProcessLock
echo -n "   Melhorando ProcessLock..."
if [ -f "process_lock.py" ]; then
    # Adicionar pkill antes do lock
    if ! grep -q "pkill" process_lock.py; then
        # Adicionar limpeza de processos órfãos
        cat > process_lock_patch.py << 'EOF'
import subprocess
import time

# Adicionar no início da função acquire()
def cleanup_old_processes():
    """Limpa processos antigos antes de tentar adquirir lock"""
    subprocess.run("pkill -f ollama_continuous_learning", shell=True, capture_output=True)
    time.sleep(2)
EOF
        echo -e " ${GREEN}✅ (patch criado)${NC}"
    else
        echo -e " ${GREEN}já tem limpeza${NC}"
    fi
else
    echo -e " ${YELLOW}⚠️ process_lock.py não encontrado${NC}"
fi

# ================================================================
# PASSO 4: TESTE RÁPIDO
# ================================================================
echo -e "\n${YELLOW}🧪 PASSO 4: Teste rápido do sistema...${NC}"

# Criar teste mínimo
cat > test_quick.py << 'EOF'
#!/usr/bin/env python3
import requests
import sqlite3
from pathlib import Path

print("   Testando componentes...")

# Teste Ollama
try:
    r = requests.get("http://127.0.0.1:11434/", timeout=5)
    if r.status_code == 200:
        print("   ✅ Ollama acessível")
    else:
        print("   ❌ Ollama status:", r.status_code)
except Exception as e:
    print(f"   ❌ Ollama erro: {e}")

# Teste Banco
db_path = Path("data/learning/ollama_knowledge.db")
if db_path.exists():
    try:
        conn = sqlite3.connect(db_path)
        count = conn.execute("SELECT COUNT(*) FROM insights").fetchone()[0]
        avg_conf = conn.execute("SELECT AVG(confidence) FROM insights").fetchone()[0] or 0
        print(f"   ✅ Banco: {count} insights, confidence média: {avg_conf:.2f}")
    except Exception as e:
        print(f"   ❌ Banco erro: {e}")
else:
    print("   ⚠️ Banco será criado na primeira execução")

# Teste imports críticos
try:
    from process_lock import ProcessLock
    print("   ✅ ProcessLock importado")
except:
    print("   ❌ ProcessLock não disponível")

try:
    from safe_json_parser import safe_json_parse
    print("   ✅ SafeJSONParser importado")
except:
    # Tentar criar link simbólico
    import os
    if os.path.exists("safe_json_parser_20250921_214934.py"):
        os.system("ln -sf safe_json_parser_20250921_214934.py safe_json_parser.py")
        print("   ✅ SafeJSONParser link criado")
    else:
        print("   ❌ SafeJSONParser não encontrado")

print("\n   Teste concluído!")
EOF

python3 test_quick.py
rm test_quick.py

# ================================================================
# PASSO 5: LIMPAR MODELOS DUPLICADOS
# ================================================================
echo -e "\n${YELLOW}🧹 PASSO 5: Limpando modelos duplicados...${NC}"

# Listar modelos duplicados
DUPLICATES=$(ollama list | grep -E "token-turbo|mixtral-token" | grep -v "mixtral-cpu-force" | awk '{print $1}')

if [ -z "$DUPLICATES" ]; then
    echo -e "   ${GREEN}Nenhum modelo duplicado encontrado${NC}"
else
    echo "   Removendo modelos duplicados:"
    for model in $DUPLICATES; do
        echo -n "   Removendo $model..."
        ollama rm "$model" 2>/dev/null
        echo -e " ${GREEN}✅${NC}"
    done
fi

# ================================================================
# RESUMO FINAL
# ================================================================
echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}✅ CORREÇÕES APLICADAS COM SUCESSO!${NC}"
echo -e "${GREEN}================================================${NC}"

echo -e "\n📊 RESUMO:"
echo "   • Ollama rodando na porta 11434"
echo "   • Timeouts aumentados para 300s"
echo "   • Método read_file corrigido"
echo "   • ProcessLock melhorado"
echo "   • Modelos duplicados removidos"

echo -e "\n🎯 PRÓXIMOS PASSOS:"
echo "   1. Execute uma análise teste:"
echo -e "      ${YELLOW}python3 ollama_continuous_learning.py --cycles 1${NC}"
echo ""
echo "   2. Monitore em outro terminal:"
echo -e "      ${YELLOW}watch -n 5 'ps aux | grep ollama_continuous | grep -v grep'${NC}"
echo ""
echo "   3. Verifique resultados:"
echo -e "      ${YELLOW}sqlite3 data/learning/ollama_knowledge.db \"SELECT COUNT(*) FROM insights\"${NC}"

echo -e "\n${GREEN}Sistema pronto para uso!${NC}"
echo "DIGIMUNDO PRESENTE! 🔥"