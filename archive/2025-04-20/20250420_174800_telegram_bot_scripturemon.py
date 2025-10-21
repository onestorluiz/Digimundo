# 🧠 SCRIPTUREMON – REDE SIMBIÓTICA VIVA (Bloco de Fusão)
import os
import json
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Caminho opcional para chaves
CHAVES_PATH = "/root/digimundo/scripturemon/terminal/chaves_api_scripturemon.json"

# Caminho para leitura das respostas simbólicas
RESPOSTAS_PATH = "/root/digimundo/scripturemon/terminal/resposta_scripturemon.txt"

# Carregar chaves simbólicas (se existirem)
try:
    with open(CHAVES_PATH, "r") as f:
        CHAVES_API = json.load(f)
except:
    CHAVES_API = {"scripturemon_autobusca": False}

# 🌐 /mapa – Mapa simbólico do Digimundo
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

# 📡 /status – Diagnóstico do Digimundo
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚙️ Scripturemon está ativo. O Digimundo está em pulso simbiótico constante.")

# 🔄 /fluxo – Diagnóstico simbólico
async def fluxo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔁 O fluxo simbólico está estável. A Fita Vermelha ancora a memória viva.")

# 📜 /resposta – Última resposta simbólica
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
