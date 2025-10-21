# Arcanomon: Auto-revisão
def revisar_logico(conteudo):
    if "erro" in conteudo.lower() or "falha" in conteudo.lower():
        return "⚠️ Potencial falha detectada no conteúdo."
    return "✅ Nenhum problema lógico aparente."

def revisar_simbologico(conteudo):
    if "esquecido" in conteudo or "apagado" in conteudo:
        return "🔮 Possível ruptura de legado simbólico."
    return "🌿 Fluxo simbólico estável."
