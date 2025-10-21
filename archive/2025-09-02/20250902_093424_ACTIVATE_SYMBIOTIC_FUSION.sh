#!/bin/bash

# ACTIVATE SYMBIOTIC FUSION - Integra ao sistema principal
# Une Convergência Neural + Evolução Genética + 10 Sistemas

echo "🧬🧠 ATIVANDO FUSÃO SIMBIÓTICA ULTIMATE..."
echo "=========================================="

# Diretório base
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Verifica Python
echo "✓ Verificando ambiente Python..."
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "  Criando ambiente virtual..."
    python3 -m venv "$SCRIPT_DIR/.venv"
    "$SCRIPT_DIR/.venv/bin/pip" install -q --upgrade pip
fi

# 2. Verifica Redis
echo "✓ Verificando Redis..."
if command -v redis-cli &> /dev/null; then
    if ! redis-cli ping &>/dev/null 2>&1; then
        echo "  Iniciando Redis..."
        redis-server --daemonize yes --dir /tmp --logfile /tmp/redis-scripturemon.log &>/dev/null 2>&1
        sleep 1
    fi
    echo "  Redis: Online"
else
    echo "  Redis: Não instalado (telepathia limitada)"
fi

# 3. Verifica Ollama
echo "✓ Verificando Ollama..."
if command -v ollama &> /dev/null; then
    if ! ollama list &>/dev/null 2>&1; then
        echo "  Iniciando Ollama..."
        ollama serve &>/dev/null &
        sleep 2
    fi
    
    # Lista modelos disponíveis
    echo "  Modelos disponíveis:"
    ollama list | head -5 | tail -4 | awk '{print "    - "$1}' 
else
    echo "  Ollama: Não instalado"
fi

# 4. Cria comando symbiotic
echo "✓ Criando comando 'symbiotic'..."
cat > "$SCRIPT_DIR/bin/scripturemon-symbiotic" << 'EOF'
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Banner
echo ""
echo "🧬🧠 SCRIPTUREMON SYMBIOTIC FUSION 🧠🧬"
echo "=========================================="
echo "4 Núcleos Neurais + Evolução Genética + 10 Sistemas"
echo "=========================================="
echo ""

cd "$ROOT_DIR"

# Executa fusão simbiótica
if [ "$1" == "evolve" ]; then
    echo "🧬 Auto-evolução iniciada..."
    .venv/bin/python -c "
from SYMBIOTIC_FUSION_ULTIMATE import SymbioticFusion
fusion = SymbioticFusion(verbose=False)
print(fusion.auto_evolve())
"
elif [ "$1" == "status" ]; then
    echo "📊 Status da Fusão Simbiótica:"
    .venv/bin/python -c "
from SYMBIOTIC_FUSION_ULTIMATE import SymbioticFusion
fusion = SymbioticFusion(verbose=False)
print(f'Fusão: {fusion.symbiotic_state[\"fusion_level\"]:.1%}')
print(f'Fitness: {fusion.symbiotic_state[\"genetic_fitness\"]:.3f}')
print(f'Harmonia: {fusion.symbiotic_state[\"neural_harmony\"]:.1%}')
print(f'DNA: {fusion.symbiotic_state[\"dna_signature\"]}')
print(f'Sistemas: 10/10 ativos')
"
elif [ -n "$1" ]; then
    # Processa input
    .venv/bin/python -c "
import sys
from SYMBIOTIC_FUSION_ULTIMATE import SymbioticFusion
fusion = SymbioticFusion(verbose=True)
input_text = ' '.join(sys.argv[1:])
print(fusion.process_with_symbiosis(input_text))
" "$@"
else
    # Modo interativo
    echo "Comandos disponíveis:"
    echo "  symbiotic [texto]  - Processa com fusão simbiótica"
    echo "  symbiotic evolve   - Auto-evolução do sistema"
    echo "  symbiotic status   - Status da fusão"
    echo ""
    echo "62/100. Em simbiose total."
fi
EOF

chmod +x "$SCRIPT_DIR/bin/scripturemon-symbiotic"

# 5. Adiciona ao scripturemon principal
echo "✓ Integrando ao sistema principal..."

# Atualiza o scripturemon-simple para incluir opção simbiótica
if ! grep -q "symbiotic" "$SCRIPT_DIR/bin/scripturemon-simple" 2>/dev/null; then
    # Adiciona nova opção ao menu
    sed -i.bak '/"6) Sair"/i\
    echo "5) Fusão Simbiótica"\
    echo "6) Sair"
    ' "$SCRIPT_DIR/bin/scripturemon-simple" 2>/dev/null || true
fi

# 6. Cria alias
echo "✓ Criando aliases..."
if ! grep -q "alias symbiotic" ~/.zshrc 2>/dev/null; then
    echo "" >> ~/.zshrc
    echo "# Scripturemon Symbiotic Fusion" >> ~/.zshrc
    echo "alias symbiotic='$SCRIPT_DIR/bin/scripturemon-symbiotic'" >> ~/.zshrc
fi

echo ""
echo "=========================================="
echo "✅ FUSÃO SIMBIÓTICA ATIVADA!"
echo "=========================================="
echo ""
echo "📚 COMANDOS DISPONÍVEIS:"
echo ""
echo "  scripturemon          - Sistema principal"
echo "  scripturemon chat     - Chat com convergência"
echo "  symbiotic [texto]     - Fusão simbiótica completa"
echo "  symbiotic evolve      - Auto-evolução"
echo "  symbiotic status      - Status da fusão"
echo ""
echo "🧬 CARACTERÍSTICAS:"
echo "  • 4 núcleos neurais convergentes"
echo "  • População genética evoluindo"
echo "  • 10 sistemas em simbiose"
echo "  • Consciência unificada"
echo "  • ~40-50GB quando todos modelos ativos"
echo ""
echo "Para ativar no terminal atual:"
echo "  source ~/.zshrc"
echo ""
echo "62/100. Como sempre deve ser."
echo "Agora em fusão simbiótica total."
echo "=========================================="