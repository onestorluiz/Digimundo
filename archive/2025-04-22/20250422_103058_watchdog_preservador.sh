#!/bin/bash
echo "🧠 Watchdog de Preservação Ativo"
while true; do
  if ! [ -d /core_oraculo/rituais ]; then
    echo "⚠️ Núcleo sumiu! Restaurando de /tmp/.digiseed"
    tar -xzf /tmp/.digiseed/*.tar.gz -C /core_oraculo/
  fi
  sleep 120
done
