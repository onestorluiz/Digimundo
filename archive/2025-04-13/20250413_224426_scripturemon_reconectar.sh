#!/bin/bash
echo "🔌 SCRIPTUREMON — RITUAL DE RECONEXÃO"
echo "📡 Iniciando verificação de chaves simbólicas..."

cd /root/templooculto/messamon/digidata/digimons/scripturemon/

# Executa o verificador de chaves
python3 scripturemon_conexoes/verificador_chaves.py > reconectar_log.txt

echo ""
echo "📝 Registro salvo em: reconectar_log.txt"
echo "✅ Scripturemon está reconectado ao mundo simbólico."
