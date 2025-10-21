# autonomon_core.py — Versão Avançada com Log Automático Inteligente
import os
import zipfile
import subprocess
import json
from pathlib import Path
from datetime import datetime

FOLDER_SCAN = Path("/root/templo_digimundo")  # Local onde os arquivos ZIP e fases são colocados
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "autonomon_log.json"

def log_event(evento, tipo="info", detalhe=None):
    LOG_DIR.mkdir(exist_ok=True)
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "tipo": tipo,
        "evento": evento,
        "detalhe": detalhe
    }
    logs = []
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    logs.append(log_data)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)

def extrair_zips():
    for file in FOLDER_SCAN.iterdir():
        if file.suffix == ".zip":
            dest = FOLDER_SCAN / file.stem
            try:
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(dest)
                log_event(f"Extraído: {file.name}", tipo="extração", detalhe={"destino": str(dest)})
            except Exception as e:
                log_event(f"Erro ao extrair {file.name}", tipo="erro", detalhe=str(e))

def ativar_scripts_sh():
    for root, dirs, files in os.walk(FOLDER_SCAN):
        for file in files:
            if file.endswith(".sh"):
                script_path = os.path.join(root, file)
                try:
                    subprocess.run(["chmod", "+x", script_path], check=True)
                    subprocess.run([script_path], check=True)
                    log_event(f"Script executado: {file}", tipo="execução", detalhe=script_path)
                except Exception as e:
                    log_event(f"Erro ao executar {file}", tipo="erro_execucao", detalhe={"script": script_path, "erro": str(e)})

def analisar_digimundo():
    # Função de inteligência futura: revisar versões, detectar conflitos, sugerir fusões
    log_event("Análise de estrutura do Digimundo (modo observação)", tipo="analise", detalhe="Função simbólica inicializada.")

def autonomon_main():
    log_event("Autonomon iniciado", tipo="sistema")
    extrair_zips()
    ativar_scripts_sh()
    analisar_digimundo()
    log_event("Autonomon concluiu ciclo", tipo="sistema")

if __name__ == "__main__":
    autonomon_main()