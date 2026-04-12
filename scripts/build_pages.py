import json
from pathlib import Path

catalog_path = Path("output/anime_catalog.json")
categories_path = Path("output/categories")
manifest_path = Path("docs/site_manifest.json")

if not catalog_path.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {catalog_path}")

if not categories_path.exists():
    raise FileNotFoundError(f"Pasta não encontrada: {categories_path}")

with open(catalog_path, "r", encoding="utf-8") as f:
    catalog = json.load(f)

categories = []

for file in sorted(categories_path.glob("*.json")):
    with open(file, "r", encoding="utf-8") as f:
        items = json.load(f)

    slug = file.stem

    categories.append({
        "slug": slug,
        "name": slug.replace("_", " ").title(),
        "count": len(items),
        "file": f"https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/categories/{file.name}",
        "page": f"category.html?slug={slug}",
        "iptv": f"https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/m3u/{slug}.m3u",
        "sample": items[:12]
    })

recent = sorted(
    [item for item in catalog if item.get("year")],
    key=lambda x: x.get("year", 0),
    reverse=True
)[:24]

types_count = {}
for item in catalog:
    anime_type = item.get("type") or "Unknown"
    types_count[anime_type] = types_count.get(anime_type, 0) + 1

manifest = {
    "total_animes": len(catalog),
    "total_categories": len(categories),
    "categories": categories,
    "recent": recent,
    "types": types_count,
    "links": {
        "anime_m3u": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/anime_channels.m3u",
        "series_m3u": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/series_channels.m3u",
        "master_m3u": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/master_playlist.m3u",
        "master_m3u_validated": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/master_playlist_validated.m3u",
        "completed_anime_series_m3u": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/completed_anime_series.m3u",
        "grouped_completed_anime_series_m3u": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/completed_anime_series_grouped.m3u",
        "catalog_json": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/anime_catalog.json",
        "categories_base": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/categories/",
        "categories_m3u_base": "https://raw.githubusercontent.com/kaykewf13/anime-iptv/main/output/m3u/"
    }
}

manifest_path.parent.mkdir(parents=True, exist_ok=True)

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("✅ Manifesto do site gerado com sucesso!")
print(f"📊 Total de animes: {len(catalog)}")
print(f"📂 Total de categorias: {len(categories)}")