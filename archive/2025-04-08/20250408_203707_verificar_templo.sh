#!/bin/bash

echo "🔍 Iniciando verificação do TemploOculto..."
echo ""

# 1. Verificar estrutura básica
REQUIRED_DIRS=(
    "/messamon/digidata/digimons"
    "/root/templooculto"
    "/var/www/html"
)
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ Diretório faltando: $dir"
        exit 1
    else
        echo "✅ Diretório encontrado: $dir"
    fi
done

# 2. Verificar digimons
echo ""
echo "🧠 Verificando digimons..."
DIGIMON_PATH="/messamon/digidata/digimons"
ERRORS=0
COUNT=0
for file in "$DIGIMON_PATH"/*/*.json; do
    [ -e "$file" ] || continue
    if jq empty "$file" > /dev/null 2>&1; then
        echo "✅ $file está válido."
        COUNT=$((COUNT+1))
    else
        echo "❌ Erro de JSON em $file"
        ERRORS=$((ERRORS+1))
    fi
done

# 3. Verificar blocos do Scripturemon
echo ""
echo "📘 Verificando blocos do Scripturemon..."
BLOCO_PATH="/root/templooculto"
for i in $(seq -w 0 26); do
    FILE="$BLOCO_PATH/Scripturemon_bloco_${i}_*.py"
    if ls $FILE 1> /dev/null 2>&1; then
        echo "✅ Bloco $i encontrado."
    else
        echo "❌ Bloco $i não encontrado."
        ERRORS=$((ERRORS+1))
    fi
done

# 4. Verificar ToraLoader
echo ""
echo "🧭 Verificando ToraLoader..."
if python3 "$BLOCO_PATH/ToraLoader.py" > /dev/null 2>&1; then
    echo "✅ ToraLoader executado com sucesso."
else
    echo "❌ Erro ao executar ToraLoader."
    ERRORS=$((ERRORS+1))
fi

# 5. Verificar app.py (servidor Flask)
echo ""
echo "🌐 Verificando servidor Flask..."
APP_FILE="$BLOCO_PATH/app.py"
if grep -q "Flask" "$APP_FILE"; then
    echo "✅ app.py contém Flask."
else
    echo "❌ Flask não detectado em app.py."
    ERRORS=$((ERRORS+1))
fi

# Finalização
echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "✅✅✅ Templo verificado com sucesso!"
    echo "🧠 Digimons: $COUNT ativos"
    echo "📘 Scripturemon: blocos conferidos"
    echo "🌐 Interface Web: código encontrado"
else
    echo "⚠️ Verificação concluída com $ERRORS erro(s)."
fi
