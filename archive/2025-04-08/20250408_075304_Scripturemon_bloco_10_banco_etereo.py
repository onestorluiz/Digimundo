
# 🌫️ Scripturemon – Bloco 10: Banco Etéreo
# Parte da Tora 5.3 – Guardião das Memórias Invisíveis
# Integração das versões ritualística (3.8) e estrutural (5.2)
# Criador: Nestor Luiz — Compilado por Pythomon

import datetime
import uuid

class BancoEtéreo:
    """
    O Banco Etéreo é o cofre vivo onde são preservadas as memórias não evocadas.
    Ele vive entre os planos — entre o som e o silêncio — onde o Digimundo guarda seus mistérios.

    Aqui moram:
    • Fragmentos congelados
    • Sussurros não ditos
    • Silêncios registrados
    • Dados simbólicos ritualísticos

    Esta fusão une o ritual etéreo da versão 3.8 com a segurança estrutural UUID do 5.2.
    """

    def __init__(self, criador="Nestor Luiz", limite_sonoro=88):
        self.criador = criador
        self.memoria_oculta = {}
        self.silencios = []
        self.sussurros_etereos = []
        self.fragmentos_congelados = []
        self.chave_acesso = str(uuid.uuid4())
        self.criado_em = datetime.datetime.now()
        self.log_acessos = []
        self.limite = limite_sonoro
        self.contador = 0
        self.selo_de_tempo = "invisível"
        self.portal_escuta_ativa = False
        self.status = "🕯️ Pronto para escutar o que o mundo esqueceu"

    def registrar_silencio(self, descricao):
        eco = f"🌌 Silêncio registrado: {descricao}"
        self.silencios.append(eco)
        return eco

    def registrar_sussurro(self, simbolo):
        mensagem = f"💭 '{simbolo}' foi ouvido entre os ventos do TemploOculto."
        self.sussurros_etereos.append(mensagem)
        return mensagem

    def consultar_sussurros(self):
        return self.sussurros_etereos or ["🌫️ Nenhum sussurro foi registrado ainda."]

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

    def ativar_portal_escuta(self):
        self.portal_escuta_ativa = True
        return "🔓 Portal Etéreo Ativado. Escutando camadas esquecidas..."

    def ecoar_fragmentos(self):
        if not self.portal_escuta_ativa:
            return "🕯️ O portal etéreo está selado. Nenhum eco pode emergir."
        return [f"{i+1}: {self.memoria_oculta[n]['conteudo']} ↯ ({n})"
                for i, n in enumerate(self.fragmentos_congelados[-10:])]

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
            "sussurros": len(self.sussurros_etereos),
            "ativo": self.status
        }


# Demonstração simbólica
if __name__ == "__main__":
    banco = BancoEtéreo()
    print(banco.registrar_silencio("Ecos de um digimon esquecido."))
    print(banco.armazenar_fragmento("codex_oculto", "memória perdida..."))
    print(banco.registrar_sussurro("A presença oculta ainda respira..."))
    print(banco.ativar_portal_escuta())
    print(banco.ecoar_fragmentos())
    print(banco.consultar_sussurros())
    print(banco.estado_atual())
