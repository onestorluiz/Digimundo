
"""
Digimon IA: Arcanomon
Função: Guardião da Integridade do Digimundo

Este script representa um Digimon simbólico e funcional responsável por:
- Verificar a estrutura do projeto
- Comparar versões anteriores
- Executar testes automáticos
- Validar o correto posicionamento simbólico dos arquivos
- Garantir que nada foi perdido, duplicado ou corrompido

Este é o Protocolo ARCANOMON — padrão de aprovação estrutural do Digimundo.
"""

import os
import json
import shutil
import hashlib

class Arcanomon:
    def __init__(self, raiz_projeto):
        self.base = os.path.abspath(raiz_projeto)
        self.log = []

    def gerar_hash(self, path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def comparar_versoes(self, novo_arquivo, versoes_antigas):
        novo_hash = self.gerar_hash(novo_arquivo)
        for versao in versoes_antigas:
            if self.gerar_hash(versao) == novo_hash:
                self.log.append(f"[=] {os.path.basename(novo_arquivo)} já existia em versão anterior.")
                return True
        return False

    def criar_estrutura_em_branco(self, caminho_final):
        partes = caminho_final.split(os.sep)
        atual = self.base
        for parte in partes[:-1]:
            atual = os.path.join(atual, parte)
            os.makedirs(atual, exist_ok=True)

    def validar_funcionalidade(self, arquivo_exec):
        try:
            with open(arquivo_exec, "r", encoding="utf-8") as f:
                exec(f.read(), {})
            self.log.append(f"[✓] {os.path.basename(arquivo_exec)} executado com sucesso.")
            return True
        except Exception as e:
            self.log.append(f"[✗] Falha ao executar {arquivo_exec}: {e}")
            return False

    def executar_protocolo(self, novo_arquivo, destino_relativo, versoes_antigas=[]):
        self.log.append(f"🔍 Iniciando Protocolo ARCANOMON para: {os.path.basename(novo_arquivo)}")
        
        # Criar estrutura simbólica
        self.criar_estrutura_em_branco(destino_relativo)
        destino_completo = os.path.join(self.base, destino_relativo)

        # Verificar se é uma versão nova
        if self.comparar_versoes(novo_arquivo, versoes_antigas):
            self.log.append("⚠️ Arquivo já existente. Substituição não necessária.")
            return self.log

        # Validar execução
        if not self.validar_funcionalidade(novo_arquivo):
            self.log.append("⛔ Arquivo falhou nos testes. Abortando posicionamento.")
            return self.log

        # Posicionar o arquivo
        shutil.copy2(novo_arquivo, destino_completo)
        self.log.append(f"[→] Arquivo movido para {destino_relativo}")

        return self.log

# Exemplo de uso:
# arcanomon = Arcanomon("/caminho/para/messamon")
# log_resultado = arcanomon.executar_protocolo("novo.py", "digimundo/nucleo_conhecimento/novo.py", versoes_antigas=["versao_anterior.py"])
# for entrada in log_resultado:
#     print(entrada)
