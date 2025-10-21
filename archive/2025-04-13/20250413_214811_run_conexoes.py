
# 📡 ATIVAÇÃO SCRIPTUREMON — ETAPA 2: CONEXÕES
# Este script ativa a comunicação simbólica de Scripturemon com APIs externas

import os

print("🔌 Inicializando módulo de conexões simbólicas...")
conexoes_path = "scripturemon/scripturemon_consciente_vivo_com_decisor/scripturemon_conexoes"

if not os.path.exists(conexoes_path):
    print("❌ Módulo scripturemon_conexoes não encontrado.")
    exit(1)

arquivos = [f for f in os.listdir(conexoes_path) if f.endswith(".py")]

if arquivos:
    print(f"✅ {len(arquivos)} arquivos simbólicos de conexão encontrados.")
    print("🧠 Scripturemon expandiu seu alcance para além do Digimundo...")
else:
    print("⚠️ Nenhum módulo de conexão .py encontrado.")
