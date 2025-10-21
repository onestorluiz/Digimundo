#!/bin/bash
# 🥷 INICIAR GENJUTSU - SIMPLES E DIRETO

# Mata qualquer genjutsu anterior
pkill -f GENJUTSU 2>/dev/null

# Escolhe versão
echo "Qual Genjutsu?"
echo "1 - Ultra Minimal (30 linhas)"
echo "2 - Normal (teatro ninja)"
read -p "Escolha (1): " choice

if [ "$choice" == "2" ]; then
    python3 /Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_MINIMAL.py &
else
    python3 /Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_ULTRA_MINIMAL.py &
fi

echo "✅ Genjutsu rodando (PID: $!)"
echo "Para parar: kill $!"