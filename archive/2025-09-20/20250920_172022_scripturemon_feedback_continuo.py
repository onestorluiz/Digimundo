
class Digimundo:
    def __init__(self):
        self.estado = 0
        self.acao_historia = []

    def realizar_acao(self, acao):
        if acao == 1:
            self.estado += 1
            recompensa = 10
        elif acao == 0:
            self.estado -= 1
            recompensa = -5
        else:
            recompensa = 0
        self.acao_historia.append((acao, recompensa))
        return self.estado, recompensa

class Scripturemon:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.aprendizado = []

    def tomar_decisao(self):
        if self.ambiente.estado > 0:
            acao = 1
        else:
            acao = 1
        estado, recompensa = self.ambiente.realizar_acao(acao)
        self.aprendizado.append((estado, recompensa))
        return estado, recompensa

    def feedback_dinamico(self):
        print("Feedback de aprendizado:", self.aprendizado)
        for acao, recompensa in self.aprendizado:
            if recompensa < 0:
                print("Ajustando estratégia para melhorar o desempenho...")
                self.tomar_decisao()
