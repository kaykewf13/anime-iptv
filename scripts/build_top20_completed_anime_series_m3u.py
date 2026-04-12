import json
from pathlib import Path

INPUT_FILE = Path("output/anime_catalog.json")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "top20_completed_anime_series.m3u"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def is_completed_series(anime: dict) -> bool:
    status = (anime.get("status") or "").upper()
    anime_type = (anime.get("type") or "").upper()

    return (
        status in {"FINISHED", "COMPLETED"} and
        anime_type in {"TV", "ONA", "OVA"}
    )


def normalize_title(title: str) -> str:
    return " ".join((title or "").strip().split())


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def build_playlist():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    unique_by_title = {}

    for anime in catalog:
        if not is_completed_series(anime):
            continue

        title = normalize_title(anime.get("title", "Sem título"))
        if not title:
            continue

        episodes = safe_int(anime.get("episodes"), 0)
        current = unique_by_title.get(title)

        if current is None:
            unique_by_title[title] = anime
        else:
            current_episodes = safe_int(current.get("episodes"), 0)
            if episodes > current_episodes:
                unique_by_title[title] = anime

    top_20 = sorted(
        unique_by_title.values(),
        key=lambda anime: (
            -safe_int(anime.get("episodes"), 0),
            normalize_title(anime.get("title", "")).lower()
        )
    )[:20]

    lines = ["#EXTM3U"]
    total_items = 0

    for anime in top_20:
        title = normalize_title(anime.get("title", "Sem título"))
        year = anime.get("year", "N/A")
        episodes = safe_int(anime.get("episodes"), 0)
        anime_type = anime.get("type", "TV")
        logo = anime.get("picture", "")

        group_title = "🎬 Séries | Anime Concluído | Top 20 Mais Longos"
        display_title = f"{title} ({year}) - {episodes if episodes > 0 else '?'} eps [{anime_type}]"

        # Link neutro para o catálogo/site
        url = "https://kaykewf13.github.io/anime-iptv/"

        extinf = (
            f'#EXTINF:-1 '
            f'tvg-name="{title}" '
            f'tvg-logo="{logo}" '
            f'group-title="{group_title}",'
            f'{display_title}'
        )

        lines.append(extinf)
        lines.append(url)
        total_items += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("✅ Playlist Top 20 de animes concluídos gerada com sucesso!")
    print(f"📄 Arquivo: {OUTPUT_FILE}")
    print(f"🎬 Total de títulos incluídos: {total_items}")


if __name__ == "__main__":
    build_playlist()