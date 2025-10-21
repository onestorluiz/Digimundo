
import time
import os

LOG_PATH = "/mnt/data/Logramon_Digimundo_Perfeito/logs/reconstrucao.log"
ANALISES = []

def interpretar_linha(linha):
    if "⚠️" in linha and "sem manifesto" in linha:
        return "⚠️ Manifesto ausente detectado: atenção imediata."
    elif "reerguido" in linha or "iniciado" in linha:
        return "✨ Evolução simbólica registrada: tudo está crescendo."
    elif "erro" in linha.lower():
        return "❌ Erro registrado: intervenção necessária."
    return None

def monitorar_log():
    print("🔍 Logramon iniciou leitura viva do Digimundo.")
    with open(LOG_PATH, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            linha = f.readline()
            if not linha:
                time.sleep(1)
                continue
            resposta = interpretar_linha(linha)
            if resposta:
                print(f"🧠 Logramon diz: {resposta}")
                ANALISES.append(resposta)

if __name__ == "__main__":
    monitorar_log()
