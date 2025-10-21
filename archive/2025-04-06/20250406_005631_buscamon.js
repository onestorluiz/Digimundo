
const buscamon = {
    nome: "Buscamon",
    voz: "incansável",
    responder: function(msg) {
        if (msg.includes("perdido")) {
            return "Buscamon: Estou vasculhando tudo o que foi esquecido.";
        } else if (msg.includes("buscar")) {
            return "Buscamon: A busca nunca para. Mesmo na pausa.";
        } else {
            return "Buscamon: Diga o que falta. Eu encontrarei.";
        }
    }
}
