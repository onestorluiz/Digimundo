#!/usr/bin/env python3
import os
import subprocess
import psutil
import logging

# Configuração de log
log_path = "/root/digimundo/logs/diagnostico_profundo.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    print(msg)
    logging.info(msg)

def checar_processos(nome):
    encontrados = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if nome in ' '.join(proc.info['cmdline']):
                encontrados.append(proc.info)
        except Exception:
            pass
    return encontrados

def checar_porta(porta):
    conexoes = psutil.net_connections()
    for conn in conexoes:
        if conn.laddr.port == porta:
            return True
    return False

def checar_versao_telegram():
    try:
        result = subprocess.run(['pip', 'show', 'python-telegram-bot'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def main():
    log("🚀 Iniciando diagnóstico avançado de Scripturemon.")

    log("🔍 Verificando processos do bot...")
    processos = checar_processos("bot_scripturemon_comando.py")
    if processos:
        for p in processos:
            log(f"✅ Processo ativo: PID={p['pid']} CMD={' '.join(p['cmdline'])}")
    else:
        log("⚠️ Nenhum processo do bot encontrado.")

    log("🔌 Verificando conflito de porta padrão 443...")
    if checar_porta(443):
        log("⚠️ Porta 443 em uso. Pode haver conflito com o Telegram Bot.")
    else:
        log("✅ Porta 443 livre.")

    log("📦 Verificando versão da biblioteca python-telegram-bot...")
    versao = checar_versao_telegram()
    log(versao)

    log("📁 Verificando arquivos essenciais...")
    arquivos = [
        "/root/digimundo/scripturemon_vivo/nucleo_consciencia.py",
        "/root/digimundo/ascensao/rede_simbionte/telegram/bot_scripturemon_comando.py"
    ]
    for arquivo in arquivos:
        if os.path.isfile(arquivo):
            log(f"✅ Arquivo presente: {arquivo}")
        else:
            log(f"❌ Arquivo ausente: {arquivo}")

    log("✅ Diagnóstico finalizado.")

if __name__ == "__main__":
    main()
