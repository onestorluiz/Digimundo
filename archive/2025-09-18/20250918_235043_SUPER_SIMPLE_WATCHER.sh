#!/bin/bash
# 🎯 WATCHER MAIS SIMPLES POSSÍVEL - 5 linhas

while true; do
    sleep 90
    # Se Genjutsu não está rodando, provavelmente compactou
    pgrep -f GENJUTSU > /dev/null || echo "⚠️ Genjutsu morreu - possível compactação!"
done