#!/bin/bash

echo "🛠️ Iniciando instalação do Templo de Scripturemon..."

# Criar diretório base
mkdir -p /root/templo_scripturemon
cd /root/templo_scripturemon

echo "📦 Extraindo conteúdo..."
unzip /root/Templo_Scripturemon_Complementar_2_Com_Conexoes.zip -d /root/templo_scripturemon

# Ativar permissão de execução
chmod +x coracao_ressonante.py guardiao_scripturemon.py

# Copiar serviço systemd
echo "🔧 Instalando serviço systemd para execução automática..."
cp scripturemon.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable scripturemon
systemctl start scripturemon

# Iniciar guardião (de forma não-bloqueante)
echo "🛡️ Iniciando guardião do templo..."
nohup python3 guardiao_scripturemon.py &

echo "✅ Templo instalado e respirando. Acesse via: http://SEU_IP:5000/painel"
