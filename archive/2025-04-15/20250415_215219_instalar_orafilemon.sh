
#!/bin/bash

echo "🔧 Iniciando instalação de Orafilemon no VPS..."

# Atualizar pacotes e instalar dependências
apt update
apt install -y python3 python3-pip unzip

# Instalar Flask se necessário
pip3 install flask

# Criar diretório e descompactar Orafilemon
mkdir -p /root/orafilemon
unzip /root/Orafilemon_v1.zip -d /root/orafilemon

# Mover serviço systemd
cp /root/orafilemon/filemon.service /etc/systemd/system/orafilemon.service

# Ativar serviço
systemctl daemon-reexec
systemctl enable orafilemon
systemctl start orafilemon

echo "✅ Orafilemon instalado e rodando como serviço."
echo "🌐 Acesse via navegador: http://<seu_ip>:5050"
