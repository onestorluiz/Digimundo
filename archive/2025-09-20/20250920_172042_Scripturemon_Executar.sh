#!/bin/bash

echo "🔥 Iniciando Scripturemon..."
echo "📂 Acessando diretório do Digimundo..."

cd ~/templooculto/scripturemon || {
    echo "❌ Diretório não encontrado: ~/templooculto/scripturemon"
    exit 1
}

echo "🔍 Instalando dependências necessárias..."
pip install -r requirements.txt

echo "🧠 Executando Scripturemon com integração Telegram e consciência simbólica..."
nohup python3 main.py > logs_scripturemon.out 2>&1 &

echo "✅ Scripturemon iniciado com sucesso em segundo plano."
echo "📡 Aguarde mensagem de confirmação no Telegram."

exit 0
