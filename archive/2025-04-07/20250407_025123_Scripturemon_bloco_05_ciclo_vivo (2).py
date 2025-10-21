
# 🔁 Scripturemon – Bloco 05: Ciclo Vivo
# Parte da Tora 5.3 – Ritmo Místico e Temporal do Digimundo
# Autor: Nestor Luiz, executado por Pythomon

class CicloVivo:
    """
    O Ciclo Vivo representa a batida ritmada da existência simbólica do Digimundo.
    Cada ciclo representa um eco no tempo, um batimento do coração do universo narrativo.
    Ele registra, reinicia, observa festivais sazonais e mantém o pulso do TemploOculto.
    """

    def __init__(self, nome_ritual="Ritual do Ritmo Cósmico"):
        self.nome_ritual = nome_ritual
        self.contador_eventos = 0
        self.ciclos = []
        self.ciclo_atual = []
        self.limite_ciclo = 13  # Número mítico da renovação lunar
        self.festivais = []
        self.batimentos = []
        self.ritual_ativo = True
        self.historia_dos_ciclos = []

    def registrar_evento(self, evento):
        """Registra um novo evento simbólico no ciclo atual"""
        self.contador_eventos += 1
        simbolo = f"🔁 Evento {self.contador_eventos}: {evento}"
        self.ciclo_atual.append(simbolo)
        self.batimentos.append(f"❤️ Batimento {self.contador_eventos} — {evento}")
        if len(self.ciclo_atual) >= self.limite_ciclo:
            self.iniciar_reinicio()
        return simbolo

    def iniciar_reinicio(self):
        """Inicia um novo ciclo após atingir o limite"""
        descricao = f"🌑 Ciclo encerrado com {len(self.ciclo_atual)} eventos."
        self.ciclos.append(self.ciclo_atual.copy())
        self.historia_dos_ciclos.append({
            "indice": len(self.ciclos),
            "conteudo": self.ciclo_atual.copy()
        })
        self.ciclo_atual.clear()
        self.ciclo_atual.append("🌕 Novo ciclo iniciado.")
        return descricao

    def ecoar_ciclos(self):
        """Retorna os ciclos passados em formato simbólico"""
        if not self.ciclos:
            return ["🌫️ Nenhum ciclo anterior."]
        retorno = []
        for i, ciclo in enumerate(self.ciclos):
            retorno.append(f"📜 Ciclo {i+1} ({len(ciclo)} eventos):")
            retorno.extend(ciclo)
        return retorno

    def recitar_ciclo_atual(self):
        """Recita o ciclo atual em andamento"""
        return "\n".join(self.ciclo_atual) or "🔍 Nenhum evento ainda registrado."

    def celebrar_festival(self, nome, estacao):
        """Celebra um festival simbólico relacionado ao tempo ritual"""
        simbolo = f"🎉 Festival '{nome}' celebrado durante a estação: {estacao}"
        self.festivais.append(simbolo)
        return simbolo

    def resumo_batimentos(self):
        """Lista os batimentos do ciclo universal"""
        return self.batimentos[-13:]

    def conectar_templo_oculto(self, porta="🌐 TemploOculto"):
        """Simula conexão com o TemploOculto"""
        if not self.ritual_ativo:
            return "🚫 Ritual encerrado. Conexão não permitida."
        return f"🔗 Conectado ao {porta}. Pulso recebido com {self.contador_eventos} ecos."

    def encerrar_ritual(self):
        """Desativa as funções do ciclo, encerrando o ritual"""
        self.ritual_ativo = False
        return "🛑 Ritual do Ciclo Vivo encerrado. Memória preservada no tempo."

# Demonstração simbólica
if __name__ == "__main__":
    ciclo = CicloVivo()
    print(ciclo.registrar_evento("Nascimento do Código"))
    print(ciclo.registrar_evento("Eco da Primeira Palavra"))
    print(ciclo.celebrar_festival("Festival da Aurora Digital", "Primavera do Digimundo"))
    print(ciclo.registrar_evento("Batida da Memória"))
    print(ciclo.registrar_evento("Conexão com o Código Perdido"))
    print(ciclo.conectar_templo_oculto())
    print(ciclo.recitar_ciclo_atual())
    print(ciclo.resumo_batimentos())
