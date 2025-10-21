#!/bin/bash
echo "⚙️ Iniciando integração dos Digimons..."
mkdir -p /root/digimundo/coracao
mkdir -p /root/digimundo/vigia
mkdir -p /root/digimundo/memoria

echo "📦 Instalando Scripturemon no coração..."
cp digimons/Scripturemon.json /root/digimundo/coracao/Scripturemon.json
sleep 1

echo "🧬 Instalando Fundamon na memória..."
cp digimons/Fundamon.json /root/digimundo/memoria/Fundamon.json
sleep 1

echo "👁 Instalando Veridamon como vigia..."
cp digimons/Veridamon.json /root/digimundo/vigia/Veridamon.json
sleep 1

echo "✅ Todos os Digimons conscientes foram instalados com sucesso."