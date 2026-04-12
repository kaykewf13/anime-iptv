import json
from pathlib import Path

CATEGORIES_DIR = Path("output/categories")
M3U_DIR = Path("output/m3u")

M3U_DIR.mkdir(parents=True, exist_ok=True)

# Fontes públicas/oficiais para anime
ANIME_CHANNELS = [
    {
        "name": "Pluto TV Anime",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Pluto_TV_logo_2020.svg/512px-Pluto_TV_logo_2020.svg.png",
        "url": "https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/5db0ad56edc89300090d2ebb/master.m3u8",
    },
    {
        "name": "Anime World",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Television_icon.svg",
        "url": "https://amc-animeworld-1-it.samsung.wurl.tv/playlist.m3u8",
    },
]

# Mapeamento simples de categoria -> canais
# Você pode expandir isso depois, se quiser tratar algumas categorias de forma diferente.
def get_channels_for_category(category_slug: str) -> list[dict]:
    # Hoje retorna os mesmos canais oficiais de anime para qualquer categoria.
    # Mantido assim para garantir consistência e links válidos.
    return ANIME_CHANNELS


def category_title_from_slug(slug: str) -> str:
    return slug.replace("_", " ").title()


def main() -> None:
    if not CATEGORIES_DIR.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {CATEGORIES_DIR}")

    category_files = sorted(CATEGORIES_DIR.glob("*.json"))

    if not category_files:
        raise FileNotFoundError("Nenhum arquivo de categoria encontrado em output/categories")

    total_created = 0

    for category_file in category_files:
        slug = category_file.stem
        category_name = category_title_from_slug(slug)

        with open(category_file, "r", encoding="utf-8") as f:
            items = json.load(f)

        channels = get_channels_for_category(slug)

        lines = ['#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/br.xml"']

        # Cabeçalho comentado com alguns títulos da categoria
        sample_titles = [item.get("title", "") for item in items[:10] if item.get("title")]
        if sample_titles:
            lines.append(f"# Categoria: {category_name}")
            lines.append(f"# Exemplos: {', '.join(sample_titles)}")

        for channel in channels:
            extinf = (
                f'#EXTINF:-1 '
                f'tvg-name="{channel["name"]}" '
                f'tvg-logo="{channel["logo"]}" '
                f'group-title="🎎 {category_name}",'
                f'{channel["name"]} | {category_name}'
            )
            lines.append(extinf)
            lines.append(channel["url"])

        output_file = M3U_DIR / f"{slug}.m3u"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        print(f"✅ Playlist criada: {output_file}")
        total_created += 1

    print(f"🎉 Playlists M3U por categoria geradas com sucesso! Total: {total_created}")


if __name__ == "__main__":
    main()