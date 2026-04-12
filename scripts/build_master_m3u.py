from __future__ import annotations

from pathlib import Path
from typing import Iterable


OUTPUT_DIR = Path("output")
MASTER_FILE = OUTPUT_DIR / "master_playlist.m3u"

ANIME_MAIN = OUTPUT_DIR / "anime_channels.m3u"
SERIES_MAIN = OUTPUT_DIR / "series_channels.m3u"
ANIME_VOD = OUTPUT_DIR / "anime_vod.m3u"
SERIES_VOD = OUTPUT_DIR / "series_vod.m3u"

ANIME_CATEGORY_DIR = OUTPUT_DIR / "m3u"
SERIES_CATEGORY_DIR = OUTPUT_DIR / "series_m3u"
VOD_CATEGORY_DIR = OUTPUT_DIR / "vod_categories"


def normalize_title(title: str) -> str:
    """Normaliza o título para comparação de duplicidade."""
    return " ".join(title.strip().lower().split())


def extract_display_title(extinf_line: str) -> str:
    """
    Extrai o título exibido após a última vírgula da linha #EXTINF.
    Exemplo:
    #EXTINF:-1 group-title="Anime",Pluto TV Anime | Fantasy
    -> Pluto TV Anime | Fantasy
    """
    if "," not in extinf_line:
        return extinf_line.strip()
    return extinf_line.rsplit(",", 1)[-1].strip()


def parse_m3u_entries(file_path: Path) -> list[tuple[str, str]]:
    """
    Lê um arquivo M3U e retorna pares (#EXTINF, URL).
    Ignora comentários soltos e cabeçalhos #EXTM3U.
    """
    entries: list[tuple[str, str]] = []

    if not file_path.exists():
        print(f"⚠️ Arquivo não encontrado: {file_path}")
        return entries

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("#EXTINF") and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.startswith("http"):
                entries.append((line, next_line))
            i += 2
        else:
            i += 1

    return entries


def collect_entries_from_directory(directory: Path) -> list[tuple[str, str]]:
    """Coleta entradas de todos os arquivos .m3u de um diretório."""
    all_entries: list[tuple[str, str]] = []

    if not directory.exists():
        print(f"ℹ️ Pasta não encontrada, ignorando: {directory}")
        return all_entries

    for file_path in sorted(directory.glob("*.m3u")):
        print(f"📂 Incluindo playlist: {file_path}")
        all_entries.extend(parse_m3u_entries(file_path))

    return all_entries


def deduplicate_entries(entries: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    """
    Remove duplicados por:
    1. URL
    2. título visível do #EXTINF
    Mantém a primeira ocorrência.
    """
    unique_entries: list[tuple[str, str]] = []
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()

    for extinf, url in entries:
        title = normalize_title(extract_display_title(extinf))
        normalized_url = url.strip()

        if normalized_url in seen_urls:
            continue

        if title in seen_titles:
            continue

        unique_entries.append((extinf, url))
        seen_urls.add(normalized_url)
        seen_titles.add(title)

    return unique_entries


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    collected: list[tuple[str, str]] = []

    print("🔄 Gerando playlist mestra...")

    # Playlists principais
    collected.extend(parse_m3u_entries(ANIME_MAIN))
    collected.extend(parse_m3u_entries(SERIES_MAIN))
    collected.extend(parse_m3u_entries(ANIME_VOD))
    collected.extend(parse_m3u_entries(SERIES_VOD))

    # Playlists por diretório
    collected.extend(collect_entries_from_directory(ANIME_CATEGORY_DIR))
    collected.extend(collect_entries_from_directory(SERIES_CATEGORY_DIR))
    collected.extend(collect_entries_from_directory(VOD_CATEGORY_DIR))

    unique_entries = deduplicate_entries(collected)

    lines = ["#EXTM3U"]
    for extinf, url in unique_entries:
        lines.append(extinf)
        lines.append(url)

    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("✅ Playlist mestra gerada com sucesso!")
    print(f"📄 Arquivo: {MASTER_FILE.resolve()}")
    print(f"📥 Entradas coletadas: {len(collected)}")
    print(f"🧹 Entradas únicas: {len(unique_entries)}")
    print(f"♻️ Duplicados removidos: {len(collected) - len(unique_entries)}")


if __name__ == "__main__":
    main()