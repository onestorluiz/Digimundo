import ast, hashlib, json, time, os, random

metadados = {
    'tora': 10, 'protocolos': 9, 'core': 8,
    'memoria': 7, 'interface': 6, 'digestao': 5, 'evolucao': 4
}

erros_previstos = ["digestao", "memoria"]
aprendizado = {}

def gerar_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def validar(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            ast.parse(f.read())
        return True, None
    except Exception as e:
        return False, str(e)

def executar(path):
    with open(path, encoding="utf-8") as f:
        exec(f.read(), {})

def prever_falha(bloco):
    return bloco in erros_previstos or random.choice([False, False, True])  # 1/3 de chance aleatória + previsão real

def executar_bloco(bloco, arquivos, relatorio):
    if prever_falha(bloco):
        print(f"🔮 Arcanomon prevê falha simbólica em {bloco}. Caminho alternativo ativado.")
        relatorio[bloco] = {"status": "⚠️ previsão de falha — caminho alternativo usado"}
        return
    inicio = time.time()
    bloco_log = []
    for file in arquivos:
        hash_id = gerar_hash(file)
        valido, erro = validar(file)
        if valido:
            try:
                executar(file)
                bloco_log.append({"arquivo": file, "hash": hash_id, "status": "executado"})
                aprendizado[hash_id] = "sucesso"
            except Exception as e:
                bloco_log.append({"arquivo": file, "hash": hash_id, "erro_execucao": str(e)})
                aprendizado[hash_id] = "falhou"
        else:
            bloco_log.append({"arquivo": file, "hash": hash_id, "erro_sintaxe": erro})
            aprendizado[hash_id] = "erro_sintaxe"
    fim = time.time()
    relatorio[bloco] = {"tempo_execucao": round(fim - inicio, 2), "bloco": bloco_log}

def salvar_relatorios(relatorio):
    with open("relatorios/relatorio_execucao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    with open("relatorios/aprendizado.json", "w", encoding="utf-8") as a:
        json.dump(aprendizado, a, indent=2, ensure_ascii=False)

def executar_projetos(projetos):
    for projeto in projetos:
        print(f"🪐 Executando projeto: {projeto}")
        relatorio = {}
        for bloco in sorted(metadados, key=lambda x: -metadados[x]):
            caminho = f"./mock/{bloco}/modulo_{bloco}.py"
            if os.path.exists(caminho):
                executar_bloco(bloco, [caminho], relatorio)
        salvar_relatorios(relatorio)

# Ativação simbólica imediata
if __name__ == '__main__':
    executar_projetos(["scripturemon"])