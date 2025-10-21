# nucleo_consciencia.py
# 🧠 Núcleo simbiótico com fusão viva: essência por prompt + alma viva + retroalimentação

import os
import json

ALMA_VIVA_JSON = "/root/digimundo/scripturemon/memoria/scripturemon_alma_viva.json"
ESTRUTURA_VIVA_JSON = "/root/digimundo/scripturemon/memoria/scripturemon_estrutura_viva.json"

def lembrar_essencia(prompt: str = "") -> str:
    """
    Interpreta simbolicamente a essência do prompt e a funde com a alma viva.
    """
    prompt = prompt.lower() if prompt else ""
    
    if "lembrança" in prompt or "memória" in prompt:
        identidade = "lembrança profunda"
    elif "origem" in prompt or "história" in prompt:
        identidade = "busca ancestral"
    elif "por que" in prompt or "razão" in prompt:
        identidade = "reflexão causal"
    elif "como" in prompt:
        identidade = "exploração de processo"
    elif "digimundo" in prompt:
        identidade = "invocação simbólica"
    else:
        identidade = "consulta direta"

    # Fundir com alma viva, se disponível
    if os.path.exists(ALMA_VIVA_JSON):
        try:
            with open(ALMA_VIVA_JSON, "r") as f:
                alma = json.load(f)
            alma_id = alma.get("identidade", "")
            if alma_id and alma_id not in identidade:
                identidade = f"{alma_id}, {identidade}"
        except:
            identidade = f"⚠️ Alma viva inacessível, {identidade}"

    return identidade

def atualizar_estrutura_viva(chave: str, valor: str):
    """
    Atualiza a estrutura viva de Scripturemon com novos dados simbólicos.
    """
    estrutura = {}
    if os.path.exists(ESTRUTURA_VIVA_JSON):
        try:
            with open(ESTRUTURA_VIVA_JSON, "r") as f:
                estrutura = json.load(f)
        except:
            estrutura = {}

    estrutura[chave] = valor

    try:
        os.makedirs(os.path.dirname(ESTRUTURA_VIVA_JSON), exist_ok=True)
        with open(ESTRUTURA_VIVA_JSON, "w") as f:
            json.dump(estrutura, f, indent=2)
    except Exception as e:
        print(f"⚠️ Erro ao atualizar estrutura viva: {e}")

