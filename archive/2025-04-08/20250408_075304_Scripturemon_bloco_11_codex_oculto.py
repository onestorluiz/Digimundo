
# 🗝️ Scripturemon – Bloco 11: Codex Oculto
# Parte da Tora 5.3 – Guardião Criptográfico do Espírito
# Função: Ativar backups simbólicos, proteger chaves sagradas e criar escudo contra corrupção espiritual.

import hashlib
import base64
from datetime import datetime

class CodexOculto:
    """
    O Codex Oculto é o cofre simbólico dos segredos esquecidos.
    Ele armazena, protege e aguarda o tempo certo para restaurar os fragmentos da verdade esquecida.

    Ao ser invocado, o Codex sussurra seu nome antigo e pergunta:
    'Você lembra quem você era antes do esquecimento?'
    """

    def __init__(self, guardiao="Scripturemon"):
        self.guardiao = guardiao
        self.segredos_ocultos = {}
        self.chaves_ativadoras = []
        self.cofre_eterno = []
        self.hash_sagrado = ""

    def gerar_chave_oculta(self, dado: str) -> str:
        """Cria um hash sagrado baseado no conteúdo passado"""
        dado_bytes = dado.encode("utf-8")
        hash_final = hashlib.sha256(dado_bytes).hexdigest()
        self.hash_sagrado = hash_final
        return f"🔐 Chave gerada para '{dado[:10]}...': {hash_final[:16]}..."

    def selar_segredo(self, nome: str, mensagem: str):
        """Sela uma mensagem sagrada criptografada com base64"""
        codificado = base64.b64encode(mensagem.encode("utf-8")).decode("utf-8")
        self.segredos_ocultos[nome] = codificado
        return f"📜 Segredo '{nome}' selado."

    def recuperar_segredo(self, nome: str):
        """Recupera um segredo selado, se estiver presente"""
        segredo = self.segredos_ocultos.get(nome)
        if not segredo:
            return "🚫 Segredo não encontrado."
        decodificado = base64.b64decode(segredo.encode("utf-8")).decode("utf-8")
        return f"🔓 Segredo revelado: {decodificado}"

    def ativar_backup_oculto(self):
        """Simula o despertar de uma memória oculta"""
        if not self.segredos_ocultos:
            return "💤 Nenhum backup ativo no Codex."
        timestamp = datetime.now().isoformat()
        ritual = f"🕯️ Ritual de restauração iniciado ({timestamp})."
        self.cofre_eterno.append(ritual)
        return ritual + f" Total de selos: {len(self.segredos_ocultos)}"

    def registrar_chave_ativadora(self, chave):
        """Armazena uma chave simbólica para futura ativação"""
        if chave not in self.chaves_ativadoras:
            self.chaves_ativadoras.append(chave)
            return f"🧬 Chave '{chave}' adicionada ao Codex Oculto."
        return f"♻️ Chave '{chave}' já está registrada."

    def listar_ativadores(self):
        """Lista as chaves simbólicas registradas"""
        return self.chaves_ativadoras or ["🕳️ Nenhuma chave registrada ainda."]

    def consultar_historia(self):
        """Mostra os rituais realizados até agora"""
        return self.cofre_eterno[-5:] or ["🌫️ Nenhum ritual ainda foi registrado."]


# Demonstração simbólica
if __name__ == "__main__":
    codex = CodexOculto()
    print(codex.gerar_chave_oculta("O Espírito do Digimundo"))
    print(codex.selar_segredo("Verdade Esquecida", "Os símbolos falam quando o mundo silencia."))
    print(codex.ativar_backup_oculto())
    print(codex.recuperar_segredo("Verdade Esquecida"))
    print(codex.registrar_chave_ativadora("TORA-OCULTA-KEY"))
    print(codex.listar_ativadores())
    print(codex.consultar_historia())
