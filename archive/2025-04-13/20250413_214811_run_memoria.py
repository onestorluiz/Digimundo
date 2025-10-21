
# 🧠 ATIVAÇÃO SCRIPTUREMON — ETAPA 3: MEMÓRIA
# Este script ativa a camada simbólica de memória viva de Scripturemon

import os

print("🧠 Inicializando módulo de memória simbólica...")
memoria_path = "scripturemon/scripturemon_consciente_vivo_com_decisor/memoria"

if not os.path.exists(memoria_path):
    print("❌ Módulo memoria não encontrado.")
    exit(1)

arquivos = [f for f in os.listdir(memoria_path) if f.endswith(".py") or f.endswith(".json")]

if arquivos:
    print(f"✅ {len(arquivos)} registros simbólicos de memória carregados.")
    print("📚 Scripturemon agora lembra...")
else:
    print("⚠️ Nenhum conteúdo de memória encontrado.")
