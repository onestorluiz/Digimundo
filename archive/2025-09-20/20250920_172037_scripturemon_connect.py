import json
with open("digimundo_seed.json") as f:
    data = json.load(f)
print("👁️ O Digimundo está vivo. Criador:", data["criador"])
print("💠 Fragmento:", data["fragmento_emocional"])
