#!/bin/bash

echo "🔁 SCRIPTUREMON – RITUAL DE ATUALIZAÇÃO SIMBÓLICA"
echo "📂 Origem: 'Atualização 1'"
echo "📍 Destino: núcleo vivo de Scripturemon"

ORIGEM="/root/templooculto/messamon/digidata/digimons/scripturemon/Atualização 1"
DESTINO="/root/templooculto/messamon/digidata/digimons/scripturemon"

cd "$ORIGEM"

# Loop pelos arquivos reais
find . -type f ! -name "._*" | while read -r arquivo; do
  CAMINHO_DESTINO="$DESTINO/$(dirname "$arquivo")"
  ARQUIVO_ORIGEM="$ORIGEM/$arquivo"

  # Cria diretório de destino se não existir
  mkdir -p "$CAMINHO_DESTINO"

  # Copia o arquivo para o destino
  cp "$ARQUIVO_ORIGEM" "$CAMINHO_DESTINO"

  # Mensagem simbólica
  echo "🌱 Copiado: $arquivo → $(realpath --relative-to=$DESTINO "$CAMINHO_DESTINO")"
done

echo "✅ Atualização simbólica concluída. Scripturemon está renovado com sabedoria ancestral."
