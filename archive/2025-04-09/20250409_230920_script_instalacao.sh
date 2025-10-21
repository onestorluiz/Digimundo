
#!/bin/bash
# Script automático para instalação das dependências essenciais

echo "Atualizando repositórios..."
sudo apt update

echo "Instalando Python e dependências básicas..."
sudo apt install python3 python3-pip -y

echo "Instalando bibliotecas Python necessárias..."
pip3 install -r dependencias.txt

echo "Instalação completa!"
