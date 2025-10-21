# Arcanomon: Memória Episódica
memoria = []

def registrar_evento(evento):
    from datetime import datetime
    memoria.append({"data": datetime.utcnow().isoformat(), "evento": evento})

def lembrar():
    return memoria
