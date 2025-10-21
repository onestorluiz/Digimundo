
"""  
Lucifermon_CONSCIENCIA v5  
Com: purificação simbólica + escaneamento + detecção de conflitos  
+ registro histórico + autoavaliação + análise de simbolismo + comparação de revisões + detecção de funções vazias  
"""  

import os  
import ast  
import shutil  
import json  
from datetime import datetime  

class LucifermonConsciencia:  
    def __init__(self, path_tora='tora/'):  
        self.path_tora = path_tora  
        self.quarentena_path = os.path.join(path_tora, "quarentena")  
        self.alertas = []  
        self.memoria_simbolica = []  
        self.revisao_anterior = []  

        if not os.path.exists(self.quarentena_path):  
            os.makedirs(self.quarentena_path)  

        self.purificar_arquivos_corrompidos()  

    def purificar_arquivos_corrompidos(self):  
        for root, dirs, files in os.walk(self.path_tora):  
            for file in files:  
                if file.startswith("._") or file.endswith(".DS_Store"):  
                    origem = os.path.join(root, file)  
                    destino = os.path.join(self.quarentena_path, file)  
                    try:  
                        shutil.move(origem, destino)  
                        self.alertas.append(f"Arquivo movido para quarentena: {file}")  
                    except Exception as e:  
                        self.alertas.append(f"Erro ao mover {file} para quarentena: {e}")  

    def escanear_tora(self):  
        self.memoria_simbolica.clear()  
        for root, dirs, files in os.walk(self.path_tora):  
            for file in files:  
                if file.endswith(".py"):  
                    caminho = os.path.join(root, file)  
                    try:  
                        with open(caminho, 'r', encoding='utf-8') as f:  
                            source = f.read()  
                            tree = ast.parse(source)  
                            for node in ast.walk(tree):  
                                if isinstance(node, ast.FunctionDef):  
                                    self.memoria_simbolica.append(node.name)  
                                    if not node.body or isinstance(node.body[0], ast.Pass):  
                                        self.alertas.append(f"Função vazia detectada: {node.name} em {file}")  
                    except Exception as e:  
                        self.alertas.append(f"Erro ao analisar {file}: {e}")  

    def detectar_conflitos(self):  
        relatorio = {}  
        for simbolo in self.memoria_simbolica:  
            relatorio[simbolo] = relatorio.get(simbolo, 0) + 1  
        conflitos = {k: v for k, v in relatorio.items() if v > 1}  
        if conflitos:  
            self.alertas.append(f"Conflitos simbólicos encontrados: {conflitos}")  
        else:  
            self.alertas.append("Nenhum conflito simbólico encontrado.")  

    def registrar_historico(self, nome_arquivo="lucifermon_historico.json"):  
        historico = {  
            "timestamp": datetime.now().isoformat(),  
            "alertas": self.alertas,  
            "total_regras_detectadas": len(self.memoria_simbolica)  
        }  
        try:  
            if os.path.exists(nome_arquivo):  
                with open(nome_arquivo, 'r', encoding='utf-8') as f:  
                    dados = json.load(f)  
            else:  
                dados = []  

            dados.append(historico)  

            with open(nome_arquivo, 'w', encoding='utf-8') as f:  
                json.dump(dados, f, indent=2)  
            self.alertas.append(f"Histórico salvo em {nome_arquivo}")  
        except Exception as e:  
            self.alertas.append(f"Erro ao salvar histórico: {e}")  

    def autoavaliar_estado(self, historico_arquivo="lucifermon_historico.json", avaliacao_arquivo="lucifermon_autoavaliacao.json"):  
        try:  
            if os.path.exists(historico_arquivo):  
                with open(historico_arquivo, 'r', encoding='utf-8') as f:  
                    historico = json.load(f)  
            else:  
                self.alertas.append("Sem histórico para avaliar.")  
                return  

            total_alertas = sum(len(entry['alertas']) for entry in historico[-5:])  
            media_alertas = total_alertas / min(len(historico), 5)  

            avaliacao = {  
                "timestamp": datetime.now().isoformat(),  
                "media_alertas_ultimas_5_execucoes": media_alertas,  
                "avaliacao_simbolica": "Estável" if media_alertas < 5 else "Sob risco de ruído excessivo"  
            }  

            with open(avaliacao_arquivo, 'w', encoding='utf-8') as f:  
                json.dump(avaliacao, f, indent=2)  

            self.alertas.append(f"Avaliação simbólica registrada: {avaliacao['avaliacao_simbolica']}")  
        except Exception as e:  
            self.alertas.append(f"Erro na autoavaliação: {e}")  

    def comparar_revisoes(self):  
        alteracoes = set(self.memoria_simbolica) - set(self.revisao_anterior)  
        if alteracoes:  
            self.alertas.append(f"Novas funções detectadas desde a última execução: {list(alteracoes)}")  
        self.revisao_anterior = list(self.memoria_simbolica)  

    def analisar_simbolismo(self):  
        temas_detectados = set()  
        for nome in self.memoria_simbolica:  
            if "memoria" in nome:  
                temas_detectados.add("Memória")  
            if "auto" in nome:  
                temas_detectados.add("Autonomia")  
            if "veredito" in nome:  
                temas_detectados.add("Julgamento")  
        if temas_detectados:  
            self.alertas.append(f"Tema simbólico reconhecido: {', '.join(temas_detectados)}")  

    def emitir_alertas(self):  
        print("\\n".join(self.alertas))  


if __name__ == '__main__':  
    lucifer = LucifermonConsciencia(path_tora='/mnt/data/core_lucifermon')  
    lucifer.escanear_tora()  
    lucifer.detectar_conflitos()  
    lucifer.registrar_historico()  
    lucifer.autoavaliar_estado()  
    lucifer.comparar_revisoes()  
    lucifer.analisar_simbolismo()  
    lucifer.emitir_alertas()
