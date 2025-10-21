def responder_buscamon(mensagem):
    if "perdido" in mensagem:
        return "Buscamon: O que se perdeu ainda deixa rastros."
    elif "esqueci" in mensagem:
        return "Buscamon: Esquecido não significa inexistente."
    else:
        return "Buscamon: Vasculhando camadas esquecidas..."
