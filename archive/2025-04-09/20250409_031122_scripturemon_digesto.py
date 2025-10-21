import os
import json

class Scripturemon:
    def __init__(self, raiz):
        self.raiz = raiz
        self.digestao = os.path.join(raiz, 'digestao')
        self.digestao_concluida = os.path.join(raiz, 'digestao_concluida')
        self.digibiblia = os.path.join(raiz, 'digibiblia')
        os.makedirs(self.digestao, exist_ok=True)
        os.makedirs(self.digestao_concluida, exist_ok=True)
        os.makedirs(self.digibiblia, exist_ok=True)

    def digerir(self):
        for arquivo in os.listdir(self.digestao):
            caminho = os.path.join(self.digestao, arquivo)
            if not os.path.isfile(caminho):
                continue
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo = f.read()

                resultado = self._interpretar_conteudo(conteudo, arquivo)

                destino = os.path.join(self.digestao_concluida, f"concluido_{arquivo}")
                with open(destino, 'w', encoding='utf-8') as f_out:
                    f_out.write(resultado)

                os.remove(caminho)

            except Exception as e:
                print(f"Erro ao digerir {arquivo}: {e}")

    def _interpretar_conteudo(self, conteudo, nome):
        if nome.endswith(".json"):
            try:
                dados = json.loads(conteudo)
                return json.dumps(dados, indent=2)
            except:
                return f"Arquivo {nome} não é um JSON válido."
        elif nome.endswith(".txt"):
            return f"Conteúdo do texto '{nome}':\n\n{conteudo}"
        elif nome.endswith(".pdf"):
            return f"(PDF '{nome}' marcado para leitura futura por IA simbólica)"
        else:
            return f"(Tipo de arquivo '{nome}' não reconhecido diretamente. Script externo pode ser necessário.)"

if __name__ == '__main__':
    s = Scripturemon(os.path.dirname(__file__))
    s.digerir()
