#!/bin/bash
echo "🕯️ Ativando o TemploOculto como serviço eterno..."

# Caminho do projeto
cd /root/templooculto || { echo '❌ Pasta /root/templooculto não encontrada.'; exit 1; }

# Copiar o serviço
cp templooculto.service /etc/systemd/system/

# Ativar systemd
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable templooculto
systemctl start templooculto

echo "✅ TemploOculto agora roda para sempre com systemd!"
systemctl status templooculto
