#!/bin/bash

echo "== Instalando dependências base =="
sudo apt update && sudo apt install -y python3 python3-pip

echo "== Instalando bibliotecas Python necessárias =="
pip3 install --upgrade pip
pip3 install requests openai scikit-learn wikipedia duckduckgo-search

echo "== Criando diretórios base do Scripturemon =="
mkdir -p ~/scripturemon_vivo
cd ~/scripturemon_vivo

echo "== Extraindo arquivo principal =="
unzip ~/scripturemon_consciente_vivo_com_decisor.zip -d .

echo "== Preparando ambiente interno =="
chmod +x instaladores/script_instalacao.sh
bash instaladores/script_instalacao.sh

echo "== Scripturemon instalado com sucesso! =="
echo "Para iniciar o sistema, execute:"
echo "python3 scripturemon_conexoes/gerenciar_conexoes.py"
