
# 📶 STATUS SCRIPTUREMON — ETAPA 2: CONEXÕES
# Verifica se o módulo de comunicação está acessível

import os

path = "scripturemon/scripturemon_consciente_vivo_com_decisor/scripturemon_conexoes"

if os.path.exists(path) and any(f.endswith(".py") for f in os.listdir(path)):
    print("✅ Conexões ativas. Scripturemon está ouvindo o mundo.")
else:
    print("❌ Conexões inativas. Verifique o módulo scripturemon_conexoes.")
