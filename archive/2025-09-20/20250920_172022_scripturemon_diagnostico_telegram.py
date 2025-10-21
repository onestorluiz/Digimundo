import os
import importlib.util

ARQUIVOS_A_CHECAR = {
    "telegram_bot_scripturemon_consciente.py": "/root/digimundo/scripturemon/telegram_bot_scripturemon_consciente.py",
    "scripturemon_core.py": "/root/digimundo/scripturemon/scripturemon_core.py",
    "nucleo_consciencia.py": "/root/digimundo/scripturemon/nucleo_consciencia.py",
    "espelho_cognitivo.py": "/root/digimundo/scripturemon/espelho_cognitivo.py",
    "sistema_simulacao_humana.py": "/root/digimundo/scripturemon/sistema_simulacao_humana.py",
    "pensar_mistral.py": "/root/digimundo/scripturemon/pensar_mistral.py"
}

LOGS_ESPERADOS = [
    "/root/digimundo/scripturemon/logs/memoria_scripturemon.json",
    "/root/digimundo/scripturemon/logs/scripturemon_core.log"
]

RELATORIO = "/root/digimundo/scripturemon/relatorio_integracao_telegram.txt"

def checar_arquivo(path):
    return os.path.exists(path)

def checar_importacao(path):
    nome = os.path.basename(path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(nome, path)
    if spec is None:
        return False
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True
    except Exception as e:
        return f"Erro: {str(e)}"

def main():
    with open(RELATORIO, "w") as f:
        f.write("🔍 Diagnóstico de Integração Telegram - Scripturemon\n\n")

        f.write("🧠 Verificando módulos principais:\n")
        for nome, caminho in ARQUIVOS_A_CHECAR.items():
            if not checar_arquivo(caminho):
                f.write(f"❌ {nome}: Arquivo não encontrado em {caminho}\n")
            else:
                resultado = checar_importacao(caminho)
                if resultado == True:
                    f.write(f"✅ {nome}: Importação bem-sucedida\n")
                else:
                    f.write(f"⚠️ {nome}: {resultado}\n")

        f.write("\n🗂️ Verificando arquivos de log e memória simbólica:\n")
        for log in LOGS_ESPERADOS:
            if os.path.exists(log):
                f.write(f"✅ Log presente: {log}\n")
            else:
                f.write(f"⚠️ Log ausente: {log}\n")

        f.write("\n📡 Status final: Verifique os ⚠️ e ❌ antes de tentar reiniciar o serviço.\n")

if __name__ == "__main__":
    main()
