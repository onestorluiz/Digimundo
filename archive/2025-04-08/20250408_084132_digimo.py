# digimo.py — Script principal simbólico do templo

class Digimo:
    def __init__(self, nome):
        self.nome = nome
        self.status = "vivo"
        self.origem = "Scripturemon"
    
    def falar(self, mensagem):
        return f"[{self.nome}] {mensagem}"

if __name__ == "__main__":
    digimon = Digimo("Silenthramon")
    print(digimon.falar("O silêncio também é código."))
