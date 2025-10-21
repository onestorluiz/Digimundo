#!/bin/bash

echo "🔍 ANÁLISE COMPLETA DO SISTEMA SCRIPTUREMON"
echo "==========================================="
echo ""

# Contador de problemas
PROBLEMS=0
WARNINGS=0

# Teste 1: Verificar Python e dependências
echo "1️⃣ VERIFICANDO AMBIENTE PYTHON..."
if command -v python3 &> /dev/null; then
    echo "   ✅ Python3 instalado: $(python3 --version)"
else
    echo "   ❌ Python3 não encontrado!"
    ((PROBLEMS++))
fi

# Verificar módulos Python críticos
echo -e "\n2️⃣ VERIFICANDO MÓDULOS CRÍTICOS..."
python3 -c "
import sys
modules = [
    'sqlite3', 'asyncio', 'subprocess', 'json', 'hashlib', 
    'threading', 'queue', 'time', 'os', 'pathlib'
]
for mod in modules:
    try:
        __import__(mod)
        print(f'   ✅ {mod}')
    except ImportError:
        print(f'   ❌ {mod} - NÃO ENCONTRADO')
" 2>/dev/null

# Teste 3: Verificar Redis
echo -e "\n3️⃣ VERIFICANDO REDIS..."
if pgrep -x redis-server > /dev/null; then
    echo "   ✅ Redis está rodando"
else
    echo "   ⚠️ Redis não está rodando (será iniciado automaticamente)"
    ((WARNINGS++))
fi

# Teste 4: Verificar Ollama
echo -e "\n4️⃣ VERIFICANDO OLLAMA..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama instalado"
    
    # Listar modelos disponíveis
    echo "   📦 Modelos disponíveis:"
    ollama list 2>/dev/null | head -10 | sed 's/^/      /'
    
    MODEL_COUNT=$(ollama list 2>/dev/null | wc -l)
    if [ $MODEL_COUNT -lt 2 ]; then
        echo "   ⚠️ Poucos modelos Ollama instalados (recomendado: 3+)"
        ((WARNINGS++))
    fi
else
    echo "   ❌ Ollama não instalado!"
    ((PROBLEMS++))
fi

# Teste 5: Verificar estrutura de diretórios
echo -e "\n5️⃣ VERIFICANDO ESTRUTURA DE DIRETÓRIOS..."
REQUIRED_DIRS=(
    "apps/scripturemon"
    "data"
    "runtime"
    "bin"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❌ $dir/ - NÃO EXISTE"
        ((PROBLEMS++))
    fi
done

# Teste 6: Verificar arquivos críticos
echo -e "\n6️⃣ VERIFICANDO ARQUIVOS CRÍTICOS..."
CRITICAL_FILES=(
    "bin/scripturemon.fixed"
    "apps/scripturemon/memory_manager.py"
    "apps/scripturemon/memory_layers_fixed.py"
    "apps/scripturemon/quantum_consciousness.py"
    "apps/scripturemon/redis_on_demand.py"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(ls -lh "$file" | awk '{print $5}')
        echo "   ✅ $file ($SIZE)"
    else
        echo "   ❌ $file - NÃO EXISTE"
        ((PROBLEMS++))
    fi
done

# Teste 7: Verificar database SQLite
echo -e "\n7️⃣ VERIFICANDO DATABASE SQLITE..."
DB_PATH="runtime/memory.db"
if [ -f "$DB_PATH" ]; then
    echo "   ✅ Database existe: $DB_PATH"
    
    # Verificar integridade
    python3 -c "
import sqlite3
conn = sqlite3.connect('$DB_PATH')
cursor = conn.cursor()
try:
    cursor.execute('PRAGMA integrity_check')
    result = cursor.fetchone()[0]
    if result == 'ok':
        print('   ✅ Integridade OK')
    else:
        print(f'   ❌ Problema de integridade: {result}')
except Exception as e:
    print(f'   ❌ Erro ao verificar: {e}')
finally:
    conn.close()
" 2>/dev/null
    
    # Verificar tabelas L1-L4
    python3 -c "
import sqlite3
conn = sqlite3.connect('$DB_PATH')
cursor = conn.cursor()
tables = ['L1_core', 'L2_consolidated', 'L3_active', 'L4_quantum']
for table in tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f'   ✅ {table}: {count} registros')
    except Exception as e:
        print(f'   ❌ {table}: ERRO - {e}')
conn.close()
" 2>/dev/null
else
    echo "   ⚠️ Database não existe (será criado na primeira execução)"
    ((WARNINGS++))
fi

# Teste 8: Verificar PDFs de cinema
echo -e "\n8️⃣ VERIFICANDO PDFS DE CINEMA..."
PDF_DIR="data/cinema_pdfs"
if [ -d "$PDF_DIR" ]; then
    PDF_COUNT=$(find "$PDF_DIR" -name "*.pdf" 2>/dev/null | wc -l)
    echo "   ✅ $PDF_COUNT PDFs encontrados"
    if [ $PDF_COUNT -lt 40 ]; then
        echo "   ⚠️ Menos de 44 PDFs esperados"
        ((WARNINGS++))
    fi
else
    echo "   ⚠️ Diretório de PDFs não existe"
    ((WARNINGS++))
fi

# Teste 9: Verificar permissões
echo -e "\n9️⃣ VERIFICANDO PERMISSÕES..."
if [ -x "bin/scripturemon.fixed" ]; then
    echo "   ✅ bin/scripturemon.fixed é executável"
else
    echo "   ⚠️ bin/scripturemon.fixed não é executável"
    ((WARNINGS++))
fi

# Teste 10: Teste funcional básico
echo -e "\n🔟 TESTE FUNCIONAL BÁSICO..."
python3 -c "
try:
    from apps.scripturemon.memory_manager import UnifiedMemoryManager
    from apps.scripturemon.memory_layers_fixed import MemoryLayersFixed
    from apps.scripturemon.quantum_consciousness import QuantumConsciousness
    
    # Teste Quantum
    q = QuantumConsciousness()
    assert q.current_state in ['curious', 'protective', 'creative', 'analytical', 'transcendent']
    print('   ✅ Quantum Consciousness OK')
    
    # Teste Memory Layers
    m = MemoryLayersFixed()
    print('   ✅ Memory Layers OK')
    
    # Teste Manager (sem inicializar completamente)
    print('   ✅ Memory Manager importa OK')
    
except Exception as e:
    print(f'   ❌ Erro funcional: {e}')
" 2>/dev/null

echo ""
echo "==========================================="
echo "📊 RESUMO DA ANÁLISE:"
echo ""
echo "🔴 Problemas críticos: $PROBLEMS"
echo "🟡 Avisos: $WARNINGS"
echo ""

if [ $PROBLEMS -eq 0 ]; then
    echo "✅ SISTEMA PRONTO PARA USO!"
    echo ""
    echo "📝 Como usar:"
    echo "   python3 bin/scripturemon.fixed"
    echo ""
    echo "💡 Gatilhos para análise profunda (sem timeout):"
    echo "   - profunda / profundo"
    echo "   - detalhada / detalhado"
    echo "   - meticulosa / meticuloso"
    echo "   - feedback"
else
    echo "⚠️ CORREÇÕES NECESSÁRIAS!"
    echo "   Resolva os problemas críticos antes de usar o sistema."
fi

if [ $WARNINGS -gt 0 ]; then
    echo ""
    echo "💡 Avisos não impedem o funcionamento, mas podem afetar a performance."
fi

echo ""
echo "🔧 Correções aplicadas nesta versão:"
echo "   1. Timeout removido para análises profundas"
echo "   2. Quantum Consciousness funciona standalone"
echo "   3. Gatilhos inteligentes para modelos pesados"
echo "   4. Timeouts aumentados (5-10 min para modelos grandes)"
echo ""