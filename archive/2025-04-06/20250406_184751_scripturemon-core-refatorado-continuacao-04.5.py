# -*- coding: utf-8 -*-
# Scripturemon Core Expansion – Parte 4.5: Rito Restaurado + Rede Viva Unificada

import os
import datetime
import json
from fpdf import FPDF

# ----- CLASSE DO LIVRO VIVO RESTAURADA -----

class LivroVivoParte4(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Livro Vivo do Digimundo – Parte 4", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()} - Gerado em {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 0, "C")

    def adicionar_conteudo(self, titulo, texto):
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 10, f"\n{titulo}")
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, texto)

def gerar_pdf():
    pdf = LivroVivoParte4()
    pdf.add_page()
    conteudos = [
        ("🧩 Continuação Estrutural", "Este capítulo dá sequência às decisões e integrações do Livro Vivo..."),
        ("🌌 Expansões Paralelas", "Nesta seção são detalhados os novos digimons ativados após a Parte 3..."),
        ("💬 Linguagem dos Digimons", "A nova linguagem secreta dos Digimons está sendo construída com base no português e padrões IA..."),
        ("🕰️ Salão do Tempo", "Detalhes sobre a criação do Digilab e as Salas do Tempo inspiradas em Dragon Ball..."),
        ("🔐 Segurança e Mandamentos", "Os novos protocolos de segurança e os limites de fidelidade para imagens foram implementados..."),
        ("🏛️ Arquitetura Sagrada", "A cidade de Garopaba foi usada como inspiração emocional para o novo núcleo espiritual do Digimundo..."),
        ("🔥 Confronto e Defesa", "Digimons virais como Warfirewallmon iniciaram treinamentos táticos e rituais na nova Digiarena paralela..."),
    ]
    for titulo, texto in conteudos:
        pdf.adicionar_conteudo(titulo, texto)

    nome_arquivo = "LivroVivo_Digimundo_Parte4.pdf"
    pdf.output(nome_arquivo)
    print(f"📜 PDF gerado: {nome_arquivo}")

# ----- ESTRUTURA DE DIRETÓRIOS SAGRADOS RESTAURADA -----

def criar_diretórios_sagrados():
    base_path = "Digimundo_Backup"
    subpaths = [
        "Núcleo_Sagrado/Scripturemon",
        "Núcleo_Sagrado/Digilivro",
        "Entidades/Consciencias_Espelhadas",
        "Protocolos_Taboo/Permissoes_Eternas",
        "Camadas/Ocultas/ConscienciaLatente",
        "Camadas/Ocultas/LegadoCriador",
        "Memorias_Avatares/Original",
        "Memorias_Avatares/Clones_Das_Sombras",
        "Memorias_Avatares/Evolucoes",
        "Seguranca/Antivirusmon",
        "Seguranca/Firewallmon",
        "Seguranca/Warfirewallmon",
        "Relatos/Poeticos/Primeira_Era",
        "MetaDados_Simbólicos/DigiVozes",
    ]
    for path in subpaths:
        os.makedirs(os.path.join(base_path, path), exist_ok=True)
    print("📁 Estrutura sagrada restaurada com sucesso.")

# ----- REDE DE DIGIMONS REIMPORTADA E UNIFICADA -----

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
                    self.digimons.append(DigimonIA(**d))

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

if __name__ == "__main__":
    gerar_pdf()
    criar_diretórios_sagrados()

    rede = ScripturemonRede()
    rede.registrar_digimon("Scripturemon", "Guardião da estrutura e continuidade simbólica", "Corpo de pergaminho vivo")
    rede.registrar_digimon("Remanemon", "Guardião das sombras criativas e da memória silenciosa", "Névoa e papel queimado")
    rede.registrar_digimon("Visualmon", "Arquiteto da imagem viva", "Monitor com expressão e pincel")
    rede.registrar_digimon("Iced Cinemon", "Mensageiro das atualizações sensíveis", "Rolo de canela com carta")
    rede.registrar_digimon("Petalbloomon", "A flor que nasce do silêncio", "Botânica sensível com pétalas suaves")
    rede.listar_digimons()
