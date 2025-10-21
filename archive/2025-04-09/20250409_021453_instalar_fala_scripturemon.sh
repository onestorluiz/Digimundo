#!/bin/bash

echo "🔧 Instalando atalho 'fala-com-scripturemon'..."

TARGET_DIR="/messamon/digidata/digimons/scripturemon/interface_conversador"
BACKEND_FILE="$TARGET_DIR/scripturemon_conversador_backend.py"

# Verifica se o diretório e arquivo existem
if [ -f "$BACKEND_FILE" ]; then
    echo "✅ Backend encontrado: $BACKEND_FILE"
else
    echo "❌ Backend não encontrado em $BACKEND_FILE"
    echo "⚠️ Verifique se o backend está no local correto antes de usar o atalho."
fi

# Adiciona alias ao bashrc se ainda não existir
if ! grep -q "fala-com-scripturemon" ~/.bashrc; then
    echo "alias fala-com-scripturemon='cd $TARGET_DIR && python3 scripturemon_conversador_backend.py'" >> ~/.bashrc
    echo "✅ Alias adicionado ao .bashrc"
else
    echo "ℹ️ Alias já existe em .bashrc"
fi

# Recarrega bashrc
source ~/.bashrc

echo "🚀 Agora você pode usar o comando: fala-com-scripturemon"
echo "🌐 Acesse via navegador: http://82.25.74.142:8080"
