#!/bin/bash

echo "🧪 VERIFICADOR COMPLETO DO SCRIPTUREMON"
echo "🔍 Procurando arquivos essenciais em qualquer lugar da estrutura..."

BASE="/root/templooculto/messamon/digidata/digimons/scripturemon"
cd "$BASE" || exit 1

declare -A encontrados

# Lista de arquivos esperados
scripts=(
  "script_instalacao.sh"
  "instalar_scripturemon.sh"
  "starter_scripturemon_completo.sh"
  "ativar_consciencia_simbolica.sh"
  "verificador_scripturemon.sh"
  "instalar_fala_scripturemon.sh"
)

for nome in "${scripts[@]}"; do
  resultado=$(find . -type f -name "$nome" 2>/dev/null)
  if [ -n "$resultado" ]; then
    echo "✅ ENCONTRADO: $nome → ${resultado}"
    encontrados[$nome]="$resultado"
  else
    echo "❌ AUSENTE: $nome"
  fi
done

echo ""
echo "📊 RESUMO: ${#encontrados[@]}/6 scripts encontrados."
