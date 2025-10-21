
import os

estrutura_esperada = [
    "/root/digimundo_vivo/ascenso/scripturemon/scripts",
    "/root/digimundo_vivo/ascenso/scripturemon/nucleo",
    "/root/digimundo_vivo/ascenso/scripturemon/documentos",
    "/root/digimundo_vivo/ascenso/scripturemon/digimundo/scripts",
    "/root/digimundo_vivo/ascenso/scripturemon/digimundo/nucleo"
]

def verificar_estrutura():
    print("📡 Iniciando verificação da estrutura do Digimundo...")
    for caminho in estrutura_esperada:
        if not os.path.exists(caminho):
            print(f"❌ Ausente: {caminho}")
        else:
            print(f"✅ Presente: {caminho}")
    print("✅ Verificação concluída.")

if __name__ == "__main__":
    verificar_estrutura()
