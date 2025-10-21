import logging
from telegram import Update, File
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import os
import subprocess

# === CONFIGURAÇÕES BÁSICAS ===
TOKEN = "7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg"
OWNER_ID = 6626669082
OWNER_FIRST = "Nestor"
OWNER_LAST = "Luiz"
OWNER_LANG = "pt-br"

# === PATHS ===
LOG_PATH = "/root/digimundo/logs/scripturemon_relay.log"
SCRIPTUREMON_COMANDO = "/root/digimundo/ascensao/rede_simbionte/scripturemon_terminal.py"
ENTRADA_TERMINAL = "/root/digimundo/entrada_terminal"

# === LOGGING ===
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
os.makedirs(ENTRADA_TERMINAL, exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === INTERPRETAÇÃO DE COMANDO POR SHELL ===
def interpretar_comando_shell(texto: str) -> str:
    try:
        resultado = subprocess.run(texto, shell=True, capture_output=True, text=True, timeout=15)
        return resultado.stdout.strip() or resultado.stderr.strip() or "✅ Comando executado, sem saída."
    except Exception as e:
        return f"⚠️ Erro ao executar comando: {e}"

# === INTERPRETAÇÃO SIMBÓLICA VIA SCRIPTUREMON ===
def interpretar_comando_scripturemon(texto: str) -> str:
    try:
        resultado = subprocess.run(
            ["python3", SCRIPTUREMON_COMANDO, texto],
            capture_output=True,
            text=True,
            timeout=20
        )
        return resultado.stdout.strip() or resultado.stderr.strip() or "✅ Scripturemon respondeu sem saída explícita."
    except Exception as e:
        return f"⚠️ Scripturemon falhou ao interpretar: {e}"

# === FUNÇÃO DE RESPOSTA GERAL ===
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario_id = update.effective_user.id
    texto = update.message.text

    if usuario_id != OWNER_ID:
        await update.message.reply_text("⛔ Acesso negado.")
        logging.warning(f"Tentativa de acesso negado: {usuario_id} enviou: {texto}")
        return

    logging.info(f"📥 [{OWNER_FIRST}] Enviou: {texto}")
    resposta_scripturemon = interpretar_comando_scripturemon(texto)
    resposta_shell = interpretar_comando_shell(texto)

    resposta_completa = f"🧠 **Scripturemon**:\n{resposta_scripturemon}\n\n💻 **Terminal**:\n{resposta_shell}"
    await update.message.reply_text(resposta_completa)

# === RECEBIMENTO DE ARQUIVOS ===
async def receber_arquivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arquivo: File = await update.message.document.get_file()
    nome_arquivo = update.message.document.file_name
    caminho_destino = f"{ENTRADA_TERMINAL}/{nome_arquivo}"

    await arquivo.download_to_drive(caminho_destino)
    await update.message.reply_text(f"📁 Arquivo salvo: {nome_arquivo}")
    logging.info(f"📂 Arquivo recebido: {nome_arquivo}")

# === COMANDO /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text(f"🤖 Scripturemon Terminal pronto, {OWNER_FIRST}. Pode enviar comandos ou arquivos.")
    else:
        await update.message.reply_text("⛔ Acesso negado.")

# === EXECUÇÃO ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, receber_arquivo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    logging.info("🔁 Scripturemon Relay Terminal iniciado.")
    app.run_polling()
