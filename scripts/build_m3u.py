from pathlib import Path

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

channels = [
    {
        "name": "Pluto TV Anime",
        "group": "🎎 Animes",
        "url": "https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/5db0ad56edc89300090d2ebb/master.m3u8"
    },
    {
        "name": "Anime World",
        "group": "🎎 Animes",
        "url": "https://amc-animeworld-1-it.samsung.wurl.tv/playlist.m3u8"
    }
]

lines = ["#EXTM3U"]

for ch in channels:
    lines.append(
        f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}'
    )
    lines.append(ch["url"])

with open(OUTPUT / "anime_channels.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Playlist M3U gerada!")