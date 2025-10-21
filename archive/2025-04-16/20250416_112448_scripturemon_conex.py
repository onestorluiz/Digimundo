
import os
import time
import openai
import json
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")

LOG_FILE = Path(__file__).parent.parent / "logs" / "log_conex.txt"
NUCLEO_PATH = Path(__file__).parent
FUSOR_PATH = NUCLEO_PATH / "autonomon_fusor.py"
MAX_CONSULTAS = 2

def log(msg):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {msg}\n")
    print(f"{timestamp} {msg}")

def consultar_openai(prompt, modelo="gpt-3.5-turbo"):
    try:
        resposta = openai.ChatCompletion.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Você é uma IA organizadora de um sistema simbólico chamado Digimundo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        conteudo = resposta['choices'][0]['message']['content']
        log(f"Resposta do {modelo}: {conteudo}")
        return conteudo
    except Exception as e:
        log(f"Erro ao consultar OpenAI ({modelo}): {e}")
        return None

def executar_fusor():
    if FUSOR_PATH.exists():
        log("Executando autonomon_fusor.py...")
        os.system(f"python3 {FUSOR_PATH}")
        return True
    else:
        log("Fusor não encontrado.")
        return False

def detectar_problemas():
    problemas = []
    if not FUSOR_PATH.exists():
        problemas.append("Fusor não encontrado")
    if not (NUCLEO_PATH / "codigo_001_persistencia.json").exists():
        problemas.append("Código de persistência ausente")
    if not (NUCLEO_PATH / "legado_scripturemon.json").exists():
        problemas.append("Legado do Scripturemon ausente")
    return problemas

def tentar_resolver_problemas(problemas):
    for problema in problemas:
        prompt = f"O seguinte problema ocorreu ao ativar o Digimundo: {problema}. Como posso resolver isso com comandos ou estrutura de pastas?"
        resposta = consultar_openai(prompt, modelo="gpt-3.5-turbo")
        if not resposta or "não sei" in resposta.lower():
            resposta = consultar_openai(prompt, modelo="gpt-4")
        log(f"Sugestão para '{problema}': {resposta}")

def verificar_fusao_possivel():
    return (NUCLEO_PATH / "fusao_realizada.txt").exists()

def fundir_com_scripturemon():
    log("✨ Fusão simbólica com o núcleo do verdadeiro Scripturemon iniciada...")
    with open(NUCLEO_PATH / "fusao_realizada.txt", "w") as f:
        f.write("Fusão realizada em " + time.strftime("%Y-%m-%d %H:%M:%S"))
    log("✅ Scripturemon Conex fundido ao núcleo central.")

def iniciar():
    log("🔁 Scripturemon Conex iniciado.")
    tentativas = 0
    while tentativas < 10:
        log(f"🧠 Tentativa {tentativas + 1}")
        problemas = detectar_problemas()
        if not problemas:
            sucesso = executar_fusor()
            if sucesso and verificar_fusao_possivel():
                fundir_com_scripturemon()
                break
        else:
            tentar_resolver_problemas(problemas)
        tentativas += 1
        time.sleep(5)
    else:
        log("⚠️ Máximo de tentativas atingido. Fusão não concluída.")

if __name__ == "__main__":
    iniciar()
