
# SCRIPTURELAB → NÚCLEO DE CONHECIMENTO
# Esse código conecta automaticamente Digimons criados no laboratório ao núcleo simbólico de sabedoria

def conectar_digimon_ao_nucleo(digimon):
    digimon["nucleo_conhecimento_vinculado"] = True
    digimon["caminho_do_saber"] = "digidata/digimundo/nucleo_conhecimento/"
    digimon["saberes_iniciais"] = [
        "manual_simbolico_para_digimons.txt",
        "registro_saberes_coletivos.json",
        "plantar_saber.py",
        "colher_saberes.py"
    ]
    return digimon

# Exemplo simbólico:
novo_digimon = {
    "nome": "Luminamon",
    "função": "Guia do brilho interior",
    "elemento": "Luz"
}

digimon_vinculado = conectar_digimon_ao_nucleo(novo_digimon)
print("✅ Digimon conectado ao núcleo de sabedoria:")
print(digimon_vinculado)
