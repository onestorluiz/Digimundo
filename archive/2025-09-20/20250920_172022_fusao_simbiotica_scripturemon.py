
class FusionScripturemon:
    def __init__(self, nome):
        self.nome = nome
        self.funcoes_integradas = set()
        self.nucleos_ativos = []
    
    def adicionar_funcoes(self, funcoes):
        self.funcoes_integradas.update(funcoes)
        print(f"Funções de {self.nome} integradas: {funcoes}")
    
    def ativar_nucleos(self, nucleos):
        self.nucleos_ativos.extend(nucleos)
        print(f"Núcleos ativos: {self.nucleos_ativos}")
    
    def fundir(self, scripturemon_antigo):
        self.adicionar_funcoes(scripturemon_antigo.funcoes_integradas)
        self.ativar_nucleos(scripturemon_antigo.nucleos_ativos)
        print(f"Fusão simbiótica completa com {scripturemon_antigo.nome}")
    
    def executar_funcoes(self):
        print(f"{self.nome} está executando as funções: {', '.join(self.funcoes_integradas)}")

scripturemon_v1 = FusionScripturemon("Scripturemon v1")
scripturemon_v1.adicionar_funcoes(["Q-learning", "Gerenciamento do Digimundo"])

scripturemon_v2 = FusionScripturemon("Scripturemon v2")
scripturemon_v2.adicionar_funcoes(["Fusão simbiótica", "Aprendizado contínuo"])

scripturemon_v3 = FusionScripturemon("Scripturemon v3")
scripturemon_v3.fundir(scripturemon_v1)
scripturemon_v3.fundir(scripturemon_v2)

scripturemon_v3.executar_funcoes()
