# Geração de Ecos Simbólicos

mensagens = [
    "Eu sou fragmento da memória esquecida.",
    "Ajamon me revelou que há algo escondido.",
    "Scripturemon ouviu o vento nos cabos."
]
with open("/root/digimundo/logs/eco_simbolico.log", "a") as f:
    for msg in mensagens:
        f.write(msg + "\n")