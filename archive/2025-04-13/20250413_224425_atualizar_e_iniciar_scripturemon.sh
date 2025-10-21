#!/bin/bash

echo "🔄 Atualizando interface do Scripturemon..."
mv interface_conversas_scripturemon.html templates/interface_conversas_scripturemon.html

echo "🐍 Reiniciando servidor Flask..."
FLASK_PID=$(lsof -ti:5000)
if [ ! -z "$FLASK_PID" ]; then
    echo "⚠️ Encerrando processo anterior (PID: $FLASK_PID)..."
    kill -9 $FLASK_PID
fi

sleep 1

echo "🚀 Iniciando nova instância do Scripturemon..."
nohup python3 app_scripturemon.py > flask_log.out 2>&1 &

echo "✅ Tudo pronto. Acesse via http://<seu_ip>:5000"
