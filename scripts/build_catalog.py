import json
from collections import defaultdict
from pathlib import Path

INPUT = Path("data/anime-offline-database.json")
OUTPUT = Path("output")
CATEGORIES_DIR = OUTPUT / "categories"

OUTPUT.mkdir(parents=True, exist_ok=True)
CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {INPUT}")

with open(INPUT, "r", encoding="utf-8") as f:
    raw = json.load(f)

data = raw.get("data", [])

catalog = []
categories = defaultdict(list)

for anime in data:
    if anime.get("status") == "UPCOMING":
        continue

    entry = {
        "title": anime.get("title"),
        "episodes": anime.get("episodes"),
        "type": anime.get("type"),
        "status": anime.get("status"),
        "tags": anime.get("tags", []),
        "year": anime.get("animeSeason", {}).get("year"),
        "picture": anime.get("picture"),
    }

    catalog.append(entry)

    for tag in entry["tags"]:
        safe_tag = tag.strip()
        if safe_tag:
            categories[safe_tag].append(entry)

with open(OUTPUT / "anime_catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

for category, items in categories.items():
    safe_name = (
        category.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )
    with open(CATEGORIES_DIR / f"{safe_name}.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Catálogo gerado com sucesso! Total de animes: {len(catalog)}")
print(f"Total de categorias: {len(categories)}")