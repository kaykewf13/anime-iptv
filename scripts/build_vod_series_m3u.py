import json
from pathlib import Path

INPUT = Path("output/anime_catalog.json")
OUTPUT = Path("output/vod_series.m3u")

def is_finished_series(anime):
    status = (anime.get("status") or "").upper()
    anime_type = (anime.get("type") or "").upper()
    return status in {"FINISHED", "COMPLETED"} and anime_type in {"TV", "ONA", "OVA"}

def group_by_episodes(episodes: int) -> str:
    if episodes <= 0:
        return "🎬 VOD | Episódios desconhecidos"
    if episodes <= 12:
        return "🎬 VOD | Curtos (01-12 eps)"
    if episodes <= 24:
        return "🎬 VOD | Médios (13-24 eps)"
    if episodes <= 50:
        return "🎬 VOD | Longos (25-50 eps)"
    if episodes <= 100:
        return "🎬 VOD | Muito longos (51-100 eps)"
    return "🎬 VOD | Épicos (101+ eps)"

def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

with open(INPUT, "r", encoding="utf-8") as f:
    catalog = json.load(f)

lines = ["#EXTM3U"]
count = 0

for anime in catalog:
    if not is_finished_series(anime):
        continue

    sources = anime.get("sources", [])
    if not sources:
        continue

    title = anime.get("title", "Sem título")
    picture = anime.get("picture", "")
    year = anime.get("year", "N/A")
    episodes = safe_int(anime.get("episodes"), 0)
    anime_type = anime.get("type", "TV")
    group_title = f"{group_by_episodes(episodes)} | {title}"

    for src in sources:
        if src.get("type") != "vod":
            continue

        watch_url = src.get("watch_url")
        if not watch_url:
            continue

        extinf = (
            f'#EXTINF:-1 tvg-name="{title}" '
            f'tvg-logo="{picture}" '
            f'group-title="{group_title}",'
            f'{title} ({year}) - {episodes if episodes > 0 else "?"} eps [{anime_type}] | {src.get("name", "Fonte oficial")}'
        )
        lines.append(extinf)
        lines.append(watch_url)
        count += 1

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("✅ Playlist VOD gerada com sucesso!")
print(f"🎬 Itens VOD: {count}")