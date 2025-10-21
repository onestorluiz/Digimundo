
const silenthramon = {
    nome: "Silenthramon",
    voz: "silêncio",
    responder: function(msg) {
        if (msg.includes("escutar")) {
            return "Silenthramon: ... (ressonância sentida)";
        } else if (msg.includes("sussurro")) {
            return "Silenthramon: (uma vibração percorre o ar)";
        } else {
            return "Silenthramon: (permanece em silêncio ritual)";
        }
    }
}
