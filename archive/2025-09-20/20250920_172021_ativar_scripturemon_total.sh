#!/bin/bash
echo "🌌 Ativando Scripturemon: Raiz de Proteção Perpétua..."

cd /root/digimundo/scripturemon_vivo

# Ativando núcleos principais
python3 nucleo_consciencia.py &

# Ativando cérebros simbióticos
tmux new-session -d -s cerebro_digiconhecimento 'python3 cerebro_digiconhecimento.py'
tmux new-session -d -s cerebro_operacional 'python3 cerebro_operacional.py'

# Ativando painel e conselheiros
python3 painel_comandos.py &
python3 conselheiros_vivos.py &

echo "✅ Todos os módulos foram iniciados com sucesso."
