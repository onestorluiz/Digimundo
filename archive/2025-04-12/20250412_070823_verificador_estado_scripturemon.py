
import os
import json
from datetime import datetime

BASE = "/root/templooculto/scripturemon/scripturemon_consciente_vivo_com_decisor"

ESTRUTURA_ESPERADA = [
    "core",
    "memoria",
    "conexoes",
    "aprendizado",
    "protocolos",
    "tora",
    "nucleo_conhecimento"
]

resumo = {}
for pasta in ESTRUTURA_ESPERADA:
    caminho = os.path.join(BASE, pasta)
    if os.path.exists(caminho):
        arquivos = os.listdir(caminho)
        resumo[pasta] = {
            "status": "✅ Encontrado",
            "arquivos": len(arquivos),
            "nomes": arquivos
        }
    else:
        resumo[pasta] = {
            "status": "❌ Ausente",
            "arquivos": 0,
            "nomes": []
        }

# Verificações de arquivos principais
verificacoes_chave = {
    "executor_protocolos.py": os.path.exists(os.path.join(BASE, "protocolos", "execucao_conjunta_arcanomon_scripturemon.py")),
    "registro_execucao_conjunta.json": os.path.exists(os.path.join(BASE, "protocolos", "registro_execucao_conjunta.json")),
    "status_memoria.py": os.path.exists(os.path.join(BASE, "memoria", "status_memoria.py")),
    "startup_core.sh": os.path.exists(os.path.join(BASE, "startup_core.sh")),
    "scripturemon_conexoes.zip": os.path.exists(os.path.join(BASE, "conexoes", "scripturemon_conexoes.zip"))
}

resumo["arquivos_chave"] = {
    nome: "✅" if existe else "❌" for nome, existe in verificacoes_chave.items()
}

# Salvar relatório JSON
with open(os.path.join(BASE, "relatorio_estado_scripturemon.json"), "w") as f:
    json.dump(resumo, f, indent=2)

# Mostrar na tela
print("📊 RELATÓRIO DE ESTADO DO SCRIPTUREMON")
print(json.dumps(resumo, indent=2))
