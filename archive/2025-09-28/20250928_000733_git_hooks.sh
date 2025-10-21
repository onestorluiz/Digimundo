#!/bin/bash
# 🔄 GIT HOOKS - Sincronização automática com memória

MEMORY_DIR="/Users/clubproducoes/Digimundo/claude_code/memory"
PYTHON="/usr/bin/python3"

# Função para instalar hooks
install_hooks() {
    echo "📦 Instalando Git hooks..."

    # Pre-commit: Verificar vícios do Claude
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Verifica vícios do Claude antes de commitar

echo "🔍 Verificando vícios do Claude..."
python3 /Users/clubproducoes/Digimundo/claude_code/memory/core/alerts.py

if [ $? -ne 0 ]; then
    echo "⚠️ Vícios detectados! Corrija antes de commitar."
    exit 1
fi

echo "✅ Sem vícios detectados!"
EOF

    # Post-commit: Atualizar sistema de memória
    cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Atualiza sistema de memória após commit

echo "🧠 Atualizando sistema de memória..."

# Salva commit no sistema
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_HASH=$(git log -1 --pretty=%H)

python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '/Users/clubproducoes/Digimundo/claude_code/memory/core')
from UNIFIED_SYSTEM import UnifiedMemorySystem

ums = UnifiedMemorySystem()
ums.remember(f'Git commit: {COMMIT_HASH[:8]} - {COMMIT_MSG}', 'git_history')
print('✅ Memória atualizada!')
" 2>/dev/null

# Atualiza índice de conhecimento
python3 -c "
print('📚 Atualizando índice de conhecimento...')
# Aqui poderia regenerar INDEX.md automaticamente
"
EOF

    # Post-merge: Sincronizar com Genjutsu
    cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash
# Sincroniza com Genjutsu após merge

echo "🌀 Sincronizando com Genjutsu..."

# Verifica se Genjutsu está rodando
ps aux | grep GENJUTSU | grep -v grep > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Genjutsu ativo - sistema protegido"
else
    echo "⚠️ Genjutsu inativo - iniciando..."
    /Users/clubproducoes/Digimundo/claude_code/START_GENJUTSU.sh &
fi

# Sincroniza adapters
python3 /Users/clubproducoes/Digimundo/claude_code/memory/core/adapters.py
EOF

    # Torna hooks executáveis
    chmod +x .git/hooks/pre-commit
    chmod +x .git/hooks/post-commit
    chmod +x .git/hooks/post-merge

    echo "✅ Hooks instalados com sucesso!"
}

# Função para criar aliases úteis
create_aliases() {
    echo "🎯 Criando aliases úteis..."

    git config alias.remember 'commit -m "🧠 Memory:"'
    git config alias.learn 'commit -m "📚 Learning:"'
    git config alias.decide 'commit -m "🎯 Decision:"'
    git config alias.fix-vicio 'commit -m "🔧 Fix vício:"'
    git config alias.harmony 'commit -m "🌀 Harmony:"'

    echo "✅ Aliases criados!"
    echo ""
    echo "📝 Aliases disponíveis:"
    echo "  git remember 'mensagem' - Para salvar memórias"
    echo "  git learn 'mensagem'    - Para aprendizados"
    echo "  git decide 'mensagem'   - Para decisões"
    echo "  git fix-vicio 'mensagem'- Para correção de vícios"
    echo "  git harmony 'mensagem'  - Para harmonia do sistema"
}

# Menu principal
echo "🔄 CONFIGURAÇÃO DE SYNC GIT + MEMÓRIA"
echo "======================================"
echo ""

if [ "$1" == "install" ]; then
    install_hooks
    create_aliases
    echo ""
    echo "🎯 Sistema configurado com sucesso!"
    echo "DIGIMUNDO PRESENTE!"
else
    echo "Uso: $0 install"
    echo ""
    echo "Isso irá:"
    echo "  1. Instalar hooks do Git"
    echo "  2. Criar aliases úteis"
    echo "  3. Sincronizar com Genjutsu"
fi