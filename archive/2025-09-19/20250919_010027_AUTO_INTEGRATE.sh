#!/bin/bash
# 🔄 AUTO INTEGRATE - Integração automática no Sistema Unificado de Memória

echo "🔄 AUTO INTEGRATE - Sistema de Integração Automática"
echo "===================================================="
echo ""

# Verificar se arquivo foi passado
if [ $# -eq 0 ]; then
    echo "Uso: ./AUTO_INTEGRATE.sh <arquivo_ou_texto>"
    echo ""
    echo "Exemplos:"
    echo "  ./AUTO_INTEGRATE.sh novo_conhecimento.md"
    echo "  ./AUTO_INTEGRATE.sh 'Descoberta: sistema X faz Y'"
    exit 1
fi

INPUT="$1"

# Detectar se é arquivo ou texto
if [ -f "$INPUT" ]; then
    echo "📄 Integrando arquivo: $INPUT"

    # Extrair nome do arquivo sem path
    FILENAME=$(basename "$INPUT")

    # Copiar para pasta de memória se não estiver lá
    if [[ "$INPUT" != *"/claude_code/memory/"* ]]; then
        cp "$INPUT" /Users/clubproducoes/Digimundo/claude_code/memory/
        echo "  ✅ Arquivo copiado para /memory/"
    fi

    # Adicionar ao sistema unificado
    python3 - << EOF
import sys
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory')
from UNIFIED_MEMORY_SYSTEM import UnifiedMemorySystem

ums = UnifiedMemorySystem()

# Registrar novo arquivo
with open('$INPUT') as f:
    content = f.read()

ums.remember(f"Novo arquivo integrado: $FILENAME", "knowledge")

# Atualizar índice de conhecimento
ums._index_knowledge()

print("  ✅ Arquivo indexado no sistema unificado")
print(f"  📊 Total de documentos: {len(ums.cache['connections']['knowledge_index'])}")
EOF

else
    echo "💬 Integrando texto direto..."

    # Salvar texto no sistema
    python3 - << EOF
import sys
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory')
from UNIFIED_MEMORY_SYSTEM import UnifiedMemorySystem

ums = UnifiedMemorySystem()
ums.remember("$INPUT", "manual")

print("  ✅ Texto salvo no sistema unificado")
EOF
fi

echo ""
echo "🔍 Verificando integração..."

python3 - << EOF
import sys
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory')
from UNIFIED_MEMORY_SYSTEM import UnifiedMemorySystem

ums = UnifiedMemorySystem()

# Mostrar estatísticas
print(f"📊 Estatísticas do Sistema:")
print(f"  • Memórias: {len(ums.cache['memories'])}")
print(f"  • Decisões: {len(ums.cache['decisions'])}")
print(f"  • Regras: {len(ums.cache['rules'])}")
print(f"  • Documentos: {len(ums.cache['connections']['knowledge_index'])}")
print(f"  • Última sync: {ums.cache['last_sync']}")
EOF

echo ""
echo "✅ INTEGRAÇÃO COMPLETA!"
echo "DIGIMUNDO PRESENTE"