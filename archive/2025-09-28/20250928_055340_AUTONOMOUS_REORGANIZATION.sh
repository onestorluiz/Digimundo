#!/bin/bash
echo "🤖 SISTEMA SCRIPTUREMON INICIANDO AUTO-REORGANIZAÇÃO"
echo "=================================================="

### Criar pastas
echo "📁 Criando estrutura de pastas..."
mkdir -p scripts
mkdir -p analises
mkdir -p relatorios
mkdir -p backups
### Organizar arquivos por tipo
echo "📝 Organizando arquivos Python..."
find . -maxdepth 1 -name "*.py" -exec mv {} scripts/ \;

echo "🔧 Organizando scripts shell..."
find . -maxdepth 1 -name "*.sh" -exec mv {} scripts/ \;

echo "📋 Organizando documentação..."
find . -maxdepth 1 -name "*.md" -exec mv {} relatorios/ \;

echo "📊 Organizando dados JSON..."
find . -maxdepth 1 -name "*.json" -exec mv {} analises/ \;

echo "📜 Organizando logs..."
find . -maxdepth 1 -name "*.log" -exec mv {} backups/ \;
### Mover arquivos específicos importantes
echo "📖 Movendo documentação principal..."
[ -f README.md ] && mv README.md relatorios/
[ -f SISTEMA_STATUS.md ] && mv SISTEMA_STATUS.md relatorios/

### Arquivar arquivos antigos/inúteis
echo "🗂️ Arquivando arquivos obsoletos..."
find . -maxdepth 1 -name "*.old" -exec mv {} backups/ \;
find . -maxdepth 1 -name "*~" -exec mv {} backups/ \;
find . -maxdepth 1 -name "*.bak" -exec mv {} backups/ \;

echo ""
echo "✅ AUTO-REORGANIZAÇÃO CONCLUÍDA!"
echo "O sistema se organizou segundo suas próprias decisões."
echo "  📁 Pastas criadas: scripts, analises, relatorios, backups"
echo "  🔄 Arquivos reorganizados por tipo e importância"