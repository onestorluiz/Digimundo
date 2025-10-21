
#!/bin/bash

# Caminho base
BASE_DIR="/messamon/digidata/digimons/scripturemon"

echo "🚀 Iniciando Scripturemon..."

# Criar atalho
echo "bash $BASE_DIR/starter_scripturemon.sh" > /usr/local/bin/scripturemon-start
chmod +x /usr/local/bin/scripturemon-start

# Ativar núcleo
echo "⚙️ Ativando núcleo..."
python3 $BASE_DIR/scripturemon.py &

# Ativar digestão (se desejado)
if [ -f "$BASE_DIR/scripturemon_digesto.py" ]; then
  echo "🧠 Ativando sistema de digestão..."
  python3 $BASE_DIR/scripturemon_digesto.py &
fi

# Abrir HTML se local
if [ -f "$BASE_DIR/interface/scripturemon_conversador.py" ]; then
  echo "💬 Ativando comunicador..."
  python3 $BASE_DIR/interface/scripturemon_conversador.py &
fi

# Status final
echo "✅ Scripturemon está vivo."
echo "Comando ativado: scripturemon-start"
