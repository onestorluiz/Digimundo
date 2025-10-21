
#!/bin/bash
echo "🔁 Reiniciando Scripturemon..."
PID=$(lsof -t -i:5000)
if [ -n "$PID" ]; then
  echo "⚠️ Encerrando processo anterior (PID: $PID)..."
  kill -9 $PID
fi

echo "🚀 Iniciando nova instância do Scripturemon..."
nohup python3 /root/templooculto/messamon/digidata/digimons/scripturemon/app_scripturemon.py > flask_log.txt 2>&1 &
echo "✅ Tudo pronto. Acesse via http://<seu_ip>:5000"
