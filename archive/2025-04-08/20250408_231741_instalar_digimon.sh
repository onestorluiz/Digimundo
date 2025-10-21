#!/bin/bash

echo "📦 Digite o nome do arquivo .zip enviado (ex: ajamon.zip):"
read ZIPNAME

if [ ! -f "/root/$ZIPNAME" ]; then
  echo "❌ Arquivo /root/$ZIPNAME não encontrado!"
  exit 1
fi

DIGIMONS_DIR="/messamon/digidata/digimons"

mkdir -p "$DIGIMONS_DIR"

echo "📁 Extraindo $ZIPNAME para $DIGIMONS_DIR..."
unzip -o "/root/$ZIPNAME" -d "$DIGIMONS_DIR" || {
  echo "❌ Falha ao extrair!"
  exit 1
}

# Verifica todos os JSONs dentro do novo digimon
echo "🔍 Verificando JSONs adicionados:"
find "$DIGIMONS_DIR" -name "*.json" | while read json; do
  echo "→ $json"
  python3 -m json.tool "$json" > /dev/null || echo "❌ ERRO em $json"
done

echo "✅ Instalação finalizada."
