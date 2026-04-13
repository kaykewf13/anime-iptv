import json
from pathlib import Path

CATALOG_FILE = Path("output/anime_catalog.json")
SOURCES_FILE = Path("data/official_sources.json")
OUTPUT_FILE = Path("output/anime_catalog.json")

ALLOWED_DOMAINS = {
    "pluto.tv",
    "service-stitcher.clusters.pluto.tv",
    "tubitv.com",
    "youtube.com",
    "youtu.be",
    "www.youtube.com",
}

def normalize_title(title: str) -> str:
    return " ".join((title or "").strip().lower().split())

def is_allowed_url(url: str) -> bool:
    if not url:
        return False
    url = url.lower()
    return any(domain in url for domain in ALLOWED_DOMAINS)

def main():
    if not CATALOG_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CATALOG_FILE}")

    if not SOURCES_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {SOURCES_FILE}")

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = json.load(f)

    sources_by_title = {}

    for item in sources:
        if not item.get("approved", False):
            continue

        match_title = normalize_title(item.get("match_title", ""))
        if not match_title:
            continue

        if not is_allowed_url(item.get("watch_url", "")):
            continue

        source_entry = {
            "name": item.get("source_name"),
            "type": item.get("type"),
            "source_url": item.get("source_url"),
            "watch_url": item.get("watch_url"),
            "approved": True,
            "is_playable": True
        }

        sources_by_title.setdefault(match_title, []).append(source_entry)

    updated = 0

    for anime in catalog:
        title_key = normalize_title(anime.get("title", ""))
        anime_sources = sources_by_title.get(title_key, [])

        anime["sources"] = anime_sources
        anime["has_playable_source"] = len(anime_sources) > 0

        if anime_sources:
            updated += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print("✅ Fontes oficiais mescladas ao catálogo com sucesso!")
    print(f"📚 Títulos com fonte reproduzível: {updated}")

if __name__ == "__main__":
    main()