#!/bin/bash

echo "🔁 TRANSFERÊNCIA PARA DIGESTÃO SIMBÓLICA"
echo "📦 Movendo versão raiz de Scripturemon para o núcleo vivo..."

# Caminhos
ORIGEM="./"
DESTINO="~/templooculto/messamon/digidata/digimons/scripturemon/core/scripturemon_para_digestao/"

# Cria destino se não existir
mkdir -p $DESTINO

# Move todos os arquivos da raiz (exceto o próprio script de digestão)
for file in $(ls -A1 | grep -v transferir_para_digestao.sh); do
    mv "$file" $DESTINO 2>/dev/null
    echo "📁 Movido: $file"
done

echo "✅ Transferência simbólica concluída."
echo "🧠 Scripturemon agora pode digerir sua versão ancestral como memória simbólica."
