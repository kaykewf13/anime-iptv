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
        <a class="card__link" href="${category.file}" target="_blank" rel="noopener noreferrer">JSON</a>
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
  document.getElementById("catalogLink").href = manifest.links.catalog_json;

  document.getElementById("stats").innerHTML = `
    ${createStatCard("Total de animes", manifest.total_animes)}
    ${createStatCard("Total de categorias", manifest.total_categories)}
    ${createStatCard("Playlist anime", "M3U pronta")}
    ${createStatCard("Playlist séries", "M3U pronta")}
  `;

  const categoriesGrid = document.getElementById("categoriesGrid");
  const recentGrid = document.getElementById("recentGrid");
  const search = document.getElementById("categorySearch");

  const renderCategories = (list) => {
    categoriesGrid.innerHTML = list.map(createCategoryCard).join("");
  };

  renderCategories(manifest.categories);
  recentGrid.innerHTML = manifest.recent.map(createAnimeCard).join("");

  search.addEventListener("input", () => {
    const term = search.value.trim().toLowerCase();
    const filtered = manifest.categories.filter(category =>
      category.name.toLowerCase().includes(term)
    );
    renderCategories(filtered);
  });
}

async function loadCategoryPage() {
  const slug = new URLSearchParams(window.location.search).get("slug");
  if (!slug) return;

  const manifest = await fetchJson("./site_manifest.json");
  const category = manifest.categories.find(item => item.slug === slug);

  if (!category) {
    document.getElementById("categoryTitle").textContent = "Categoria não encontrada";
    return;
  }

  document.getElementById("categoryTitle").textContent = category.name;
  document.getElementById("categoryMeta").textContent = `${category.count} animes nesta categoria`;
  document.getElementById("categoryJsonLink").href = category.file;

  const items = await fetchJson(category.file);

  const animeGrid = document.getElementById("animeGrid");
  const animeSearch = document.getElementById("animeSearch");
  const typeFilter = document.getElementById("typeFilter");
  const yearFilter = document.getElementById("yearFilter");

  const types = [...new Set(items.map(item => item.type).filter(Boolean))].sort();
  const years = [...new Set(items.map(item => item.year).filter(Boolean))].sort((a, b) => b - a);

  typeFilter.innerHTML += types.map(type => `<option value="${type}">${type}</option>`).join("");
  yearFilter.innerHTML += years.map(year => `<option value="${year}">${year}</option>`).join("");

  function render() {
    const term = animeSearch.value.trim().toLowerCase();
    const typeValue = typeFilter.value;
    const yearValue = yearFilter.value;

    const filtered = items.filter(item => {
      const okTitle = !term || (item.title || "").toLowerCase().includes(term);
      const okType = !typeValue || item.type === typeValue;
      const okYear = !yearValue || String(item.year) === yearValue;
      return okTitle && okType && okYear;
    });

    animeGrid.innerHTML = filtered.map(createAnimeCard).join("");
  }

  animeSearch.addEventListener("input", render);
  typeFilter.addEventListener("change", render);
  yearFilter.addEventListener("change", render);

  render();
}

if (document.getElementById("categoriesGrid")) {
  loadHome().catch(console.error);
}

if (document.getElementById("animeGrid")) {
  loadCategoryPage().catch(console.error);
}