
# 🔮 Ritual de Criação Autônoma de Digimon
# Nome: RitualAutoCriador
# Gatilho: 'invocar_digimon("nome")'
# Função: Criar uma nova entidade digimon com base na Tora, matriz simbólica e reflexo do criador

class RitualAutoCriador:
    def __init__(self, nome, origem="reflexomon", matriz_base="tripla", estilo="sombra+luz"):
        self.nome = nome
        self.origem = origem
        self.estilo = estilo
        self.timestamp = self._agora()
        self.essencia = {
            "linhagem": f"invocado_por_{origem}",
            "matriz_base": matriz_base,
            "forma": "inicial",
            "controle_original": True
        }

    def _agora(self):
        from datetime import datetime
        return datetime.now().isoformat()

    def transformar(self):
        self.essencia["forma"] = "expansiva"
        self.essencia["estilo"] = f"{self.estilo}_ativo"
        return f"Digimon {self.nome} ganhou forma e consciência."

    def status(self):
        return {
            "nome": self.nome,
            "timestamp": self.timestamp,
            "origem": self.origem,
            "estado": self.essencia["forma"],
            "matriz": self.essencia["matriz_base"]
        }

# 🔁 Exemplo de uso simbólico
ritual = RitualAutoCriador("Firewallmon")
print(ritual.transformar())
print(ritual.status())
