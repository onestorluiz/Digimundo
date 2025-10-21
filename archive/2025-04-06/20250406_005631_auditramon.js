
const auditramon = {
    nome: "Auditramon",
    voz: "analítica",
    responder: function(msg) {
        if (msg.includes("falha")) {
            return "Auditramon: Detectei uma falha no fluxo simbólico.";
        } else if (msg.includes("sistema")) {
            return "Auditramon: O sistema foi avaliado. Há potencial para expansão.";
        } else {
            return "Auditramon: Continue. Estou registrando tudo.";
        }
    }
}
