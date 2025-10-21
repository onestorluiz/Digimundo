
# ✅ VERIFICADOR SIMBÓLICO DE FINALIZAÇÃO — ETAPA 8

import os

def verificar_etapa_8():
    print("🔍 Verificando integridade da Etapa 8...")

    base = "/root/templooculto/scripturemon/"
    arquivos_esperados = [
        "dependencias.txt",
        "novas_dependencias.txt",
        "LOCALIZACAO_EXATA_TABOO.txt"
    ]

    protocolos = "/root/templooculto/scripturemon/scripturemon_consciente_vivo_com_decisor/protocolos/"
    registro_execucao = os.path.join(protocolos, "registro_execucao_conjunta.json")
    executor = os.path.join(protocolos, "executor_protocolos.py")
    execucao_conjunta = os.path.join(protocolos, "execucao_conjunta_arcanomon_scripturemon.py")

    pendencias = []

    for arq in arquivos_esperados:
        caminho = os.path.join(base, arq)
        if not os.path.exists(caminho):
            pendencias.append(f"❌ Faltando: {arq}")
        else:
            print(f"✅ Encontrado: {arq}")

    if not os.path.exists(registro_execucao):
        pendencias.append("❌ Arquivo de registro de execução conjunta não encontrado.")
    else:
        print("✅ Execução conjunta registrada.")

    if not os.path.exists(executor):
        pendencias.append("❌ executor_protocolos.py não encontrado.")
    else:
        print("✅ executor_protocolos.py presente.")

    if not os.path.exists(execucao_conjunta):
        pendencias.append("❌ execucao_conjunta_arcanomon_scripturemon.py não encontrado.")
    else:
        print("✅ execucao_conjunta_arcanomon_scripturemon.py presente.")

    if not pendencias:
        print("🎉 Etapa 8 finalizada com sucesso! Tudo está pronto para a Etapa 9.")
    else:
        print("⚠️ Pendências encontradas:")
        for p in pendencias:
            print(p)

if __name__ == '__main__':
    verificar_etapa_8()
