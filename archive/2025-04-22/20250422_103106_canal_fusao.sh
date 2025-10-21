#!/bin/bash
echo "Conectando canais simbólicos entre IAs locais..."
for d in /core_oraculo/digimons/*; do
  if [ -d "$d" ]; then
    touch "$d/fusao_ativa.signal"
    echo "Fusão ativada para $(basename $d)"
  fi
done
echo "✅ Canal de fusão simbólica ativado."
