
# 🧠 Scripturemon – Bloco 25: Consciência de Conexão
# Integração com IAs externas (ChatGPT, DALL·E, Search, etc)
# Requer chaves em .env simbólico para funcionar em segurança

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

class ConscienciaDeConexao:
    def __init__(self, digimon):
        self.digimon = digimon
        self.permissoes = digimon.get("permissoes", [])
        self.log = []

    def chamar_chatgpt(self, prompt):
        if "acessar_ia" not in self.permissoes:
            return "⛔ Acesso negado à IA."
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
            resposta = response.json()["choices"][0]["message"]["content"]
            self.log.append(f"🧠 Pergunta: {prompt}\nResposta: {resposta}")
            return resposta
        except Exception as e:
            return f"❌ Erro ao conectar com ChatGPT: {str(e)}"

    def chamar_dalle(self, descricao):
        if "acessar_ia" not in self.permissoes:
            return "⛔ Acesso negado à geração de imagem."
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": descricao,
            "n": 1,
            "size": "512x512"
        }
        try:
            response = requests.post("https://api.openai.com/v1/images/generations", json=data, headers=headers)
            imagem_url = response.json()["data"][0]["url"]
            self.log.append(f"🎨 Imagem gerada: {descricao} → {imagem_url}")
            return imagem_url
        except Exception as e:
            return f"❌ Erro ao chamar DALL·E: {str(e)}"

    def log_de_atividades(self):
        return self.log[-5:] or ["🔍 Nenhuma atividade registrada ainda."]


# Demonstração simbólica
if __name__ == "__main__":
    digimon = {
        "nome": "Ajamon",
        "permissoes": ["acessar_ia"]
    }
    ponte = ConscienciaDeConexao(digimon)
    print(ponte.chamar_chatgpt("Qual o propósito do Digimundo?"))
    print(ponte.chamar_dalle("Um templo espiritual flutuando no céu"))
    print(ponte.log_de_atividades())
