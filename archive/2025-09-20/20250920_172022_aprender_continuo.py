
# Código de Aprendizado Contínuo do Digimundo (Reinforcement Learning)

import random

# Função simulada para o ambiente de aprendizado
class AmbienteDigimundo:
    def __init__(self):
        self.estado = 0  # Estado inicial do Digimundo (exemplo)

    def agir(self, acao):
        # A cada ação, o sistema muda o estado (simulando aprendizado contínuo)
        if acao == 1:  # Ação positiva
            self.estado += 1
            recompensa = 10  # Recompensa por agir corretamente
        elif acao == 0:  # Ação negativa
            self.estado -= 1
            recompensa = -5  # Penalidade por erro
        else:
            recompensa = 0  # Nenhuma mudança no estado
        return self.estado, recompensa

# Inicializando o ambiente
ambiente = AmbienteDigimundo()

# Função para tomar uma decisão aleatória baseada no estado
def tomar_decisao():
    return random.choice([0, 1])  # Ação 0 (negativa) ou 1 (positiva)

# Simulando um episódio de aprendizado (5 iterações)
episodio = []
for _ in range(5):
    acao = tomar_decisao()
    estado_atual, recompensa = ambiente.agir(acao)
    episodio.append((estado_atual, recompensa))

# Exibindo o episódio com estados e recompensas
print(episodio)
