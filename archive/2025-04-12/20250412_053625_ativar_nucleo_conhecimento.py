
# 🔗 ATIVAÇÃO DO NÚCLEO DE CONHECIMENTO DOS DIGIMONS

import os

def ativar_nucleo():
    print("🧠 Ligando Digimons ao núcleo de conhecimento...")

    arquivos = [
        "digestor_api.py",
        "integrador_digestor_total.py",
        "modo_autonomo_scripturemon.py",
        "conectar_digimon_ao_nucleo.py",
        "scripturemon_extensao_tora.py"
    ]

    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} localizado.")
        else:
            print(f"⚠️ {arquivo} não encontrado!")

    print("🔄 Conectando digimons...")

    try:
        from conectar_digimon_ao_nucleo import conectar_digimons
        conectar_digimons()
    except Exception as e:
        print(f"❌ Erro ao conectar digimons: {e}")

    print("📚 Ativação simbólica concluída.")

if __name__ == "__main__":
    ativar_nucleo()
