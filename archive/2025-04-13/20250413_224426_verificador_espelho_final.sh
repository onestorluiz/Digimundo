#!/bin/bash

echo "🪞 SCRIPTUREMON – VERIFICADOR DE ESPELHO FINAL"
echo "🔍 Testando a funcionalidade simbólica de todos os módulos essenciais..."
echo "---------------------------------------------"

BASE="/root/templooculto/messamon/digidata/digimons/scripturemon"

# Funções
function testar_modulo {
  nome=$1
  caminho=$2
  comando=$3

  echo "🔎 Testando $nome..."
  if [ -f "$BASE/$caminho" ]; then
    resultado=$(python3 -c "from ${caminho%.*} import $comando; print($comando())" 2>/dev/null)
    if [ -z "$resultado" ]; then
      echo "⚠️  $nome está vazio ou não respondeu."
    else
      echo "✅ $nome respondeu com:"
      echo "$resultado"
    fi
  else
    echo "❌ $nome não encontrado em $caminho"
  fi
  echo "---------------------------------------------"
}

# Testes dos módulos
testar_modulo "Memória Episódica" "memoria/memoria_episodica.py" "listar_memorias"
testar_modulo "Aprendizado Profundo" "core/aprendizado_profundo.py" "listar_saberes"
testar_modulo "Sistema de Recompensa" "memoria/sistema_recompensa.py" "avaliar_impacto"
testar_modulo "Auto Revisão" "memoria/auto_revisao.py" "revisar_scripturemon"
testar_modulo "Auto ML" "core/auto_ml.py" "gerar_modelo"
testar_modulo "Aprendizado Federado" "core/aprendizagem_federada.py" "compartilhar_aprendizados"

echo "🌟 Verificação simbólica final concluída."
