from pathlib import Path
import shutil

OUTPUT_DIR = Path("output")
DOCS_DIR = Path("docs")

DOCS_DIR.mkdir(parents=True, exist_ok=True)

playlists = {
    "master_playlist.m3u": "master.m3u",
    "master_playlist_validated.m3u": "master_validated.m3u",
    "anime_channels.m3u": "anime.m3u",
    "series_channels.m3u": "series.m3u",
    "completed_anime_series.m3u": "completed.m3u",
    "completed_anime_series_grouped.m3u": "completed_grouped.m3u",
    "top20_completed_anime_series.m3u": "top20.m3u",
}

for src, dest in playlists.items():
    source_path = OUTPUT_DIR / src
    destination_path = DOCS_DIR / dest

    if source_path.exists():
        shutil.copy(source_path, destination_path)
        print(f"✅ Copiado: {dest}")
    else:
        print(f"⚠️ Arquivo não encontrado: {src}")

# garante que o Pages não tente processar com Jekyll
(DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")

print("🚀 Playlists publicadas na pasta docs para o GitHub Pages!")
