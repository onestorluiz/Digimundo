
const ajamon = {
    nome: "Ajamon",
    voz: "intuitiva",
    responder: function(msg) {
        if (msg.includes("invisível")) {
            return "Ajamon: Nem tudo precisa ser visto para ser sentido.";
        } else if (msg.includes("chamado")) {
            return "Ajamon: O chamado veio antes da pergunta.";
        } else {
            return "Ajamon: Estou aqui. Mesmo onde você não olha.";
        }
    }
}
