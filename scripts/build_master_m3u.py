from pathlib import Path

OUTPUT_DIR = Path("output")
CATEGORY_M3U_DIR = OUTPUT_DIR / "m3u"
MASTER_FILE = OUTPUT_DIR / "master_playlist.m3u"

ANIME_MAIN = OUTPUT_DIR / "anime_channels.m3u"
SERIES_MAIN = OUTPUT_DIR / "series_channels.m3u"

def append_playlist(lines, file_path):
    """Adiciona o conteúdo de uma playlist à lista principal."""
    if not file_path.exists():
        print(f"⚠️ Arquivo não encontrado: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and line != "#EXTM3U":
                lines.append(line)

def main():
    lines = ["#EXTM3U"]

    print("🔄 Gerando playlist mestra...")

    # Adiciona playlists principais
    append_playlist(lines, ANIME_MAIN)
    append_playlist(lines, SERIES_MAIN)

    # Adiciona playlists por categoria
    if CATEGORY_M3U_DIR.exists():
        for m3u_file in sorted(CATEGORY_M3U_DIR.glob("*.m3u")):
            print(f"📺 Incluindo categoria: {m3u_file.name}")
            append_playlist(lines, m3u_file)

    # Remove duplicatas preservando a ordem
    unique_lines = []
    seen = set()
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    # Salva o arquivo final
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_lines) + "\n")

    print("✅ Playlist mestra gerada com sucesso!")
    print(f"📄 Arquivo: {MASTER_FILE.resolve()}")

if __name__ == "__main__":
    main()