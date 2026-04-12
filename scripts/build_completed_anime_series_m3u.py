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


def build_playlist():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    lines = ["#EXTM3U"]
    count = 0

    for anime in catalog:
        if not is_completed_series(anime):
            continue

        title = anime.get("title", "Título desconhecido")
        year = anime.get("year", "N/A")
        episodes = anime.get("episodes", "N/A")
        anime_type = anime.get("type", "TV")

        # Apenas metadados (VOD informativo)
        extinf = (
            f'#EXTINF:-1 tvg-name="{title}" '
            f'group-title="🎌 Anime Series | Completed",'
            f'{title} ({year}) - {episodes} eps [{anime_type}]'
        )

        # URL placeholder informativa
        url = "https://kaykewf13.github.io/anime-iptv/"

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