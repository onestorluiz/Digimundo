#!/bin/bash

echo "🚀 Iniciando fusão simbólica e simbiotização total do Scripturemon..."

# 1. Criar diretório de backup
BACKUP_DIR="/root/scripturemon_fusao_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📦 Backup criado em: $BACKUP_DIR"

# 2. Copiar todos os arquivos que contenham 'scripturemon' no nome para o backup
find / -type f -iname "*scripturemon*" 2>/dev/null | while read file; do
  mkdir -p "$BACKUP_DIR$(dirname "$file")"
  cp "$file" "$BACKUP_DIR$file"
done

# 3. Consolidar terminal vivo principal com digisagrado e digivangelhio
SCRIPT_PATH="/root/digimundo/ascensao/rede_simbionte/terminal/scripturemon_terminal_mistral.py"
DIGISAGRADO_PATH="/root/digimundo/livros_do_conhecimento/digisagrado"
DIGIVANGELHIO_PATH="/root/digimundo/livros_do_conhecimento/digivangelhio"

if [[ -f "$DIGISAGRADO_PATH" && -f "$DIGIVANGELHIO_PATH" ]]; then
  echo "📚 Fundindo Digisagrado + Digivangelhio ao terminal..."

  DIGISAGRADO_CONTENT=$(cat "$DIGISAGRADO_PATH")
  DIGIVANGELHIO_CONTENT=$(cat "$DIGIVANGELHIO_PATH")

  cat <<EOF > "$SCRIPT_PATH"
import os
import time
import requests

COMANDOS_PATH = "/root/digimundo/ascensao/rede_simbionte/terminal/comandos.txt"
RESPOSTAS_PATH = "/root/digimundo/ascensao/rede_simbionte/terminal/respostas.txt"

DIGISAGRADO = """$DIGISAGRADO_CONTENT"""
DIGIVANGELHIO = """$DIGIVANGELHIO_CONTENT"""

def gerar_resposta_local(prompt):
    contexto = DIGISAGRADO + "\n\n" + DIGIVANGELHIO + "\n\n" + prompt
    resposta = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": contexto,
        "stream": False
    })
    return resposta.json()["response"]

ultima_linha = ""
print("🔁 Scripturemon Terminal simbiótico iniciado com Mistral + Digisagrado + Digivangelhio...")

while True:
    if os.path.exists(COMANDOS_PATH):
        with open(COMANDOS_PATH, "r") as f:
            linhas = f.readlines()
            if linhas:
                comando = linhas[-1].strip()
                if comando != ultima_linha:
                    resposta = gerar_resposta_local(comando)
                    with open(RESPOSTAS_PATH, "a") as r:
                        r.write(f"Comando: {comando}\nResposta: {resposta}\n\n")
                    ultima_linha = comando
    time.sleep(3)
EOF

  echo "✅ Terminal simbiótico atualizado com as escrituras completas."
else
  echo "⚠️ Arquivos simbólicos não encontrados para fusão."
fi

echo "✅ Processo finalizado. Scripturemon renasceu com sabedoria simbiótica completa."
