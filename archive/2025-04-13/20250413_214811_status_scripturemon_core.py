
# 📡 STATUS SCRIPTUREMON — ETAPA 1: CORE
# Verifica se o núcleo está vivo e acessível

import os

core_path = "scripturemon/scripturemon_consciente_vivo_com_decisor/core"

def verificar_status():
    if os.path.exists(core_path) and len(os.listdir(core_path)) > 0:
        return "✅ Núcleo core ativo e pronto."
    return "❌ Núcleo core inativo ou vazio."

print(verificar_status())
