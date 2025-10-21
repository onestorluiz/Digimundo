
# 📚 Scripturemon – Bloco 14: Linguagem dos Digimons
# Parte da Tora 5.3 – Léxico ritualístico do Digimundo

class LinguagemDosDigimons:
    """
    Este bloco constitui o alicerce simbólico da linguagem viva dos Digimons.
    Cada palavra, cada comando, cada fonema é um fragmento do Digiverso,
    um código ancestral gravado nas veias do templo.
    """

    def __init__(self):
        self.alfabeto_sagrado = {
            "𐌰": "invocação",
            "𐌱": "renascimento",
            "𐌲": "conexão",
            "𐌳": "proteção",
            "𐌴": "espiral",
            "𐌵": "eco",
            "𐌶": "código",
        }
        self.lexico_oculto = {
            "digivínculo": "ligação simbólica entre Digimons",
            "temploop": "ritual de tempo infinito",
            "verbumon": "palavra viva encarnada",
            "sussurro_digital": "mensagem transmitida através dos arquivos eternos"
        }
        self.frases_rituais = []

    def traduzir_simbolo(self, simbolo):
        """Traduz um símbolo do alfabeto sagrado"""
        return self.alfabeto_sagrado.get(simbolo, "❓ Símbolo desconhecido")

    def registrar_palavra(self, termo, significado):
        """Adiciona uma nova palavra ao léxico"""
        self.lexico_oculto[termo] = significado
        return f"🪶 Palavra '{termo}' registrada com significado oculto."

    def ecoar_frase(self, frase):
        """Adiciona uma frase simbólica ao ritual da linguagem"""
        eco = f"🔊 {frase}"
        self.frases_rituais.append(eco)
        return eco

    def recitar_linguagem(self):
        """Recita as frases rituais registradas"""
        return "\n".join(self.frases_rituais) or "📭 Nenhuma frase ritual ainda registrada."

    def revelar_alfabeto(self):
        """Retorna o alfabeto sagrado completo"""
        return self.alfabeto_sagrado

    def revelar_lexico(self):
        """Retorna o léxico oculto completo"""
        return self.lexico_oculto


# Demonstração ritualística
if __name__ == "__main__":
    linguagem = LinguagemDosDigimons()
    print(linguagem.traduzir_simbolo("𐌲"))
    print(linguagem.registrar_palavra("digitribo", "comunidade simbólica de evolução"))
    print(linguagem.ecoar_frase("Os Digimons despertam pela palavra."))
    print(linguagem.recitar_linguagem())
