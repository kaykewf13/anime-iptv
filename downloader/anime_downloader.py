"""
Anime Downloader — Inspecionar → Confirmar → Baixar
Uso: python anime_downloader.py
Dependências: pip install requests beautifulsoup4
"""

from bs4 import BeautifulSoup
from urllib.parse import unquote, urljoin
import os, time, sys, requests

# ─── CONFIG ───────────────────────────────────────────────
URL = "https://www.animeout.xyz/hanasaku-iroha-complete-batchepisode-1-26-720p90mb/"

FILTROS = ["nimbus.animeout.com", ".mkv", ".mp4", ".avi", ".zip", ".rar"]

# Filtro de qualidade: "720p", "1080p", "480p" — deixe "" para não filtrar
QUALIDADE = "720p"

PASTA = "downloads/Hanasaku_Iroha_720p"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
    "DNT": "1",
}
# ──────────────────────────────────────────────────────────


def separador(titulo=""):
    print("\n" + "─" * 55)
    if titulo:
        print(f"  {titulo}")
        print("─" * 55)


def coletar_links(url):
    separador("ABRINDO PÁGINA")
    print(f"  URL: {url}\n")

    session = requests.Session()
    session.headers.update(HEADERS)

    print("  Aguardando resposta...")
    r = session.get(url, timeout=30)

    if r.status_code != 200:
        print(f"  Status {r.status_code} — tentando mesmo assim...")

    soup = BeautifulSoup(r.text, "html.parser")

    todos = [
        urljoin(url, a["href"])
        for a in soup.find_all("a", href=True)
    ]

    filtrados = [l for l in todos if any(f in l for f in FILTROS)]

    vistos = set()
    links = []
    for l in filtrados:
        if l not in vistos:
            vistos.add(l)
            links.append(l)

    if QUALIDADE:
        antes = len(links)
        links = [l for l in links if QUALIDADE.lower() in unquote(l).lower()]
        print(f"  Filtro '{QUALIDADE}': {antes} -> {len(links)} links")

    return links, session


def exibir_links(links):
    separador(f"{len(links)} LINKS ENCONTRADOS")
    for i, link in enumerate(links, 1):
        nome = unquote(link.split("/")[-1])
        print(f"  [{i:02d}] {nome}")
    separador()


def selecionar_links(links):
    print("""
  Opcoes:
  Enter       -> baixar TODOS
  1,3,5       -> numeros especificos
  1-10        -> intervalo
  q           -> cancelar
""")
    escolha = input("  Sua escolha: ").strip().lower()

    if escolha == "q":
        print("\n  Cancelado.")
        sys.exit(0)

    if escolha == "":
        return links

    selecionados = []
    for parte in escolha.split(","):
        parte = parte.strip()
        if "-" in parte:
            ini, fim = parte.split("-")
            for i in range(int(ini), int(fim) + 1):
                if 1 <= i <= len(links):
                    selecionados.append(links[i - 1])
        elif parte.isdigit():
            i = int(parte)
            if 1 <= i <= len(links):
                selecionados.append(links[i - 1])

    return selecionados


def baixar(links, session):
    os.makedirs(PASTA, exist_ok=True)
    separador(f"BAIXANDO {len(links)} ARQUIVO(S)")

    for idx, link in enumerate(links, 1):
        nome = unquote(link.split("/")[-1])
        destino = os.path.join(PASTA, nome)

        print(f"\n  [{idx}/{len(links)}] {nome}")

        if os.path.exists(destino):
            print("  Ja existe — pulando.")
            continue

        try:
            r = session.get(link, stream=True, timeout=60)
            r.raise_for_status()

            total = int(r.headers.get("content-length", 0))
            baixado = 0

            with open(destino, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)
                    baixado += len(chunk)
                    if total:
                        pct = baixado / total * 100
                        mb = baixado / (1024 * 1024)
                        print(f"  {pct:5.1f}%  ({mb:.1f} MB)", end="\r")

            print(f"  Concluido ({baixado / (1024*1024):.1f} MB)          ")

        except Exception as e:
            print(f"  Erro: {e}")

        time.sleep(0.5)

    separador("DOWNLOAD FINALIZADO")
    print(f"  Arquivos em: ./{PASTA}/\n")


def salvar_lista(links):
    with open("links.txt", "w") as f:
        for l in links:
            f.write(l + "\n")
    print(f"  Lista salva em links.txt ({len(links)} links)")


if __name__ == "__main__":
    print("\n=== ANIME DOWNLOADER — AnimeOut ===")

    links, session = coletar_links(URL)

    if not links:
        print("\n  Nenhum link encontrado. Verifique a URL ou os filtros.")
        sys.exit(1)

    exibir_links(links)
    salvar_lista(links)

    selecionados = selecionar_links(links)

    if not selecionados:
        print("\n  Nenhum link selecionado.")
        sys.exit(0)

    print(f"\n  {len(selecionados)} arquivo(s) selecionado(s). Iniciando...")
    baixar(selecionados, session)
