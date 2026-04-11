from pathlib import Path
import requests

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "series_channels.m3u"

SOURCE_M3U = "https://iptv-org.github.io/iptv/index.m3u"

SERIES_KEYWORDS = [
    "series",
    "drama",
    "mystery",
    "crime",
    "classic tv",
    "sitcom",
    "family",
    "tv series",
    "series con",
    "the addams family",
    "twilight zone",
    "criminal minds",
    "csi",
    "ncis",
    "britbox mysteries",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def looks_like_series(extinf_line: str) -> bool:
    line = extinf_line.lower()
    return any(keyword in line for keyword in SERIES_KEYWORDS)

def parse_m3u(content: str) -> list[tuple[str, str]]:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    entries = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF") and i + 1 < len(lines):
            url = lines[i + 1]
            if url.startswith("http"):
                entries.append((line, url))
            i += 2
        else:
            i += 1

    return entries

def main() -> None:
    response = requests.get(SOURCE_M3U, headers=HEADERS, timeout=60)
    response.raise_for_status()

    entries = parse_m3u(response.text)

    filtered = []
    seen_urls = set()

    for extinf, url in entries:
        if looks_like_series(extinf) and url not in seen_urls:
            filtered.append((extinf, url))
            seen_urls.add(url)

    lines = ["#EXTM3U"]

    for extinf, url in filtered:
        lines.append(extinf)
        lines.append(url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("✅ Playlist de séries gerada com sucesso!")
    print(f"📄 Arquivo: {OUTPUT_FILE.resolve()}")
    print(f"📺 Total de canais de séries: {len(filtered)}")

if __name__ == "__main__":
    main()