async function loadManifest() {
  const response = await fetch("site_manifest.json");
  const data = await response.json();

  document.getElementById("total").innerText =
    `Total de Animes: ${data.total_animes}`;

  const container = document.getElementById("categories");

  data.categories.forEach(cat => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `
      <h3>${cat.name}</h3>
      <p>${cat.count} animes</p>
      <a href="category.html?file=${cat.file}&name=${cat.name}">
        Ver categoria
      </a>
    `;
    container.appendChild(div);
  });
}

async function loadCategory() {
  const params = new URLSearchParams(window.location.search);
  const file = params.get("file");
  const name = params.get("name");

  if (!file) return;

  document.getElementById("title").innerText = name;

  const response = await fetch(file);
  const animes = await response.json();

  const list = document.getElementById("anime-list");

  animes.slice(0, 50).forEach(anime => {
    const li = document.createElement("li");
    li.textContent = anime.title;
    list.appendChild(li);
  });
}

if (document.getElementById("categories")) {
  loadManifest();
}

if (document.getElementById("anime-list")) {
  loadCategory();
}