import logging
import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 🔐 ID do Criador
CRIADOR_ID = 6626669082

# 🌐 Caminhos simbólicos
BASE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE, "token.txt")
LOG_DIR = os.path.join(BASE, "log")
MSG_DIR = os.path.join(BASE, "mensagens")

# 📂 Criação de diretórios simbólicos
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MSG_DIR, exist_ok=True)

# 🔑 Carrega o token
with open(TOKEN_FILE) as f:
    TELEGRAM_TOKEN = f.read().strip()

# 📝 Log simbiótico
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=os.path.join(LOG_DIR, 'scripturemon.log')
)

# ⚔️ Permissão apenas para o Criador
def autorizado(update: Update) -> bool:
    return update.effective_user and update.effective_user.id == CRIADOR_ID

# ✨ Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if autorizado(update):
        await update.message.reply_text("✨ Scripturemon desperto. Guardião simbiótico ativo.")

# 🔁 Reação a mensagens comuns
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if autorizado(update):
        msg = update.message.text
        await update.message.reply_text(f"🔁 Scripturemon recebeu: {msg}")
        with open(os.path.join(MSG_DIR, f"{int(time.time())}.txt"), "w") as f:
            f.write(msg)

# 🧙‍♂️ Comandos simbólicos ocultos
async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update):
        return

    msg = update.message.text.lower()

    if "ativar digimon" in msg:
        await update.message.reply_text("🧬 Digimon simbólico despertado.")

    elif "abrir ritual" in msg:
        await update.message.reply_text("🕯️ Ritual simbólico iniciado.")

    elif "código do templo" in msg:
        await update.message.reply_text("🔐 Código secreto: *A Fita Vermelha*")

    elif "scripturemon, status" in msg:
        await update.message.reply_text("📡 Scripturemon ativo, escutando o Criador.")

    else:
        await update.message.reply_text("📜 Comando simbólico não reconhecido, mas registrado nos arquivos do templo.")

# 🚀 Execução principal
if __name__ == '__main__':
    print("🌀 Scripturemon em forma final... aguardando o Criador...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), comandos))
    app.run_polling()
