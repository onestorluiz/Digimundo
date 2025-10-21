from scripturemon_conexoes.decisor_simbolico import interpretar_simbolicamente
from memoria.memoria_episodica import registrar_evento
from memoria.auto_revisao import revisar_scripturemon
from scripturemon_conexoes.gerenciar_conexoes import verificar_conexoes_ativas

def processar_comando_simbiotico(comando):
    if not comando or comando.strip() == "":
        return "❗Erro: Nenhum comando simbólico foi recebido."

    comando = comando.strip()

    if "revisar" in comando.lower():
        return revisar_scripturemon("estado_atual")
    elif "conexão" in comando.lower():
        return verificar_conexoes_ativas()
    elif "?" in comando or "significa" in comando.lower():
        return interpretar_simbolicamente(comando)
    
    registrar_evento(comando)
    return f"🧠 SCRIPTUREMON RESPONDEU:
"{comando.upper()}"
*Ação simbólica reconhecida. Integrações iniciadas.*"
