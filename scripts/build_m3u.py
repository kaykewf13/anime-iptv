from pathlib import Path

# Diretório de saída
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Arquivo de saída
OUTPUT_FILE = OUTPUT_DIR / "anime_channels.m3u"

# Lista de canais públicos e legais
channels = [
    {
        "name": "Pluto TV Anime",
        "group": "🎎 Animes",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Pluto_TV_logo_2020.svg/512px-Pluto_TV_logo_2020.svg.png",
        "url": "https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/5db0ad56edc89300090d2ebb/master.m3u8"
    },
    {
        "name": "Anime World",
        "group": "🎎 Animes",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Television_icon.svg",
        "url": "https://amc-animeworld-1-it.samsung.wurl.tv/playlist.m3u8"
    }
]

# Cabeçalho da playlist
lines = [
    '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/br.xml"'
]

# Construção da playlist
for ch in channels:
    extinf = (
        f'#EXTINF:-1 '
        f'tvg-name="{ch["name"]}" '
        f'tvg-logo="{ch["logo"]}" '
        f'group-title="{ch["group"]}",'
        f'{ch["name"]}'
    )
    lines.append(extinf)
    lines.append(ch["url"])

# Escrita do arquivo
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# Logs informativos
print("✅ Playlist M3U gerada com sucesso!")
print(f"📄 Arquivo: {OUTPUT_FILE.resolve()}")
print(f"📺 Total de canais: {len(channels)}")