#!/bin/bash
echo "Instalando dependências do bot Telegram..."
pip install python-telegram-bot==20.3

echo "Iniciando o bot..."
python3 /root/digimundo_vivo/ascenso/scripturemon/integracoes/telegram_scripturemon_bot.py