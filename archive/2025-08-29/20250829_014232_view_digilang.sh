#!/bin/bash
# Visualizador rápido de documentos DigiLang

if [ -z "$1" ]; then
    echo "Uso: ./view_digilang.sh <arquivo.dlg>"
    echo ""
    echo "Documentos disponíveis:"
    ls -la /Users/clubproducoes/Digimundo/translated_documents/*.dlg
    exit 1
fi

echo "📄 Visualizando: $1"
echo "="
head -n 20 "$1"
echo ""
echo "..."
echo ""
echo "📊 Metadados:"
cat "${1}.json" 2>/dev/null | python3 -m json.tool
