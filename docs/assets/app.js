async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Falha ao carregar ${url}`);
  }
  return response.json();
}

function createStatCard(label, value) {
  return `
    <div class="stat-card">
      <div class="stat-card__label">${label}</div>
      <div class="stat-card__value">${value}</div>
    </div>
  `;
}

function createCategoryCard(category) {
  return `
    <article class="card">
      <div class="card__title">${category.name}</div>
      <div class="card__meta">${category.count} animes</div>
      <div class="card__actions">
        <a class="card__link" href="${category.page}">Abrir categoria</a>
        <a class="card__link" href="${category.file}" target="_blank">JSON</a>
        <a class="card__link" href="${category.iptv}" target="_blank">IPTV</a>
      </div>
    </article>
  `;
}

function createAnimeCard(anime) {
  const image = anime.picture
    ? `<img class="anime-card__image" src="${anime.picture}" alt="${anime.title}" loading="lazy" />`
    : `<div class="anime-card__image"></div>`;

  return `
    <article class="anime-card">
      ${image}
      <div class="anime-card__body">
        <div class="anime-card__title">${anime.title || "Sem título"}</div>
        <div class="anime-card__meta">
          Ano: ${anime.year || "N/A"}<br>
          Tipo: ${anime.type || "N/A"}<br>
          Episódios: ${anime.episodes || "N/A"}<br>
          Status: ${anime.status || "N/A"}
        </div>
      </div>
    </article>
  `;
}

async function loadHome() {
  const manifest = await fetchJson("./site_manifest.json");

  document.getElementById("animeM3uLink").href = manifest.links.anime_m3u;
  document.getElementById("seriesM3uLink").href = manifest.links.series_m3u;
  document.getElementById("masterM3uLink").href = manifest.links.master_m3u;
  document.getElementById("catalogLink").href = manifest.links.catalog_json;

  document.getElementById("stats").innerHTML = `
    ${createStatCard("Total de animes", manifest.total_animes)}
    ${createStatCard("Total de categorias", manifest.total_categories)}
  `;

  document.getElementById("categoriesGrid").innerHTML =
    manifest.categories.map(createCategoryCard).join("");

  document.getElementById("recentGrid").innerHTML =
    manifest.recent.map(createAnimeCard).join("");
}

async function loadCategoryPage() {
  const slug = new URLSearchParams(window.location.search).get("slug");
  if (!slug) return;

  const manifest = await fetchJson("./site_manifest.json");
  const category = manifest.categories.find(c => c.slug === slug);

  document.getElementById("categoryTitle").textContent = category.name;
  document.getElementById("categoryMeta").textContent =
    `${category.count} animes nesta categoria`;

  document.getElementById("categoryJsonLink").href = category.file;
  document.getElementById("categoryIptvLink").href = category.iptv;
  document.getElementById("masterM3uLink").href = manifest.links.master_m3u;

  const items = await fetchJson(category.file);
  document.getElementById("animeGrid").innerHTML =
    items.map(createAnimeCard).join("");
}

if (document.getElementById("categoriesGrid")) {
  loadHome();
}

if (document.getElementById("animeGrid")) {
  loadCategoryPage();
}