async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Falha ao carregar ${url}`);
  }
  return response.json();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
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
        <a class="card__link" href="${category.iptv}" target="_blank" rel="noopener noreferrer">Assistir via IPTV</a>
      </div>
    </article>
  `;
}

function createAnimeCard(anime) {
  const image = anime.picture
    ? `<img class="anime-card__image" src="${anime.picture}" alt="${escapeHtml(anime.title || "Sem título")}" loading="lazy" />`
    : `<div class="anime-card__image"></div>`;

  const canWatch = Boolean(anime.watch_url);
  const watchButton = canWatch
    ? `<button class="button button--small js-watch-btn"
         type="button"
         data-title="${escapeHtml(anime.title || "Sem título")}"
         data-watch-url="${escapeHtml(anime.watch_url)}"
         data-watch-type="${escapeHtml(anime.watch_type || "video")}"
         data-source-name="${escapeHtml(anime.source_name || "Fonte oficial")}"
       >▶ Assistir</button>`
    : "";

  const externalButton = anime.source_url
    ? `<a class="button button--ghost button--small" href="${anime.source_url}" target="_blank" rel="noopener noreferrer">Fonte oficial</a>`
    : "";

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
        <div class="anime-card__actions">
          ${watchButton}
          ${externalButton}
        </div>
      </div>
    </article>
  `;
}

function isDirectVideoUrl(url) {
  return /\.(mp4|webm|ogg|m3u8)(\?.*)?$/i.test(url);
}

function isEmbeddableUrl(url) {
  return /youtube\.com\/embed|player\.vimeo\.com|archive\.org\/embed/i.test(url);
}

function closePlayer() {
  const panel = document.getElementById("playerPanel");
  const video = document.getElementById("videoPlayer");
  const iframe = document.getElementById("iframePlayer");
  const info = document.getElementById("playerInfo");

  if (!panel || !video || !iframe || !info) return;

  video.pause();
  video.removeAttribute("src");
  video.load();
  iframe.src = "";
  video.classList.add("hidden");
  iframe.classList.add("hidden");
  panel.classList.add("hidden");
  info.innerHTML = "";
}

function openPlayer({ title, url, type, sourceName }) {
  const panel = document.getElementById("playerPanel");
  const video = document.getElementById("videoPlayer");
  const iframe = document.getElementById("iframePlayer");
  const info = document.getElementById("playerInfo");

  if (!panel || !video || !iframe || !info) return;

  closePlayer();

  info.innerHTML = `
    <strong>${title}</strong><br>
    Reprodução via: ${sourceName}
  `;

  if (type === "iframe" || isEmbeddableUrl(url)) {
    iframe.src = url;
    iframe.classList.remove("hidden");
  } else if (type === "video" || isDirectVideoUrl(url)) {
    video.src = url;
    video.classList.remove("hidden");
  } else {
    info.innerHTML = `
      <strong>${title}</strong><br>
      Esta fonte não pode ser reproduzida diretamente no player embutido.<br>
      <a href="${url}" target="_blank" rel="noopener noreferrer">Abrir fonte oficial</a>
    `;
  }

  panel.classList.remove("hidden");
  panel.scrollIntoView({ behavior: "smooth", block: "start" });
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
  document.getElementById("categoryIptvLink").href = category.iptv;
  document.getElementById("masterM3uLink").href = manifest.links.master_m3u;

  const items = await fetchJson(category.file);

  const animeGrid = document.getElementById("animeGrid");
  const animeSearch = document.getElementById("animeSearch");
  const typeFilter = document.getElementById("typeFilter");
  const yearFilter = document.getElementById("yearFilter");
  const resultsCount = document.getElementById("resultsCount");
  const closePlayerBtn = document.getElementById("closePlayerBtn");

  if (closePlayerBtn) {
    closePlayerBtn.addEventListener("click", closePlayer);
  }

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
    resultsCount.textContent = `${filtered.length} resultado(s)`;

    animeGrid.querySelectorAll(".js-watch-btn").forEach((button) => {
      button.addEventListener("click", () => {
        openPlayer({
          title: button.dataset.title,
          url: button.dataset.watchUrl,
          type: button.dataset.watchType,
          sourceName: button.dataset.sourceName
        });
      });
    });
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