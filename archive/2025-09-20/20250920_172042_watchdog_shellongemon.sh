#!/bin/bash
echo "🧠 Verificando Shellongemon..."
pgrep -f shellongemon_core.py > /dev/null
if [ $? -ne 0 ]; then
  echo "🚨 Shellongemon não está rodando. Reiniciando..."
  nohup python3 shellongemon_core.py &
else
  echo "✅ Shellongemon está ativo."
fi