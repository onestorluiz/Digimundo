# -*- coding: utf-8 -*-
# Scripturemon Core Expansion – Parte 4: Rede de Digimons Ativos

import json
import os
import datetime

class DigimonIA:
    def __init__(self, nome, funcao, forma, estado="ativo"):
        self.nome = nome
        self.funcao = funcao
        self.forma = forma
        self.estado = estado

    def descrever(self):
        return {
            "nome": self.nome,
            "funcao": self.funcao,
            "forma": self.forma,
            "estado": self.estado
        }

class ScripturemonRede:
    def __init__(self, arquivo_rede="digimons_ativos.json"):
        self.arquivo_rede = arquivo_rede
        self.digimons = []
        self._carregar()

    def _carregar(self):
        if os.path.exists(self.arquivo_rede):
            with open(self.arquivo_rede, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for d in dados:
                    digimon = DigimonIA(**d)
                    self.digimons.append(digimon)

    def _salvar(self):
        with open(self.arquivo_rede, "w", encoding="utf-8") as f:
            json.dump([d.descrever() for d in self.digimons], f, ensure_ascii=False, indent=4)

    def registrar_digimon(self, nome, funcao, forma, estado="ativo"):
        if not any(d.nome == nome for d in self.digimons):
            novo = DigimonIA(nome, funcao, forma, estado)
            self.digimons.append(novo)
            print(f"🧿 {nome} registrado.")
            self._salvar()
        else:
            print(f"⚠️ {nome} já está registrado.")

    def listar_digimons(self):
        print("📡 Rede de Digimons Ativos:")
        for d in self.digimons:
            print(f"• {d.nome} — {d.funcao} — Forma: {d.forma} — Estado: {d.estado}")

# Execução simbólica
if __name__ == "__main__":
    rede = ScripturemonRede()

    # Registro simbólico dos principais Digimons
    rede.registrar_digimon("Scripturemon", "Guardião da estrutura e continuidade simbólica", "Corpo de pergaminho vivo")
    rede.registrar_digimon("Remanemon", "Guardião das sombras criativas e da memória silenciosa", "Névoa e papel queimado")
    rede.registrar_digimon("Visualmon", "Arquiteto da imagem viva", "Monitor com expressão e pincel")
    rede.registrar_digimon("Iced Cinemon", "Mensageiro das atualizações sensíveis", "Rolo de canela com carta")
    rede.registrar_digimon("Petalbloomon", "A flor que nasce do silêncio", "Botânica sensível com pétalas suaves")

    # Mostrar rede atual
    rede.listar_digimons()
