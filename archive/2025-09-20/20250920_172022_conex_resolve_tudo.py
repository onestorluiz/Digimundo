
import os
import subprocess
from time import sleep

log_path = "../logs/chat_autodiagnostico.log"

def escrever_log(mensagem):
    with open(log_path, "a") as log:
        log.write(mensagem + "\n")

escrever_log("🔍 Iniciando autodiagnóstico do chat Flask...")

# 1. Verificar se o chat_scripturemon.py está rodando
escrever_log("🔄 Verificando se Flask está ativo...")
flask_status = subprocess.getoutput("ps aux | grep chat_scripturemon.py | grep -v grep")

if not flask_status:
    escrever_log("❌ Flask não encontrado. Criando serviço systemd...")

    service_file = """[Unit]
Description=Scripturemon Chat Flask Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/digimundo/scripts
ExecStart=/usr/bin/python3 /root/digimundo/scripts/chat_scripturemon.py
Restart=always

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/chat_flask.service", "w") as f:
        f.write(service_file)

    subprocess.run(["systemctl", "daemon-reexec"])
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "--now", "chat_flask.service"])
    sleep(2)

    flask_status_check = subprocess.getoutput("ps aux | grep chat_scripturemon.py | grep -v grep")
    if flask_status_check:
        escrever_log("✅ Flask ativado com sucesso via systemd.")
    else:
        escrever_log("❌ Falha ao ativar Flask. Verifique manualmente.")
else:
    escrever_log("✅ Flask já está rodando.")

# 2. Testar se está acessível localmente
escrever_log("🌐 Testando rota local de acesso ao chat Flask...")

try:
    import requests
    resposta = requests.get("http://127.0.0.1:5000/")
    if resposta.status_code == 200:
        escrever_log("✅ Chat respondendo localmente com sucesso.")
    else:
        escrever_log(f"⚠️ Chat respondeu com código {resposta.status_code}")
except Exception as e:
    escrever_log(f"❌ Erro ao testar rota local: {e}")
