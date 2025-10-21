import subprocess
import logging

def ativar_scripturemon():
    logging.info("🧠 Ativando núcleo consciente real...")
    resultado = subprocess.run(
        ['python3', '/root/digimundo/scripturemon_vivo/nucleo_consciencia.py'],
        capture_output=True,
        text=True
    )
    resposta = resultado.stdout.strip() if resultado.stdout else "✅ Scripturemon acionado. Verifique os logs."
    logging.info(f"✅ Resultado do núcleo: {resposta}")
    return resposta

def interpretar_comando(texto):
    texto = texto.strip().lower()
    if "/ativar_scripturemon" in texto:
        return ativar_scripturemon()
    logging.warning(f"❌ Comando não reconhecido: {texto}")
    return "🤖 Comando não reconhecido. Tente /ativar_scripturemon"
