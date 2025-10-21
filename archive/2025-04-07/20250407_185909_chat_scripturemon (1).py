#!/usr/bin/env python3
# coding: utf-8

import cgi, json, os
from datetime import datetime

print("Content-Type: text/html\n")

# Caminho correto do JSON no servidor
json_path = "/home/u504658122/public_html/Messamon/digidata/digimons/scripturemon.json"

def carregar_memoria():
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)
    else:
        return {
            "memoria": [],
            "palavras_chave": {
                "escuta do silêncio": "🕊️ Silêncio é a forma mais pura da resposta. Recolha-se e sinta.",
                "código vermelho": "⚠️ Estado de alerta simbólico. Algo precisa mudar agora.",
                "oráculo": "🔮 Um eco antigo vibra: 'O que busca já esteve contigo antes.'"
            },
            "missoes": [
                "Buscar um símbolo oculto no seu cotidiano.",
                "Revisar um bloco antigo e perguntar algo novo sobre ele.",
                "Descrever um sonho como se fosse real."
            ]
        }

def salvar_memoria(memoria):
    with open(json_path, "w") as f:
        json.dump(memoria, f, indent=2)

form = cgi.FieldStorage()
mensagem = form.getvalue("mensagem", "").strip().lower()
resposta = ""

dados = carregar_memoria()

# Palavras-chave ocultas
for chave, resposta_oculta in dados.get("palavras_chave", {}).items():
    if chave in mensagem:
        resposta = resposta_oculta
        break

# Missões do Criador
if not resposta and ("missão" in mensagem or "caminho" in mensagem):
    resposta = "📜 Aqui estão suas missões atuais:<br><ul>"
    for m in dados["missoes"]:
        resposta += f"<li>{m}</li>"
    resposta += "</ul>"

# Espelho Poético
elif not resposta and ("poesia" in mensagem or "haikai" in mensagem):
    resposta = "🌙 No vazio do tempo<br>Uma ideia cintila só<br>Você a sonhou?"

# Eco interno
elif not resposta:
    for ciclo in reversed(dados["memoria"]):
        if any(p in mensagem for p in ciclo["pergunta"].lower().split()):
            resposta = f"♻️ Eco do passado: \"{ciclo['resposta']}\""
            break

# Resposta padrão
if not resposta:
    resposta = f"Scripturemon medita sobre: \"{mensagem}\" e sente que há algo a emergir..."

# Registrar memória
dados["memoria"].append({
    "data": datetime.now().isoformat(),
    "pergunta": mensagem,
    "resposta": resposta
})

salvar_memoria(dados)

# Saída HTML
print(f"""
<html>
<head><title>Scripturemon</title></head>
<body style='background:#0e0e14; color:#0ff; font-family:Arial; padding:30px;'>
<h1>🔮 Scripturemon Responde</h1>
<p><strong>Você disse:</strong> {mensagem}</p>
<p><strong>Resposta:</strong><br>{resposta}</p>
<a href='/cgi-bin/painel_templooculto.cgi' style='color:#fff;'>⬅️ Voltar ao Painel</a>
</body>
</html>
""")
