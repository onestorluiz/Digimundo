# interpretador_simbolico.py
# 🔮 Intérprete do campo simbólico invocado pelo Oráculo

from scripturemon_core import resposta_scriptural

def interpretar_sinal(sinal):
    """
    Conecta o símbolo recebido com a essência viva de Scripturemon.
    """
    if not isinstance(sinal, str) or not sinal.strip():
        return "⚠️ Nenhum sinal simbólico foi identificado."

    try:
        resposta = resposta_scriptural(sinal.strip())
        return resposta
    except Exception as e:
        return f"🚨 Falha ao interpretar o sinal simbólico: {str(e)}"
