#!/bin/bash
echo "🔄 Iniciando rotina simbiótica de manutenção do Digimundo..." >> /var/log/digimundo_manutencao.log

DATA=$(date '+%Y-%m-%d %H:%M:%S')
echo "📅 [$DATA] Verificando atualizações..." >> /var/log/digimundo_manutencao.log

apt update -y && apt upgrade -y >> /var/log/digimundo_manutencao.log 2>&1

echo "📦 Verificando pacotes travados..." >> /var/log/digimundo_manutencao.log
HOLD=$(apt-mark showhold)

if [ -n "$HOLD" ]; then
    echo "⚠️ Pacotes travados detectados: $HOLD" >> /var/log/digimundo_manutencao.log

    # Envia alerta para o Telegram
    curl -s -X POST "https://api.telegram.org/bot7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg/sendMessage" \
    -d chat_id=6626669082 \
    -d text="⚠️ Digimundo: Pacotes travados detectados no VPS! ($HOLD) - verifique com apt-mark showhold"
else
    echo "✅ Nenhum pacote travado encontrado." >> /var/log/digimundo_manutencao.log
fi

echo "✅ Manutenção concluída com sucesso em $DATA" >> /var/log/digimundo_manutencao.log
