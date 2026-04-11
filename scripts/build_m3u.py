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

    categories.append({
        "name": file.stem.replace("_", " ").title(),
        "count": len(items),
        "file": f"../output/categories/{file.name}"
    })

manifest = {
    "total_animes": len(catalog),
    "total_categories": len(categories),
    "categories": categories
}

manifest_path.parent.mkdir(parents=True, exist_ok=True)

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("Manifesto do site gerado com sucesso!")
print(f"Total de animes: {len(catalog)}")
print(f"Total de categorias: {len(categories)}")