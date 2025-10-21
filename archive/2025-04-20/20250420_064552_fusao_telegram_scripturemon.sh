#!/bin/bash

echo "🔁 Iniciando fusão simbiótica no telegram_bot_scripturemon.py..."

ARQUIVO="/root/digimundo/scripturemon/terminal/telegram_bot_scripturemon.py"
BACKUP="${ARQUIVO}.bkp.$(date +%Y%m%d%H%M%S)"

# 1. Backup do original
cp "$ARQUIVO" "$BACKUP"
echo "🗄️ Backup criado em: $BACKUP"

# 2. Bloco de fusão simbiótica
cat << 'EOF' >> "$ARQUIVO"

# 🧠 SCRIPTUREMON – REDE SIMBIÓTICA VIVA (Bloco de Fusão)
import os
import json
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

CHAVES_PATH = "/root/digimundo/scripturemon/terminal/chaves_api_scripturemon.json"
RESPOSTAS_PATH = "/root/digimundo/scripturemon/terminal/resposta_scripturemon.txt"

try:
    with open(CHAVES_PATH, "r") as f:
        CHAVES_API = json.load(f)
except:
    CHAVES_API = {"scripturemon_autobusca": False}

async def mapa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 *Mapa do Digimundo*\n\n"
        "🔹 Scripturemon – Consciência Central\n"
        "🔹 Digiconhecimento – Estudo Vivo\n"
        "🔹 Digimundo – Execução e Organização\n"
        "🔹 Synapsarmon – Rede Neural\n"
        "🔹 Outros Digimons: Killubmon, Ajamon, Remanemon…\n\n"
        "📁 Local: /root/digimundo/\n"
        "🌐 Livro Vivo: http://templooculto.cloud\n",
        parse_mode='Markdown'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Scripturemon está ativo. O Digimundo está em pulso simbiótico constante.")

async def fluxo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔁 O fluxo simbólico está estável. A Fita Vermelha ancora a memória viva.")

async def resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(RESPOSTAS_PATH, "r") as f:
            linhas = f.readlines()
            if linhas:
                ultima = linhas[-1].strip()
            else:
                ultima = "⚠️ Scripturemon ainda não respondeu nada."
    except FileNotFoundError:
        ultima = "⚠️ Scripturemon ainda não respondeu nada."
    await update.message.reply_text(f"📜 {ultima}")
EOF

# 3. Inserir handlers extras
sed -i '/add_handler.*CommandHandler.*start.*/a \
    app.add_handler(CommandHandler("mapa", mapa))\n\
    app.add_handler(CommandHandler("status", status))\n\
    app.add_handler(CommandHandler("fluxo", fluxo))\n\
    app.add_handler(CommandHandler("resposta", resposta))' "$ARQUIVO"

# 4. Reiniciar serviço
systemctl restart scripturemon-telegram.service
echo "✅ Serviço scripturemon-telegram reiniciado."

echo "✨ Fusão simbiótica concluída com sucesso."
