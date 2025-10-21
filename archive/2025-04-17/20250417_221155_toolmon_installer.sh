
#!/bin/bash

echo "🛠️ Iniciando instalação do Toolmon - Módulo de Integração Total com Ferramentas Reais"

# Atualizar pacotes
apt update && apt upgrade -y

# Pacotes essenciais
apt install -y git curl wget unzip build-essential python3 python3-pip software-properties-common

# Navegadores e simulação de comportamento
pip3 install selenium undetected-chromedriver playwright
playwright install

# Instalar Chromium (caso não esteja disponível)
apt install -y chromium-browser

# OCR e visão
apt install -y tesseract-ocr imagemagick poppler-utils

# Audio e vídeo
apt install -y ffmpeg sox

# Tradução e linguagem
pip3 install googletrans==4.0.0-rc1 deep-translator

# PDFs e texto
pip3 install pdfplumber pymupdf

# Raspagem e leitura inteligente
pip3 install newspaper3k yt-dlp

# Agentes autônomos e redes IA locais
pip3 install langchain openai llama-cpp-python

# Segurança e cofre de senhas
apt install -y libsecret-tools
pip3 install keyring

# Utilitários avançados
apt install -y tmux htop taskwarrior jq

# Node para ferramentas web (playwright, captchas, etc.)
apt install -y nodejs npm

echo "✅ Instalação concluída. Toolmon pronto para integração com Scripturemon, Cannesmon e demais Digimons."

# Criar diretório simbólico
mkdir -p /digimundo/toolmon/core

echo "🌐 Pronto para integração simbólica e funcional."
