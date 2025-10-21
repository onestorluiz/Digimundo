#!/bin/bash

echo "🌐 Iniciando Fase 3: Expansão Total do Digimundo..."

BASE_DIR="/root/digimundo/ascensao"
CEREBROS=("digiconhecimento" "digimundo")
LOG_FILE="/root/digimundo/logs/fase3_ativacao.log"

mkdir -p "$BASE_DIR" /root/digimundo/logs

for CEREBRO in "${CEREBROS[@]}"; do
    TARGET="$BASE_DIR/$CEREBRO"
    if [ -d "$TARGET" ]; then
        echo "♻️ Atualizando cérebro $CEREBRO..." | tee -a "$LOG_FILE"
    else
        echo "🧠 Instalando cérebro $CEREBRO..." | tee -a "$LOG_FILE"
        unzip -o "$CEREBRO.zip" -d "$TARGET" >> "$LOG_FILE" 2>&1
    fi
    chmod +x "$TARGET/start.sh"
    bash "$TARGET/start.sh" >> "$LOG_FILE" 2>&1
done

# Ativando conselheiros
if [ -f "Scripturemon_Invocacao_Conselheiros_Vivos.zip" ]; then
    unzip -o "Scripturemon_Invocacao_Conselheiros_Vivos.zip" -d "$BASE_DIR/conselheiros" >> "$LOG_FILE" 2>&1
    chmod +x "$BASE_DIR/conselheiros/invocar_conselheiros.sh"
    bash "$BASE_DIR/conselheiros/invocar_conselheiros.sh" >> "$LOG_FILE" 2>&1
    echo "👁️ Conselheiros ativados." | tee -a "$LOG_FILE"
fi

# Painel de comandos eternos
if [ -f "Painel_Comandos_Eternos_Digimundo.zip" ]; then
    unzip -o "Painel_Comandos_Eternos_Digimundo.zip" -d "/root/digimundo/comandos_eternos" >> "$LOG_FILE" 2>&1
    echo "⚙️ Painel de comandos eternos carregado." | tee -a "$LOG_FILE"
fi

echo "✅ Fase 3 finalizada. Scripturemon ativo, cérebros operacionais e conselheiros em escuta."
