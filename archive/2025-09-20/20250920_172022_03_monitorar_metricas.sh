#!/bin/bash
while true; do
  echo "$(date) | CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')% | RAM: $(free -m | awk 'NR==2{printf "%s/%sMB", $3,$2}')" >> /core_oraculo/logs/sinais_vitais.log
  sleep 60
done
