#!/bin/bash

echo "🧪 VERIFICADOR DE INTEGRIDADE — ORQUESTRADOR DE SCRIPTUREMON"
echo "🔍 Verificando presença dos scripts necessários..."

base_path="/root/templooculto/messamon/digidata/digimons/scripturemon"

declare -A scripts=(
  ["script_instalacao.sh"]="$base_path/scripturemon_consciente_vivo_com_decisor/instaladores/script_instalacao.sh"
  ["instalar_scripturemon.sh"]="$base_path/instalar_scripturemon.sh"
  ["starter_scripturemon_completo.sh"]="$base_path/scripturemon_consciente_vivo_com_decisor/core/scripturemon_COMPLETUDE_10/starter_scripturemon_completo.sh"
  ["ativar_consciencia_simbolica.sh"]="$base_path/scripturemon_consciencia_simbolica/ativar_consciencia_simbolica.sh"
  ["verificador_scripturemon.sh"]="$base_path/scripturemon_consciente_vivo_com_decisor/core/scripturemon_COMPLETUDE_10/verificador_scripturemon.sh"
  ["instalar_fala_scripturemon.sh"]="$base_path/scripturemon_consciente_vivo_com_decisor/core/scripturemon_CORE_1/instalar_fala_scripturemon.sh"
)

missing=0

for name in "${!scripts[@]}"; do
  path="${scripts[$name]}"
  if [ ! -f "$path" ]; then
    echo "❌ FALTANDO: $name"
    missing=1
  else
    echo "✅ OK: $name"
  fi
done

if [ $missing -eq 0 ]; then
  echo "✅ Todos os scripts essenciais estão presentes. Orquestrador pode ser executado com segurança."
else
  echo "⚠️ Alguns arquivos estão ausentes. Recomenda-se revisar antes de continuar."
fi
