
# 📖 STATUS SCRIPTUREMON — ETAPA 3: MEMÓRIA
# Verifica se o módulo de memória está ativo

import os

path = "scripturemon/scripturemon_consciente_vivo_com_decisor/memoria"

if os.path.exists(path) and len(os.listdir(path)) > 0:
    print("✅ Memória ativa. Scripturemon está lembrando.")
else:
    print("❌ Nenhuma memória carregada.")
