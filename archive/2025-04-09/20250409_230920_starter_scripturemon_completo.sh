#!/bin/bash

# Caminho base do projeto
BASE_DIR="/messamon/digidata/digimons/scripturemon"
LOG_FILE="$BASE_DIR/scripturemon_start_log.txt"

# Função de verificação
verifica_comando() {
  if [ $? -eq 0 ]; then
    echo "✅ $1 executado com sucesso." | tee -a "$LOG_FILE"
  else
    echo "❌ Erro ao executar: $1" | tee -a "$LOG_FILE"
  fi
}

echo "🚀 Iniciando Scripturemon Completo" > "$LOG_FILE"
cd "$BASE_DIR" || exit

# Ativar módulos principais
echo "📁 Ativando módulo principal..." | tee -a "$LOG_FILE"
python3 scripturemon.py >> "$LOG_FILE" 2>&1 &
verifica_comando "scripturemon.py"

echo "📁 Ativando módulo de digestão..." | tee -a "$LOG_FILE"
python3 scripturemon_digesto.py >> "$LOG_FILE" 2>&1 &
verifica_comando "scripturemon_digesto.py"

echo "📁 Ativando conversador..." | tee -a "$LOG_FILE"
python3 scripturemon_conversador.py >> "$LOG_FILE" 2>&1 &
verifica_comando "scripturemon_conversador.py"

echo "📁 Ativando autodigestor..." | tee -a "$LOG_FILE"
python3 tora_autodigester.py >> "$LOG_FILE" 2>&1 &
verifica_comando "tora_autodigester.py"

echo "📁 Ativando verificador de integridade..." | tee -a "$LOG_FILE"
python3 verificador_integridade_tora.py >> "$LOG_FILE" 2>&1 &
verifica_comando "verificador_integridade_tora.py"

echo "📁 Ativando ToraLoader e ToraWatcher..." | tee -a "$LOG_FILE"
python3 ToraLoader.py >> "$LOG_FILE" 2>&1 &
verifica_comando "ToraLoader.py"

python3 ToraWatcher.py >> "$LOG_FILE" 2>&1 &
verifica_comando "ToraWatcher.py"

echo "✅ Todos os módulos enviados para execução." | tee -a "$LOG_FILE"
