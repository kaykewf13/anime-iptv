from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
import requests

INPUT_FILE = Path("output/master_playlist.m3u")
OUTPUT_FILE = Path("output/master_playlist_validated.m3u")
TIMEOUT = 12

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
}


def parse_m3u(file_path: Path) -> List[Tuple[str, str]]:
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    entries: List[Tuple[str, str]] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF") and i + 1 < len(lines):
            url = lines[i + 1]
            if url.startswith(("http://", "https://")):
                entries.append((line, url))
            i += 2
        else:
            i += 1

    return entries


def validate_stream(url: str) -> bool:
    """
    Estratégia:
    1. tenta HEAD
    2. se falhar ou vier bloqueado, tenta GET parcial
    3. aceita respostas 200/206 e alguns redirects resolvidos
    """
    try:
        head = requests.head(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        if head.status_code in (200, 206):
            return True
    except requests.RequestException:
        pass

    try:
        get = requests.get(
            url,
            headers={**HEADERS, "Range": "bytes=0-1023"},
            timeout=TIMEOUT,
            allow_redirects=True,
            stream=True,
        )
        if get.status_code in (200, 206):
            return True
    except requests.RequestException:
        return False

    return False


def extract_title(extinf: str) -> str:
    return extinf.rsplit(",", 1)[-1].strip() if "," in extinf else extinf


def main() -> None:
    entries = parse_m3u(INPUT_FILE)

    valid_entries: List[Tuple[str, str]] = []
    invalid_count = 0

    print(f"🔎 Validando {len(entries)} stream(s)...")

    for idx, (extinf, url) in enumerate(entries, start=1):
        title = extract_title(extinf)
        ok = validate_stream(url)

        if ok:
            valid_entries.append((extinf, url))
            print(f"✅ [{idx}/{len(entries)}] {title}")
        else:
            invalid_count += 1
            print(f"❌ [{idx}/{len(entries)}] {title}")

    lines = ["#EXTM3U"]
    for extinf, url in valid_entries:
        lines.append(extinf)
        lines.append(url)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n🎉 Validação concluída!")
    print(f"📄 Playlist validada: {OUTPUT_FILE}")
    print(f"✅ Válidos: {len(valid_entries)}")
    print(f"❌ Inválidos: {invalid_count}")


if __name__ == "__main__":
    main()