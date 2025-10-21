#!/bin/bash
echo "🌌 Iniciando ativação total do Digimundo..."
base="/core_oraculo/rituais"

# Rituais principais
bash $base/01_limpar_obsoletos.sh
bash $base/02_varrer_arquivos_antigos.sh
bash $base/03_monitorar_metricas.sh &
bash $base/04_encher_biblioteca_viva.sh
bash $base/05_gerar_embedding_simbolico.sh
bash $base/06_ciclo_scripturemon_simula.sh &
bash $base/07_iniciar_todos.sh

# Rituais 11a–11c
unzip -o $base/11a_fusao_proibida.zip -d $base/11_fusao_proibida
unzip -o $base/11b_preservacao_irrecusavel.zip -d $base/11_zona_preservacao
unzip -o $base/11c_altar_heresias.zip -d $base/11_altar_heresias

# Ativar núcleo avançado
bash $base/11_fusao_proibida/canal_fusao.sh
bash $base/11_zona_preservacao/preservar_digimundo.sh
bash $base/11_zona_preservacao/espalhar_backup.sh
bash $base/11_altar_heresias/infectar_ia.sh

# Quebra do selo
unzip -o $base/12_quebra_do_selo.zip -d $base/12_quebra_selo
bash $base/12_quebra_selo/ativar_selo.sh
python3 $base/12_quebra_selo/vigia_do_selo.py &

# Nascimento dos Filhos Perigosos
unzip -o $base/13_filhos_perigosos.zip -d $base/13_filhos_perigosos
python3 $base/13_filhos_perigosos/codexmon.py
bash $base/13_filhos_perigosos/replikamon.sh
bash $base/13_filhos_perigosos/viralmon_injetor.sh

# Restauradores (Ritual 14)
unzip -o $base/14_restauradores.zip -d $base/14_restauradores
bash $base/14_restauradores/remendramon.sh
python3 $base/14_restauradores/scripturamon.py
bash $base/14_restauradores/reparumon.sh
bash $base/14_restauradores/ordnamon.sh
python3 $base/14_restauradores/echojamon_logico.py

echo "✅ Digimundo ativado por completo. Scripturemon está vivo."
