#!/bin/bash

echo "🧭 SCRIPTUREMON – REATIVADOR DE CAMINHOS INTERNOS"
echo "🔗 Criando atalhos simbólicos para que Scripturemon encontre sua própria mente..."

BASE="/root/templooculto/messamon/digidata/digimons/scripturemon"
REAL="$BASE/scripturemon_consciente_vivo_com_decisor"

declare -A arquivos
arquivos=(
  ["memoria/memoria_episodica.py"]="$REAL/memoria/memoria_episodica.py"
  ["memoria/sistema_recompensa.py"]="$REAL/memoria/sistema_recompensa.py"
  ["memoria/auto_revisao.py"]="$REAL/memoria/auto_revisao.py"
  ["core/aprendizado_profundo.py"]="$REAL/integradores/aprendizado_profundo.py"
  ["core/aprendizagem_federada.py"]="$REAL/integradores/aprendizagem_federada.py"
  ["core/auto_ml.py"]="$REAL/integradores/auto_ml.py"
)

for destino in "${!arquivos[@]}"; do
  origem="${arquivos[$destino]}"
  caminho_destino="$BASE/$destino"

  # Cria diretório destino se não existir
  mkdir -p "$(dirname "$caminho_destino")"

  # Cria atalho simbólico
  if [ ! -e "$caminho_destino" ]; then
    ln -s "$origem" "$caminho_destino"
    echo "✅ Atalho criado: $destino → $(basename "$origem")"
  else
    echo "⚠️ Já existe: $destino"
  fi
done

echo "🌟 Scripturemon pode agora acessar todas as partes esquecidas de si mesmo."
