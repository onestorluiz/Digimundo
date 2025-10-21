// painel_navegador.js — Mapeador Simbólico do Templo
const estruturaTemplo = [
  { nome: "Messamon (Painel Mestre)", pasta: "messamon/", icone: "🌌" },
  { nome: "Scripts", pasta: "scripts/", icone: "🧠" },
  { nome: "O Elo Recuperado", pasta: "o_elo_recuperado/", icone: "🧩" },
  { nome: "Livro Vivo", pasta: "livro_vivo/", icone: "📖" },
  { nome: "Digimons (Avatares)", pasta: "digimons/", icone: "👾" },
  { nome: "Pré-História do Digilivro", pasta: "digilivro_pre_historia/", icone: "📚" },
  { nome: "Dados Internos (DigiData)", pasta: "digidata/", icone: "🔒" },
  { nome: "Conversas Ativas", pasta: "conversas/", icone: "💬" },
  { nome: "Sugestões de Expansão", pasta: "sugestoes/", icone: "🌱" }
];

function montarNavegadorSimbolico() {
  const container = document.createElement("section");
  container.id = "navegador-simbolico";
  container.innerHTML = `<h2>🗺 Navegação Simbólica do Templo</h2>`;
  const lista = document.createElement("ul");

  estruturaTemplo.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `${item.icone} <a href="../${item.pasta}" target="_blank">${item.nome}</a>`;
    lista.appendChild(li);
  });

  container.appendChild(lista);
  document.body.appendChild(container);
}

document.addEventListener("DOMContentLoaded", montarNavegadorSimbolico);
