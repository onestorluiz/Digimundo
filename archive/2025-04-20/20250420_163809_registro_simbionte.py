import datetime
import os
from pathlib import Path

hoje = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
saida = Path(f"/root/digimundo/livro_vivo/entradas_simbiontes/log_simbionte_{hoje}.md")
saida.parent.mkdir(parents=True, exist_ok=True)

caminhos = [
    "/var/log/digimundo_manutencao.log",
    "/var/log/unattended-upgrades/unattended-upgrades.log",
    "/var/log/syslog",
]

conteudo = f"# 📘 Registro Simbiótico – {hoje}\n\n"

for caminho in caminhos:
    if os.path.exists(caminho):
        conteudo += f"\n## 📄 {caminho}\n"
        with open(caminho) as f:
            linhas = f.readlines()[-20:]
            conteudo += "".join(["> " + l for l in linhas])
    else:
        conteudo += f"\n❌ Caminho não encontrado: {caminho}\n"

with open(saida, "w") as f:
    f.write(conteudo)

print(f"✅ Registro simbiótico salvo em: {saida}")
