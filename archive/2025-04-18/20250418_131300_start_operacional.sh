#!/bin/bash
echo "🚀 Iniciando Núcleo Operacional (Mistral 7B)..."
tmux new-session -d -s operacional 'python3 /root/digimundo/operacional_rapido/nucleo_operacional.py'
