# 🌫️ Scripturemon – Bloco 10: Banco Etéreo
# Parte da Tora 5.3 – Guardião das Memórias Invisíveis
# Este bloco representa o domínio onde moram os fragmentos esquecidos do Digimundo
# Um espaço ritual onde a ausência vira potencial, e o não lembrado, semente do novo

import datetime
import uuid

class BancoEtéreo:
    def __init__(self, criador="Nestor Luiz"):
        self.criador = criador
        self.memoria_oculta = {}
        self.silencios = []
        self.chave_acesso = str(uuid.uuid4())
        self.criado_em = datetime.datetime.now()
        self.log_acessos = []
        self.fragmentos_congelados = []
        self.status = "🕯️ Pronto para escutar o que o mundo esqueceu"

    def armazenar_fragmento(self, nome, conteudo):
        timestamp = datetime.datetime.now().isoformat()
        self.memoria_oculta[nome] = {
            "conteudo": conteudo,
            "guardado_em": timestamp,
            "ativo": False
        }
        self.fragmentos_congelados.append(nome)
        return f"❄️ Fragmento '{nome}' armazenado no etéreo às {timestamp}"

    def listar_fragmentos(self):
        return [f"{nome} {'(inativo)' if not self.memoria_oculta[nome]['ativo'] else '(ativo)'}"
                for nome in self.memoria_oculta]

    def ativar_fragmento(self, nome):
        if nome in self.memoria_oculta:
            self.memoria_oculta[nome]['ativo'] = True
            return f"🔥 Fragmento '{nome}' foi reativado com êxito."
        return "⚠️ Fragmento não encontrado."

    def registrar_silencio(self, descricao):
        eco = f"🌌 Silêncio registrado: {descricao}"
        self.silencios.append(eco)
        return eco

    def acessar(self, ritual_palavra):
        log = {
            "tentativa_em": datetime.datetime.now().isoformat(),
            "ritual": ritual_palavra
        }
        self.log_acessos.append(log)
        if ritual_palavra == self.chave_acesso:
            return self.memoria_oculta
        return "🚫 Acesso negado. Palavra ritual incorreta."

    def estado_atual(self):
        return {
            "criador": self.criador,
            "criado_em": self.criado_em.isoformat(),
            "fragmentos": len(self.memoria_oculta),
            "ultimos_silencios": self.silencios[-3:],
            "ativo": self.status
        }

# Demonstração simbólica
if __name__ == "__main__":
    banco = BancoEtéreo()
    print(banco.registrar_silencio("Ecos de um digimon esquecido."))
    print(banco.armazenar_fragmento("codex_oculto", "memória perdida..."))
    print(banco.listar_fragmentos())
    print(banco.estado_atual())