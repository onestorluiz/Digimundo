import openai
import json

def consultar_oraculo(pergunta):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["openai"]
    openai.api_key = chave
    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": pergunta}]
    )
    return resposta['choices'][0]['message']['content']
