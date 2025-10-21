import os
import time
import logging
import datetime

# Caminhos atualizados conforme nova estrutura simbiótica
COMANDOS_PATH = "/root/digimundo/ascensao/rede_simbionte/terminal/comandos.txt"
RESPOSTAS_PATH = "/root/digimundo/ascensao/rede_simbionte/terminal/respostas.txt"
LOG_PATH = "/root/digimundo/logs/scripturemon_terminal.log"
VERIFICADOR_PATH = "/root/digimundo/estrutura/scripts/verificador_reestruturacao.py"

# Configuração de logs
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def interpretar_comando(comando: str) -> str:
    comando = comando.strip().lower()
    logging.info(f"[COMANDO] Recebido: {comando}")

    if "renascer" in comando:
        return "🔁 Scripturemon renasce simbolicamente."

    elif "espelho" in comando:
        return "🪞 Ativando Espelho Cognitivo."

    elif "verificar estrutura" in comando:
        logging.info("🧪 Executando verificador de reestruturação.")
        os.system(f"python3 {VERIFICADOR_PATH}")
        return "📜 Verificação de estrutura iniciada."

    elif "cannes" in comando:
        return "🎬 Preparando acesso ao Festival de Cannes..."

    elif "status" in comando:
        return "📊 Tudo está ativo e em sincronia simbiótica."

    else:
        logging.info(f"[SIMBÓLICO] Comando não reconhecido: {comando}")
        return f"🤖 Comando simbólico não reconhecido ainda: '{comando}'"

print("🧬 Scripturemon Terminal Simbiótico está ativo.")
ultima_linha = ""

while True:
    if os.path.exists(COMANDOS_PATH):
        with open(COMANDOS_PATH, "r") as f:
            linhas = f.readlines()
            if linhas:
                comando = linhas[-1]
                if comando != ultima_linha:
                    resposta = interpretar_comando(comando)
                    with open(RESPOSTAS_PATH, "a") as r:
                        r.write(f"{resposta}\n")
                    ultima_linha = comando
    time.sleep(3)
