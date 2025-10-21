# orquestrador_ativo.py
import time
import random
from datetime import datetime

def verificar_conexao_simulada():
    estado = random.choice(["OK", "FALHA", "LENTO", "INTERMITENTE"])
    return f"[{datetime.utcnow().isoformat()}] Simulação de acesso externo: {estado}"

def ciclo_orquestrador():
    print("Iniciando ciclo perpétuo de verificação simbólica...")
    for i in range(10):  # 10 verificações consecutivas
        resultado = verificar_conexao_simulada()
        print(resultado)
        time.sleep(1)  # simbolicamente espaçado

if __name__ == '__main__':
    ciclo_orquestrador()
