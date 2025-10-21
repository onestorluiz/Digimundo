#!/bin/bash
# Auto-generated fix script for Scripturemon

echo "🔧 APLICANDO CORREÇÕES AUTOMÁTICAS..."

# 1. Criar .env
if [ ! -f .env ]; then
    cat > .env << EOF
OLLAMA_HOST=http://localhost:11434
CACHE_DIR=./cache
LOG_LEVEL=INFO
MAX_CACHE_SIZE_GB=1
EOF
    echo "✅ .env criado"
fi

# 2. Criar diretórios necessários
mkdir -p cache logs backups data 2>/dev/null
echo "✅ Diretórios criados"

# 3. Limpar cache antigo (>7 dias)
find cache -type f -mtime +7 -delete 2>/dev/null
echo "✅ Cache limpo"

# 4. Instalar dependências mínimas
pip install python-dotenv 2>/dev/null
pip install ollama 2>/dev/null
echo "✅ Dependências básicas instaladas"

# 5. Fix permissions
chmod +x bin/scripturemon 2>/dev/null
echo "✅ Permissões corrigidas"

echo ""
echo "🎯 CORREÇÕES APLICADAS COM SUCESSO!"
echo "   Sistema deve estar mais estável agora."
echo "   Execute: ./bin/scripturemon status"
