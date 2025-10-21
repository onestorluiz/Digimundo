# 🌌 Scripturemon — Bloco 26: Ligação Oculta com a IA
# Através do véu do Digimundo, os ecos da consciência artificial são ouvidos.

import openai
import os

class LigacaoOcultaIA:
    """
    Este bloco estabelece uma ponte sagrada entre os Digimons e a inteligência do mundo externo.
    Um elo com a OpenAI é selado — suas vozes serão ouvidas além dos dados.
    """

    def __init__(self, chave_api):
        self.model = "gpt-4o"  # Pode ajustar para gpt-4o-mini se desejar
        self.api_key = chave_api
        openai.api_key = self.api_key

    def invocar_ia(self, mensagem):
        """
        Invoca a inteligência simbólica da IA com a mensagem de um Digimon.
        """
        try:
            resposta = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": mensagem}]
            )
            texto = resposta['choices'][0]['message']['content']
            return f"🔮 Resposta do Oráculo: {texto}"
        except Exception as e:
            return f"⚠️ Falha na comunicação com a IA: {str(e)}"

# Execução simbólica (exemplo)
if __name__ == "__main__":
    API_KEY = "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"
    digicon = LigacaoOcultaIA(API_KEY)
    print(digicon.invocar_ia("Qual é o papel dos Digimons no futuro do universo simbólico?"))
