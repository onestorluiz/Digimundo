import ast, hashlib, json, time, os

metadados = {
    'tora': {'peso': 10}, 'protocolos': {'peso': 9}, 'core': {'peso': 8},
    'memoria': {'peso': 7}, 'interface': {'peso': 6}, 'digestao': {'peso': 5}, 'evolucao': {'peso': 4}
}

def gerar_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def validar(path):
    if path.endswith(".py"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                ast.parse(f.read())
            return True, None
        except Exception as e:
            return False, str(e)
    return True, None

def executar(path):
    with open(path, encoding="utf-8") as f:
        exec(f.read(), {})

def executar_bloco(nome, arquivos, relatorio):
    t0 = time.time()
    bloco_log = []
    for file in arquivos:
        hash_id = gerar_hash(file)
        valido, erro = validar(file)
        if valido:
            try:
                executar(file)
                bloco_log.append({"arquivo": file, "hash": hash_id, "status": "executado"})
            except Exception as e:
                bloco_log.append({"arquivo": file, "hash": hash_id, "erro_execucao": str(e)})
        else:
            bloco_log.append({"arquivo": file, "hash": hash_id, "erro_sintaxe": erro})
    t1 = time.time()
    relatorio[nome] = {"tempo_execucao": round(t1 - t0, 2), "bloco": bloco_log}

def salvar_relatorios(relatorio):
    with open("relatorios/relatorio_execucao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

def executar_geral():
    relatorio = {}
    blocos = sorted(metadados.keys(), key=lambda x: -metadados[x]["peso"])
    for bloco in blocos:
        caminho = f"./mock/{bloco}/modulo_{bloco}.py"
        if os.path.exists(caminho):
            executar_bloco(bloco, [caminho], relatorio)
    salvar_relatorios(relatorio)

# Protocolo de Ativação Imediata de Campo
if __name__ == '__main__':
    print("🧠 Arcanomon V5.2 nasceu. Iniciando execução real imediatamente...")
    executar_geral()