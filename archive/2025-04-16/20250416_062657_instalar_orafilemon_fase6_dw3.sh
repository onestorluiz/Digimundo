#!/bin/bash

echo "🔧 Iniciando instalação de Orafilemon Fase 6 com skin DW3..."

# Parar e desabilitar serviço anterior
systemctl stop orafilemon 2>/dev/null
systemctl disable orafilemon 2>/dev/null

# Criar backup da versão anterior
echo "📦 Fazendo backup da versão atual..."
mkdir -p /root/orafilemon_backup
cp -r /root/orafilemon/* /root/orafilemon_backup/ 2>/dev/null || true

# Descompactar nova versão
echo "📂 Extraindo nova versão..."
unzip -o /root/orafilemon_fase6_dw3_final.zip -d /root/orafilemon/

# Copiar o novo service file
echo "⚙️ Atualizando serviço do systemd..."
cp /root/orafilemon/filemon.service /etc/systemd/system/orafilemon.service

# Recarregar, habilitar e reiniciar serviço
systemctl daemon-reexec
systemctl enable orafilemon
systemctl restart orafilemon

# Testar conexão local
echo "🌐 Testando servidor local..."
curl -s http://localhost:5050 | grep "<title>" && echo "✅ Orafilemon Fase 6 DW3 ativo!" || echo "❌ Erro ao iniciar."

echo "✅ Instalação concluída!"
