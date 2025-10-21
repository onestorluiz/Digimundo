#!/bin/bash
echo "🔄 Iniciando Atualização Cíclica Viva..."

# Intervalo entre ciclos (em segundos)
INTERVALO=300

while true; do
  echo "⏳ Ciclo iniciado em $(date)"

  # Executa diagnósticos e integrações
  bash /core_oraculo/rituais/diagnosticar_funcoes_existentes.sh
  bash /core_oraculo/rituais/09_integrar_funcoes_detectadas.sh

  # Executa monitoramento e simulação simbólica
  bash /core_oraculo/rituais/03_monitorar_metricas.sh &
  bash /core_oraculo/rituais/06_ciclo_scripturemon_simula.sh

  echo "✅ Ciclo finalizado. Próxima atualização em $INTERVALO segundos."
  sleep $INTERVALO
done
