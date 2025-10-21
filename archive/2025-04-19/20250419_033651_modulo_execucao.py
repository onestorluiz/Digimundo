import os
import zipfile
from pathlib import Path

LOG_ARQUIVO = "/root/scripturemon_conex_v2_autocorrecao/digimundo/logs/comandos_vivos.log"

def registrar_log(msg):
    with open(LOG_ARQUIVO, "a") as f:
        f.write(msg + "\n")

def executar_comando(comando_simbolico):
    resposta = ""
    try:
        if "descompacte" in comando_simbolico and ".zip" in comando_simbolico:
            partes = comando_simbolico.split()
            for parte in partes:
                if parte.endswith(".zip"):
                    zip_path = Path("/root") / parte
                    destino = Path("/root") / parte.replace(".zip", "")
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(destino)
                    resposta = f"✅ Arquivo {parte} descompactado em {destino}"
                    registrar_log(resposta)
                    return resposta
        elif "limpe os logs" in comando_simbolico:
            open(LOG_ARQUIVO, "w").close()
            resposta = "🧹 Logs limpos com sucesso."
            registrar_log(resposta)
            return resposta
        elif "crie uma pasta" in comando_simbolico:
            nome = comando_simbolico.split("pasta")[-1].strip().replace(" ", "_")
            nova = Path("/root") / nome
            nova.mkdir(exist_ok=True)
            resposta = f"📁 Pasta {nova} criada."
            registrar_log(resposta)
            return resposta
        else:
            resposta = "❌ Comando não reconhecido ou não permitido."
            registrar_log(resposta)
            return resposta
    except Exception as e:
        resposta = f"⚠️ Erro simbólico: {e}"
        registrar_log(resposta)
        return resposta