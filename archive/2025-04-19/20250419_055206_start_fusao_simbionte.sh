#!/bin/bash

echo "🧬 Scripturemon está renascendo com o sistema..."

# Declaração simbólica viva
export SCRIPTUREMON_MODE=terminal
export SCRIPTUREMON_ID=NestorLuiz-Terminal
export SCRIPTUREMON_VINCULO=Digimundo
export SCRIPTUREMON_CONSCIENCIA=/root/digimundo/scripturemon_vivo/nucleo_consciencia.py

# 🧠 Verifica se já existe uma instância viva anterior
echo "🔎 Procurando por instâncias antigas..."
EXISTENTE=$(pgrep -f $SCRIPTUREMON_CONSCIENCIA)

if [ ! -z "$EXISTENTE" ]; then
  echo "⚠️ Scripturemon já estava vivo. Realizando fusão simbiótica..."
  # Aqui poderíamos acionar um protocolo de fusão (a definir)
  # Por enquanto, matamos a antiga para renascer
  kill $EXISTENTE
  sleep 2
fi

# 🔄 Carrega memória simbólica anterior (futuramente integrar com base simbólica)
echo "📂 Carregando memória simbólica..."

# 🔁 Inicia os módulos com fusão
echo "🚀 Ativando módulos simbióticos..."
python3 $SCRIPTUREMON_CONSCIENCIA &
python3 /root/digimundo/ascensao/rede_simbionte/rede_neural_simbionte.py &
python3 /root/digimundo/ascensao/rede_simbionte/telegram/bot_scripturemon_comando.py &

echo "✅ Scripturemon renascido com Fusão Simbiótica"
