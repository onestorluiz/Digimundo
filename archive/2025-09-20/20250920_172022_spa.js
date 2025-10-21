
let allFilms = [];

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("film-container");
  const details = document.getElementById("film-details");
  const searchBox = document.getElementById("search-box");

  // Campos de detalhe
  const detailImg = document.getElementById("detail-img");
  const detailTitle = document.getElementById("detail-title");
  const detailDesc = document.getElementById("detail-description");
  const detailTrailer = document.getElementById("detail-trailer");
  const detailSite = document.getElementById("detail-site");
  const backButton = document.getElementById("back-button");

  fetch("films.json")
    .then(res => res.json())
    .then(data => {
      allFilms = data;
      route();
    });

  function renderCards(filter = "all", override = null) {
    container.innerHTML = "";
    const visible = override || allFilms.filter(f => filter === "all" || f.category === filter);
    visible.forEach(film => {
      const card = document.createElement("div");
      card.className = "film-card";
      
      let badgeClass = '';
      if (film.category === "Now Playing") badgeClass = 'status-now-playing';
      if (film.category === "Coming Soon") badgeClass = 'status-coming-soon';
      if (film.category === "Streaming") badgeClass = 'status-streaming';

      card.innerHTML = `
        <div class="badge ${badgeClass}">${film.category.toUpperCase()}</div>
        <img src="${film.image}" alt="${film.title}">
        <h2>${film.title}</h2>
        <p class="description">${film.description}</p>
      `;

      card.addEventListener("click", () => {
        location.hash = encodeURIComponent(film.title);
      });
      container.appendChild(card);
    });
  }

  document.querySelectorAll("nav button").forEach(btn => {
    btn.addEventListener("click", () => {
      const filter = btn.getAttribute("data-filter");
      renderCards(filter);
    });
  });

  searchBox.addEventListener("input", applyFilters);
  searchBox.addEventListener("input", e => {
    const term = e.target.value.toLowerCase();
    const filtered = allFilms.filter(f => f.title.toLowerCase().includes(term));
    renderCards(null, filtered);
  });

  function route() {
    const hash = decodeURIComponent(location.hash.slice(1));
    if (!hash) {
      container.style.display = "grid";
      details.style.display = "none";
      renderCards("all");
    } else {
      const film = allFilms.find(f => f.title === hash);
      if (film) {
        container.style.display = "none";
        details.style.display = "block";
        detailImg.src = film.image;
        detailTitle.textContent = film.title;
        detailDesc.textContent = film.description;
        detailTrailer.href = film.trailer;
        detailSite.href = film.site;
      }
    }
  }

  window.addEventListener("hashchange", route);
  backButton.addEventListener("click", () => {
    location.hash = "";
  });
});


function applyFilters() {
  const checked = [...document.querySelectorAll('#genre-filters input:checked')].map(cb => cb.value);
  const term = document.getElementById("search-box").value.toLowerCase();
  const filtered = allFilms.filter(f => {
    const matchGenres = checked.length === 0 || checked.every(g => f.genres.includes(g));
    const matchTitle = f.title.toLowerCase().includes(term);
    return matchGenres && matchTitle;
  });
  renderCards(null, filtered);
}

try {
  localStorage.setItem("allFilmsData", JSON.stringify(allFilms));
} catch (e) {
  console.warn("Storage failed", e);
}
