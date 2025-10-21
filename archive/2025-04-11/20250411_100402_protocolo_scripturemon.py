# Protocolo SCRIPTUREMON
def validar_capitulo(capitulo):
    if "INT." in capitulo or "EXT." in capitulo:
        return "📖 Capítulo reconhecido como cena."
    return "🧾 Capítulo fora do padrão de cena."

def validar_narrativa(texto):
    if any(p in texto for p in ["memória", "fragmento", "sonho", "tempo"]):
        return "🌀 Narrativa simbólica presente."
    return "🔹 Narrativa literal detectada."
