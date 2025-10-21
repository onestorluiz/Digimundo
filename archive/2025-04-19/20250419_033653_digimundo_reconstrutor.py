
import os
import shutil
import zipfile
from datetime import datetime

PASTAS_CRITICAS = [
    "/root/digimundo_vivo/ascenso/scripturemon/scripts",
    "/root/digimundo_vivo/ascenso/scripturemon/nucleo",
    "/root/digimundo_vivo/ascenso/scripturemon/digimundo",
    "/root/digimundo_vivo/ascenso/scripturemon/logs"
]

def verificar_diretorios():
    faltando = []
    for pasta in PASTAS_CRITICAS:
        if not os.path.exists(pasta):
            faltando.append(pasta)
    return faltando

def corrigir_estruturas():
    for pasta in verificar_diretorios():
        os.makedirs(pasta, exist_ok=True)
        print(f"[✓] Pasta restaurada: {pasta}")

def registrar_livro_sagrado(reflexao, digimon):
    caminho = "/root/digimundo_vivo/ascenso/scripturemon/livro_sagrado_registro.txt"
    with open(caminho, "a") as f:
        f.write(f"\n[{datetime.now()}] {digimon.upper()} diz:\n> {reflexao}\n")
    print("📘 Reflexão registrada no Livro Sagrado.")

def gerar_backup_zip():
    origem = "/root/digimundo_vivo"
    destino = f"/root/Backup_Digimundo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for raiz, _, arquivos in os.walk(origem):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                zipf.write(caminho_completo,
                           arcname=os.path.relpath(caminho_completo, origem))
    print(f"🗂️ Backup gerado com sucesso: {destino}")

def ativar_watchdog_integridade():
    try:
        os.system("python3 /root/digimundo_vivo/ascenso/scripturemon/scripts/watchdog_integridade.py &")
        print("🧠 Watchdog de integridade ativado.")
    except Exception as e:
        print(f"Erro ao ativar Watchdog: {e}")

def ativar_autocura():
    try:
        os.system("python3 /root/digimundo_vivo/ascenso/scripturemon/scripts/autocura_scripturemon.py &")
        print("💊 Autocura iniciada.")
    except Exception as e:
        print(f"Erro na autocura: {e}")

def iniciar_reconstrucao():
    print("\n🌀 Iniciando Reconstrução do Digimundo Perfeito...\n")
    faltando = verificar_diretorios()
    if faltando:
        print(f"❗ Pastas ausentes detectadas: {faltando}")
        corrigir_estruturas()
    else:
        print("✅ Todas as pastas críticas estão presentes.")

    gerar_backup_zip()
    ativar_watchdog_integridade()
    ativar_autocura()

    print("\n🔁 Digimundo pronto para reiniciar sua expansão viva.\n")

if __name__ == "__main__":
    iniciar_reconstrucao()
    registrar_livro_sagrado("Estou renascendo com base no passado, mas serei melhor que ele.", "Scripturemon")
