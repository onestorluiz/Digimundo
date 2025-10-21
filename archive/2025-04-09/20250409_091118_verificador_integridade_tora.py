
import os

def verificar_integridade_toras(tora_path="tora"):
    toras_detectadas = {}
    for root, _, files in os.walk(tora_path):
        for file in sorted(files):
            if file.startswith("tora_") and file.endswith(".py"):
                tipo = file.split("_")[1]
                numero = int(file.split("_")[2])
                if tipo not in toras_detectadas:
                    toras_detectadas[tipo] = []
                toras_detectadas[tipo].append(numero)

    for tipo, numeros in toras_detectadas.items():
        esperado = list(range(min(numeros), max(numeros) + 1))
        faltando = set(esperado) - set(numeros)
        if faltando:
            print(f"⚠️ Tora {tipo} faltando sequência: {sorted(faltando)}")
        else:
            print(f"✅ Tora {tipo} com sequência completa.")
