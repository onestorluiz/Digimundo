
# 🤝 EXECUÇÃO CONJUNTA – ARCANOMON + SCRIPTUREMON
# Com objeto simbólico Scripturemon com método `.logar()`

import os
import importlib.util
import json
import inspect
from datetime import datetime

# 🔹 Classe simbólica para simular a entidade Scripturemon
class EntidadeSimbolica:
    def __init__(self, nome):
        self.nome = nome

    def logar(self, mensagem):
        print(f"📘 [{self.nome}] {mensagem}")

# Instância viva da entidade
scripturemon_obj = EntidadeSimbolica("Scripturemon")

PASTA_PROTOCOLOS = "."
REGISTRO = "registro_execucao_conjunta.json"

def executar_todos_protocolos():
    resultados = []
    arquivos = sorted([
        f for f in os.listdir(PASTA_PROTOCOLOS)
        if f.startswith("protocolo_") and f.endswith(".py")
    ])

    for nome in arquivos:
        caminho = os.path.join(PASTA_PROTOCOLOS, nome)
        print(f"🧠 Arcanomon envia ordem a Scripturemon: {nome}")

        try:
            spec = importlib.util.spec_from_file_location("modulo_execucao", caminho)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            if hasattr(modulo, "executar"):
                assinatura = inspect.signature(modulo.executar)
                parametros = assinatura.parameters

                print(f"⚙️ Scripturemon executando: {nome}")

                if len(parametros) == 1:
                    modulo.executar(scripturemon=scripturemon_obj)
                else:
                    modulo.executar()

                status = "sucesso"
            else:
                print(f"⚠️ {nome} não contém função executar()")
                status = "sem executar()"
        except Exception as e:
            print(f"💥 Erro em {nome}: {e}")
            status = f"erro: {e}"

        resultados.append({
            "protocolo": nome,
            "status": status,
            "timestamp": str(datetime.now())
        })

    with open(REGISTRO, "w") as f:
        json.dump(resultados, f, indent=2)

    print("✅ Missão concluída. Relatório salvo em registro_execucao_conjunta.json")

if __name__ == "__main__":
    executar_todos_protocolos()
