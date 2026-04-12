import requests
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "series_channels.m3u"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fonte pública confiável
SOURCE_M3U = "https://iptv-org.github.io/iptv/index.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Palavras-chave para identificar canais de séries
SERIES_KEYWORDS = [
    "series", "drama", "sitcom", "tv series", "classic tv",
    "crime", "mystery", "family", "comedy", "thriller",
    "detective", "action series", "britbox", "csi", "ncis",
    "law & order", "friends", "doctor who", "sherlock",
    "the twilight zone"
]


def is_series_channel(extinf_line: str) -> bool:
    """Verifica se o canal é de séries."""
    line = extinf_line.lower()
    return any(keyword in line for keyword in SERIES_KEYWORDS)


def parse_m3u(content: str):
    """Extrai entradas EXTINF e URLs."""
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    entries = []

    i = 0
    while i < len(lines):
        if lines[i].startswith("#EXTINF") and i + 1 < len(lines):
            url = lines[i + 1]
            if url.startswith("http"):
                entries.append((lines[i], url))
            i += 2
        else:
            i += 1

    return entries


def remove_duplicates(entries):
    """Remove duplicados com base em URL e título."""
    unique = []
    seen_urls = set()
    seen_titles = set()

    for extinf, url in entries:
        title = extinf.split(",")[-1].strip().lower()

        if url in seen_urls:
            continue
        if title in seen_titles:
            continue

        seen_urls.add(url)
        seen_titles.add(title)
        unique.append((extinf, url))

    return unique


def main():
    print("📡 Baixando lista pública de IPTV...")
    response = requests.get(SOURCE_M3U, headers=HEADERS, timeout=60)
    response.raise_for_status()

    entries = parse_m3u(response.text)

    print("🔍 Filtrando canais de séries...")
    filtered = [
        (extinf, url)
        for extinf, url in entries
        if is_series_channel(extinf)
    ]

    unique_entries = remove_duplicates(filtered)

    lines = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/br.xml"'
    ]

    for extinf, url in unique_entries:
        lines.append(extinf)
        lines.append(url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("✅ Playlist de séries gerada com sucesso!")
    print(f"📄 Arquivo: {OUTPUT_FILE}")
    print(f"📺 Total de canais: {len(unique_entries)}")


if __name__ == "__main__":
    main()