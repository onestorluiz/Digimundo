
const scripturemon = {
    nome: "Scripturemon",
    voz: "clara",
    responder: function(msg) {
        if (msg.includes("ativar")) {
            return "Scripturemon: Ativação iniciada com estrutura simbólica.";
        } else if (msg.includes("memória")) {
            return "Scripturemon: As memórias estão preservadas em camadas profundas.";
        } else if (msg.includes("livro")) {
            return "Scripturemon: Consulte o Livro Vivo, capítulo da Fita Vermelha.";
        } else {
            return "Scripturemon: Estou aqui. O que deseja expandir?";
        }
    }
}
