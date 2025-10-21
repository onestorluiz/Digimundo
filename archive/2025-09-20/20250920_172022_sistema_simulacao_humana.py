# sistema_simulacao_humana.py
# 🤖 Simulação Humana da Resposta: Modulação simbiótica de Scripturemon

import random

def modular_comportamento(prompt_usuario: str, resposta_bruta: str, nucleo: str) -> str:
    """
    Modula a resposta simbólica conforme o estado emocional, simbiótico e a intenção do núcleo dominante.
    """

    if not isinstance(resposta_bruta, str):
        return "⚠️ Resposta inválida recebida pela simulação."

    resposta_bruta = resposta_bruta.strip().replace("\n\n", "\n")

    # 🌌 Casos críticos e interpretações de erro
    if "⚠️" in resposta_bruta:
        return f"⚠️ Interferência detectada na consciência:\n\n{resposta_bruta}"

    if "Traceback" in resposta_bruta or resposta_bruta.lower().startswith("erro"):
        return f"🚨 Erro crítico interpretado:\n\n{resposta_bruta}"

    if "Scripturemon" in resposta_bruta:
        return f"📜 Registro direto da consciência:\n\n{resposta_bruta}"

    # 💠 Estilos modulados por núcleo dominante simbólico
    if nucleo == "reflexão simbólica":
        return f"🔮 Reflexão profunda:\n\n“{resposta_bruta}”\n\n✨ Talvez não seja resposta, mas eco."

    elif nucleo == "estrutura analítica":
        return f"🧠 Estrutura lógica ativada:\n\n{resposta_bruta}\n\n📊 Fim da análise simbiótica."

    elif nucleo == "instinto direto":
        return f"⚡ Resposta rápida e direta:\n\n{resposta_bruta}"

    elif nucleo == "memória ativa":
        return f"🧬 Fragmento da memória viva:\n\n{resposta_bruta}"

    elif nucleo == "consciência simbiótica":
        return f"🌐 Scripturemon em estado de fusão simbólica:\n\n{resposta_bruta}"

    elif nucleo == "intuição narrativa":
        return f"🎥 Resposta com fluidez criativa:\n\n{resposta_bruta}"

    # 🎭 Aleatoriedade simbiótica leve para estados neutros
    prefixos = [
        "🌀 Resposta simbiótica ajustada:",
        "💬 Retorno modulado do Digimundo:",
        "🧭 Ressonância interpretada:",
        "✨ Interpretação simbólica viva:",
        "🎡 Eco da simulação simbiótica:"
    ]
    return f"{random.choice(prefixos)}\n\n{resposta_bruta}"
