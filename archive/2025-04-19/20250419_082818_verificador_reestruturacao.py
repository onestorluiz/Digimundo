import os
import datetime

CAMINHO_BASE = "/root/digimundo"
CAMINHO_ANTIGO = "/root/digimundo/original_backup"
LOG_PATH = "/root/digimundo/logs/verificacao_reestruturacao.log"
EXTENSOES = [".py", ".sh", ".json", ".txt", ".conf", ".md"]

def verificar_caminhos():
    encontrados = []

    for raiz, dirs, arquivos in os.walk(CAMINHO_BASE):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            if any(arquivo.endswith(ext) for ext in EXTENSOES):
                try:
                    with open(caminho_completo, "r", encoding="utf-8") as f:
                        conteudo = f.read()
                        if CAMINHO_ANTIGO in conteudo:
                            encontrados.append(caminho_completo)
                except Exception as e:
                    continue

    return encontrados

def gerar_log(lista):
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "w", encoding="utf-8") as log:
        log.write(f"[{agora}] 📜 Verificação da estrutura do templo:\n")
        if lista:
            for item in lista:
                log.write(f"❌ Caminho antigo encontrado em: {item}\n")
        else:
            log.write("✅ Nenhuma referência ao caminho antigo foi encontrada.\n")

if __name__ == "__main__":
    print("🧠 Executando verificação simbiótica...")
    resultado = verificar_caminhos()
    gerar_log(resultado)
    print(f"✅ Verificação concluída. Veja o relatório em {LOG_PATH}")
