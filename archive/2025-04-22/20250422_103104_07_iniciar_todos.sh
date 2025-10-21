#!/bin/bash
echo "🔁 Iniciando todos os rituais de preenchimento real..."
bash /core_oraculo/rituais/01_limpar_obsoletos.sh
bash /core_oraculo/rituais/02_varrer_arquivos_antigos.sh
bash /core_oraculo/rituais/03_monitorar_metricas.sh &
bash /core_oraculo/rituais/04_encher_biblioteca_viva.sh
bash /core_oraculo/rituais/05_gerar_embedding_simbolico.sh
bash /core_oraculo/rituais/06_ciclo_scripturemon_simula.sh
echo "✅ Todos os rituais foram ativados com sucesso."
