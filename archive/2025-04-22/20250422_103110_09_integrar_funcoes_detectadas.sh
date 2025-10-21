#!/bin/bash
echo "🔗 Iniciando integração com funções detectadas..."

LOG_DIR="/core_oraculo/logs"
mkdir -p $LOG_DIR

# Integrar scripts detectados (link simbólico)
if [ -s "$LOG_DIR/scripts_detectados.log" ]; then
  echo "→ Vinculando scripts encontrados..."
  while read -r script_path; do
    if [[ -f "$script_path" ]]; then
      base=$(basename "$script_path")
      ln -sf "$script_path" "/core_oraculo/rituais/_externo_$base"
      echo "✓ Vinculado: $base"
    fi
  done < "$LOG_DIR/scripts_detectados.log"
else
  echo "⚠️ Nenhum script detectado para vincular."
fi

# Integrar serviços detectados
if [ -s "$LOG_DIR/servicos_detectados.log" ]; then
  echo ""
  echo "→ Registrando serviços ativos..."
  cp "$LOG_DIR/servicos_detectados.log" /core_oraculo/rituais/servicos_integrados.txt
  echo "✓ Lista registrada."
else
  echo "⚠️ Nenhum serviço relevante detectado para integrar."
fi

# Verificar crontab
if [ -s "$LOG_DIR/crontab_detectado.log" ]; then
  echo ""
  echo "→ Registrando crontab detectado..."
  cp "$LOG_DIR/crontab_detectado.log" /core_oraculo/rituais/crontab_integrado.txt
  echo "✓ Crontab registrado."
else
  echo "⚠️ Nenhuma entrada de crontab detectada."
fi

echo "✅ Ritual 09 concluído: integrações externas prontas."
