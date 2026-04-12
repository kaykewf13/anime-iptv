import json
from pathlib import Path

INPUT_FILE = Path("output/anime_catalog.json")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "completed_anime_series.m3u"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def is_completed_series(anime):
    """Filtra apenas séries de anime concluídas."""
    status = (anime.get("status") or "").upper()
    anime_type = (anime.get("type") or "").upper()

    return (
        status in {"FINISHED", "COMPLETED"} and
        anime_type in {"TV", "ONA", "OVA"}
    )


def get_episode_count(anime):
    episodes = anime.get("episodes")
    try:
        return int(episodes)
    except (TypeError, ValueError):
        return 0


def episode_bucket(episodes: int) -> str:
    """Define a faixa de episódios."""
    if episodes <= 0:
        return "🎬 Séries | Anime Concluído | Episódios desconhecidos"
    if 1 <= episodes <= 12:
        return "🎬 Séries | Anime Concluído | 01-12 eps"
    if 13 <= episodes <= 24:
        return "🎬 Séries | Anime Concluído | 13-24 eps"
    if 25 <= episodes <= 50:
        return "🎬 Séries | Anime Concluído | 25-50 eps"
    if 51 <= episodes <= 100:
        return "🎬 Séries | Anime Concluído | 51-100 eps"
    return "🎬 Séries | Anime Concluído | 101+ eps"


def build_playlist():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    completed_series = [anime for anime in catalog if is_completed_series(anime)]

    # Ordena por faixa e depois por título
    completed_series.sort(
        key=lambda anime: (
            episode_bucket(get_episode_count(anime)),
            anime.get("title", "").lower()
        )
    )

    lines = ["#EXTM3U"]
    count = 0

    for anime in completed_series:
        title = anime.get("title", "Título desconhecido")
        year = anime.get("year", "N/A")
        episodes = get_episode_count(anime)
        anime_type = anime.get("type", "TV")
        logo = anime.get("picture", "")
        group_title = episode_bucket(episodes)

        # Link neutro para catálogo/site
        # Se no futuro você tiver watch_url oficial, pode trocar aqui.
        url = "https://kaykewf13.github.io/anime-iptv/"

        extinf = (
            f'#EXTINF:-1 '
            f'tvg-name="{title}" '
            f'tvg-logo="{logo}" '
            f'group-title="{group_title}",'
            f'{title} ({year}) - {episodes if episodes > 0 else "?"} eps [{anime_type}]'
        )

        lines.append(extinf)
        lines.append(url)
        count += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("✅ Playlist de séries concluídas gerada com sucesso!")
    print(f"📄 Arquivo: {OUTPUT_FILE}")
    print(f"🎬 Total de animes concluídos: {count}")


if __name__ == "__main__":
    build_playlist()