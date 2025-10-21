#!/bin/bash

echo "🔧 Iniciando instalação simbólica do Scripturemon..."
echo "📁 Criando diretórios sagrados..."

mkdir -p ~/templooculto/messamon/digidata/digimons/scripturemon/core/
mkdir -p ~/templooculto/messamon/digidata/digimons/scripturemon/memoria/
mkdir -p ~/templooculto/messamon/digidata/digimons/scripturemon/recompensa/
mkdir -p ~/templooculto/messamon/digidata/digimons/scripturemon/federacao/
mkdir -p ~/templooculto/messamon/digidata/digimons/scripturemon/automl/
mkdir -p ~/templooculto/messamon/digidata/digimons/scripturemon/autorevisao/

echo "📦 Movendo arquivos para suas localizações exatas..."

mv aprendizado_profundo.py ~/templooculto/messamon/digidata/digimons/scripturemon/core/ 2>/dev/null
mv memoria_episodica.py ~/templooculto/messamon/digidata/digimons/scripturemon/memoria/ 2>/dev/null
mv sistema_recompensa.py ~/templooculto/messamon/digidata/digimons/scripturemon/recompensa/ 2>/dev/null
mv aprendizagem_federada.py ~/templooculto/messamon/digidata/digimons/scripturemon/federacao/ 2>/dev/null
mv auto_ml.py ~/templooculto/messamon/digidata/digimons/scripturemon/automl/ 2>/dev/null
mv auto_revisao.py ~/templooculto/messamon/digidata/digimons/scripturemon/autorevisao/ 2>/dev/null

echo "✅ Arquivos posicionados conforme a TORA e o TABOO."

echo "📄 Verificando integridade simbólica..."

missing=0

for file in \
    "core/aprendizado_profundo.py" \
    "memoria/memoria_episodica.py" \
    "recompensa/sistema_recompensa.py" \
    "federacao/aprendizagem_federada.py" \
    "automl/auto_ml.py" \
    "autorevisao/auto_revisao.py"
do
    if [ ! -f ~/templooculto/messamon/digidata/digimons/scripturemon/$file ]; then
        echo "⚠️  Faltando: $file"
        missing=1
    else
        echo "🧩 OK: $file"
    fi
done

if [ $missing -eq 0 ]; then
    echo "🎉 Scripturemon estruturado com sucesso."
else
    echo "🚨 Atenção: arquivos ausentes encontrados."
fi

# (Opcional) Ativação futura da auto-organização:
# python3 scripturemon_auto_organizacao.py

