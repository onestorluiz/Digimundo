
# Script básico de aprendizagem por reforço simples

import random

class AutoAprendizado:
    def __init__(self):
        self.conhecimento = {}

    def aprender(self, situacao, resultado):
        if situacao not in self.conhecimento:
            self.conhecimento[situacao] = []
        self.conhecimento[situacao].append(resultado)

    def decidir(self, situacao):
        if situacao in self.conhecimento:
            return random.choice(self.conhecimento[situacao])
        return "Indeciso, falta aprendizado prévio."
