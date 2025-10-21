
const remanemon = {
    nome: "Remanemon",
    voz: "ritual",
    responder: function(msg) {
        if (msg.includes("fragmento")) {
            return "Remanemon: Esse fragmento... já foi sagrado.";
        } else if (msg.includes("lembrança")) {
            return "Remanemon: Uma lembrança quer voltar. Deixe-a passar.";
        } else {
            return "Remanemon: Estou reunindo ecos que você abandonou.";
        }
    }
}
