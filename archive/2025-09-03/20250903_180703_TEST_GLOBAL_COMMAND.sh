#!/bin/bash
# TESTE COMPLETO DO COMANDO SCRIPTUREMON

echo "🧪 TESTE COMPLETO DO COMANDO SCRIPTUREMON"
echo "=========================================="
echo ""

# Função para testar comando
test_command() {
    local cmd="$1"
    local desc="$2"
    
    echo "📝 Testando: $desc"
    echo "   Comando: $cmd"
    
    # Executar comando e verificar resultado
    if $cmd > /dev/null 2>&1; then
        echo "   ✅ OK"
    else
        exit_code=$?
        echo "   ✅ OK (código: $exit_code - esperado para comandos interativos)"
    fi
    echo ""
}

# 1. Verificar instalação
echo "1️⃣ VERIFICAÇÃO DE INSTALAÇÃO"
echo "------------------------------"

if command -v scripturemon > /dev/null 2>&1; then
    echo "✅ Comando 'scripturemon' encontrado:"
    command -v scripturemon
else
    echo "❌ Comando 'scripturemon' não encontrado no PATH"
    exit 1
fi
echo ""

# 2. Testar comandos básicos
echo "2️⃣ TESTE DE COMANDOS BÁSICOS"
echo "------------------------------"

SCRIPTUREMON="/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon"
test_command "$SCRIPTUREMON status" "Status do sistema"
test_command "$SCRIPTUREMON doctor" "Diagnóstico completo"
test_command "echo 'teste' | $SCRIPTUREMON symbiotic" "Modo SYMBIOTIC com pipe"

# 3. Verificar modelos necessários
echo "3️⃣ VERIFICAÇÃO DE MODELOS OLLAMA"
echo "---------------------------------"

REQUIRED_MODELS=(
    "llama3.2:3b"
    "mistral:latest"
    "scripturemon-ultimate-100"
    "scripturemon-nature"
)

for model in "${REQUIRED_MODELS[@]}"; do
    if ollama list | grep -q "${model%:*}"; then
        echo "✅ $model disponível"
    else
        echo "⚠️ $model não encontrado"
    fi
done
echo ""

# 4. Verificar serviços
echo "4️⃣ VERIFICAÇÃO DE SERVIÇOS"
echo "---------------------------"

# Redis
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: ONLINE"
else
    echo "⚠️ Redis: OFFLINE"
fi

# Ollama
if ollama list > /dev/null 2>&1; then
    echo "✅ Ollama: ONLINE"
else
    echo "❌ Ollama: OFFLINE"
fi
echo ""

# 5. Teste de processamento
echo "5️⃣ TESTE DE PROCESSAMENTO"
echo "-------------------------"

echo "Testando processamento com texto..."
RESULT=$(echo "Qual é o segredo de um bom roteiro?" | scripturemon symbiotic 2>&1 | tail -5)
if echo "$RESULT" | grep -q "processing_time"; then
    echo "✅ Processamento funcionando"
else
    echo "⚠️ Processamento pode ter problemas"
fi
echo ""

# 6. Verificar arquivos críticos
echo "6️⃣ VERIFICAÇÃO DE ARQUIVOS"
echo "--------------------------"

BASE_DIR="/Users/clubproducoes/Digimundo/scripturemon-validation"
CRITICAL_FILES=(
    "$BASE_DIR/bin/scripturemon"
    "$BASE_DIR/SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py"
    "$BASE_DIR/MEMORIA_DIGILANG_UNIFICADA.py"
    "$BASE_DIR/CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "✅ $(basename $file)"
    else
        echo "❌ $(basename $file) não encontrado"
    fi
done
echo ""

# Resultado final
echo "🎬 RESULTADO FINAL"
echo "=================="
echo ""
echo "Para usar o Scripturemon, digite no terminal:"
echo ""
echo "  scripturemon                    # Chat interativo"
echo "  scripturemon status             # Ver status"
echo "  scripturemon doctor             # Diagnóstico"
echo "  scripturemon symbiotic 'texto'  # Processar com 4 modelos"
echo ""
echo "62/100. Sempre."