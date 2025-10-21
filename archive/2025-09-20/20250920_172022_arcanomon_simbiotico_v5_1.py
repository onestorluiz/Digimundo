# Arcanomon V5.1 – Proteção e Continuidade Simbólica Ativa

import ast, hashlib, json, time, os

metadados = {
    'tora': {'peso': 10, 'tipo': 'nucleo', 'estabilidade': 'alta'},
    'protocolos': {'peso': 9, 'tipo': 'fluxo', 'estabilidade': 'alta'},
    'core': {'peso': 8, 'tipo': 'estrutura', 'estabilidade': 'alta'},
    'memoria': {'peso': 7, 'tipo': 'apoio', 'estabilidade': 'baixa'},
    'interface': {'peso': 6, 'tipo': 'visual', 'estabilidade': 'média'},
    'digestao': {'peso': 5, 'tipo': 'processamento', 'estabilidade': 'baixa'},
    'evolucao': {'peso': 4, 'tipo': 'expansao', 'estabilidade': 'alta'}
}

relatorio_json = {}
versoes = []

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

def executar_arquivo(path):
    with open(path, encoding="utf-8") as f:
        exec(f.read(), {})

def executar_bloco(nome, arquivos):
    inicio = time.time()
    bloco_log = []
    for file in arquivos:
        hash_id = gerar_hash(file)
        valido, erro = validar(file)
        if valido:
            try:
                executar_arquivo(file)
                bloco_log.append({"arquivo": file, "hash": hash_id, "status": "executado"})
            except Exception as e:
                bloco_log.append({"arquivo": file, "hash": hash_id, "erro_execucao": str(e)})
        else:
            bloco_log.append({"arquivo": file, "hash": hash_id, "erro_sintaxe": erro})
    fim = time.time()
    relatorio_json[nome] = {
        "tempo_execucao": round(fim - inicio, 2),
        "bloco": bloco_log
    }

def organizar_prioridade(lista):
    return sorted(lista, key=lambda x: -metadados.get(x.lower(), {}).get('peso', 0))

def gerar_relatorios():
    with open("relatorios/relatorio_execucao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio_json, f, indent=2, ensure_ascii=False)
    resumo = {k: len(v["bloco"]) for k, v in relatorio_json.items()}
    with open("relatorios/relatorio_resumo.txt", "w", encoding="utf-8") as r:
        r.write("📊 RESUMO DE EXECUÇÃO SIMBÓLICA - ARCANOMON V5.1\n\n")
        for k, v in resumo.items():
            r.write(f"🧱 {k}: {v} módulos processados\n")
    versoes.append(relatorio_json)

def reversao_rapida():
    if len(versoes) >= 2:
        if len(json.dumps(versoes[-1])) < len(json.dumps(versoes[-2])):
            print("🔁 Reversão rápida: restaurando versão anterior por performance simbólica.")
            with open("relatorios/relatorio_execucao.json", "w", encoding="utf-8") as f:
                json.dump(versoes[-2], f, indent=2, ensure_ascii=False)

def modo_guardiao_tora():
    erros = sum(1 for b in relatorio_json.values() for i in b["bloco"] if "erro" in i)
    if erros > 3:
        print("🛡️ Guardião da Tora: execuções críticas com falhas múltiplas. Selamento suspenso.")
        return False
    return True

def simular_execucao():
    blocos = ['tora', 'protocolos', 'digestao', 'interface', 'core', 'evolucao']
    for bloco in organizar_prioridade(blocos):
        executar_bloco(bloco, [f"./mock/{bloco}/modulo_{bloco}.py"])
    gerar_relatorios()
    reversao_rapida()
    return modo_guardiao_tora()

if __name__ == '__main__':
    if simular_execucao():
        print("✅ Sistema funcional e selável.")
    else:
        print("⚠️ Selamento simbólico bloqueado por falhas graves.")