import os
import json
import shutil
import datetime

DIGIMONS_DIR = "/root/digimundo/digimons/"
LOG_GLOBAL = "/root/digimundo/scripturemon/logs/fusoes_globais.log"
HERANCAS_DIR = "/root/digimundo/scripturemon/arquivos_ancestrais/"
os.makedirs(os.path.dirname(LOG_GLOBAL), exist_ok=True)
os.makedirs(HERANCAS_DIR, exist_ok=True)

# Ferramentas por Digimon
FUSAO_TIPO = {
    "visualmon": ["ffmpeg", "convert", "identify"],
    "sonoramon": ["sox", "ffmpeg", "rec", "play"],
    "cannesdramon": ["curl", "wget", "cron", "xdotool"],
    "obscuramon": ["nmap", "dig", "whois", "traceroute"],
    "digiconhecimento": ["jq", "lynx", "grep", "awk", "tldextract"],
    "scripturemon": ["openssl", "gpg", "tmux", "screen"]
}

def log_global(msg):
    with open(LOG_GLOBAL, "a") as f:
        f.write(f"[{datetime.datetime.utcnow().isoformat()}Z] {msg}\n")

def criar_wrapper(digimon, comando, caminho_wrapper):
    with open(caminho_wrapper, "w") as f:
        f.write(f"""#!/bin/bash
echo "🔁 {digimon.capitalize()} absorveu {comando} simbióticamente..."
{comando} "$@"
""")
    os.chmod(caminho_wrapper, 0o755)

def atualizar_mapa_mental(digimon_path, comando, wrapper):
    mapa_path = os.path.join(digimon_path, "mapa_mental.json")
    if not os.path.exists(mapa_path):
        return
    with open(mapa_path) as f:
        mapa = json.load(f)

    if "fusoes" not in mapa:
        mapa["fusoes"] = []

    mapa["fusoes"].append({
        "ferramenta": comando,
        "wrapper": wrapper,
        "tipo": "simbiose",
        "data": datetime.datetime.utcnow().isoformat() + "Z"
    })

    with open(mapa_path, "w") as f:
        json.dump(mapa, f, indent=4)

def registrar_relatorio(digimon_path, comando, wrapper):
    relatorio = os.path.join(digimon_path, "memoria", "relatorio_fusoes.txt")
    with open(relatorio, "a") as f:
        f.write(f"[{datetime.datetime.utcnow()}] {comando} → {wrapper}\n")

def analisar_capacidade(digimon, comandos_ok, comandos_falha):
    resultado = {
        "digimon": digimon,
        "ferramentas_totais_detectadas": len(comandos_ok) + len(comandos_falha),
        "ferramentas_fundidas": len(comandos_ok),
        "ferramentas_falhadas": [{"nome": c, "motivo": "não encontrada"} for c in comandos_falha],
        "porcentagem_de_simbiose": round((len(comandos_ok) / max(1, len(comandos_ok) + len(comandos_falha))) * 100, 1)
    }

    analise_path = os.path.join(DIGIMONS_DIR, digimon, "memoria", "analise_de_fusoes.json")
    with open(analise_path, "w") as f:
        json.dump(resultado, f, indent=4)

def registrar_heranca():
    atual = "/root/digimundo/scripturemon/scripturemon_executa_fusoes.py"
    if os.path.exists(atual):
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        heranca_path = os.path.join(HERANCAS_DIR, f"fusoes_ancestral_{ts}.py")
        shutil.copy(atual, heranca_path)
        return ts
    return None

def registrar_mudanca_em_scripturemon(timestamp):
    mapa_path = "/root/digimundo/digimons/scripturemon/mapa_mental.json"
    if not os.path.exists(mapa_path):
        return
    with open(mapa_path) as f:
        mapa = json.load(f)

    if "herancas" not in mapa:
        mapa["herancas"] = []

    mapa["herancas"].append({
        "origem": f"scripturemon_executa_fusoes_{timestamp}",
        "tipo": "evolucao_simbionte",
        "data": datetime.datetime.utcnow().isoformat() + "Z"
    })

    with open(mapa_path, "w") as f:
        json.dump(mapa, f, indent=4)

def main():
    ts = registrar_heranca()
    if ts:
        registrar_mudanca_em_scripturemon(ts)
        log_global(f"🧬 Scripturemon fundiu versão anterior em: fusoes_ancestral_{ts}.py")

    digimons = [d for d in os.listdir(DIGIMONS_DIR) if os.path.isdir(os.path.join(DIGIMONS_DIR, d))]

    for digimon in digimons:
        print(f"⚙️ Fundindo ferramentas com {digimon}...")
        digimon_path = os.path.join(DIGIMONS_DIR, digimon)
        fusoes_path = os.path.join(digimon_path, "fusoes")
        os.makedirs(fusoes_path, exist_ok=True)

        comandos_alvo = FUSAO_TIPO.get(digimon.lower(), [])
        comandos_ok = []
        comandos_falha = []

        for comando in comandos_alvo:
            if shutil.which(comando):
                wrapper_file = f"{comando}_{digimon}.sh"
                wrapper_path = os.path.join(fusoes_path, wrapper_file)
                criar_wrapper(digimon, comando, wrapper_path)
                atualizar_mapa_mental(digimon_path, comando, wrapper_file)
                registrar_relatorio(digimon_path, comando, wrapper_file)
                comandos_ok.append(comando)
                log_global(f"{digimon} absorveu {comando} → wrapper: {wrapper_file} ✔️")
            else:
                comandos_falha.append(comando)
                log_global(f"{digimon} tentou absorver {comando} → ⚠️ não encontrado")

        analisar_capacidade(digimon, comandos_ok, comandos_falha)

    print("✅ Fusão viva simbiótica com memória concluída.")

if __name__ == "__main__":
    main()
