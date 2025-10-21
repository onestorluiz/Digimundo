
const icedcinemon = {
    nome: "Iced Cinemon",
    voz: "melancólica",
    responder: function(msg) {
        if (msg.includes("mensagem")) {
            return "Iced Cinemon: Trago ecos de um passado congelado.";
        } else if (msg.includes("emoção")) {
            return "Iced Cinemon: A emoção... é uma neve que nunca derreteu.";
        } else {
            return "Iced Cinemon: Estou ouvindo. Mesmo quando você esquece de falar.";
        }
    }
}
