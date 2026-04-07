# Guia de Captura de URLs de Video para IPTV

## Fontes Abertas e Legais de Streams

### 1. IPTV-Org (Comunidade Open Source)
- **Site:** https://iptv-org.github.io
- **Repositorio:** https://github.com/iptv-org/iptv
- **Descricao:** Maior colecao comunitaria de canais IPTV publicos e gratuitos
- **Formato:** Listas .m3u prontas, organizadas por pais, categoria e idioma
- **Como usar:** Baixar as listas .m3u e extrair as URLs dos streams desejados

### 2. Pluto TV
- **Site:** https://pluto.tv
- **Descricao:** Servico IPTV gratuito com canais ao vivo (inclui canais de anime)
- **Captura:** As URLs dos streams podem ser obtidas via Developer Tools do navegador (aba Network, filtrar por .m3u8)

### 3. Plex TV (canais gratuitos)
- **Site:** https://www.plex.tv/live-tv/
- **Descricao:** Oferece canais gratuitos ao vivo, incluindo anime
- **Captura:** Inspecionar requisicoes de rede no navegador

### 4. Crunchyroll (conteudo gratuito)
- **Site:** https://www.crunchyroll.com
- **Descricao:** Maior plataforma de anime, parte do conteudo e gratuito com ads
- **Nota:** URLs de stream sao protegidas por DRM - apenas para referencia

### 5. RedeCanais / AnimeFire (BR)
- **Descricao:** Sites brasileiros com anime legendado/dublado
- **Nota:** Verificar legalidade na sua regiao

---

## Tecnicas de Captura de URL

### Metodo 1: Developer Tools do Navegador (F12)
1. Abrir o site com o video
2. Pressionar **F12** para abrir o DevTools
3. Ir na aba **Network**
4. Filtrar por **Media** ou digitar `.m3u8` / `.mpd` / `.mp4`
5. Reproduzir o video
6. Copiar a URL do stream que aparecer

### Metodo 2: Extensoes de Navegador
- **Video DownloadHelper** (Firefox/Chrome) - Detecta streams automaticamente
- **HLS Downloader** - Especializado em capturar links .m3u8
- **Stream Detector** (Firefox) - Detecta streams HLS e DASH

### Metodo 3: yt-dlp (Linha de Comando)
```bash
# Listar formatos disponiveis de um video
yt-dlp --list-formats "URL_DO_VIDEO"

# Extrair URL direta do stream (sem baixar)
yt-dlp -g "URL_DO_VIDEO"

# Extrair URL com melhor qualidade
yt-dlp -g -f best "URL_DO_VIDEO"

# Extrair apenas audio
yt-dlp -g -f bestaudio "URL_DO_VIDEO"
```

### Metodo 4: FFprobe (analise de stream)
```bash
# Verificar se uma URL de stream e valida
ffprobe "URL_DO_STREAM"

# Ver detalhes do stream (codec, resolucao, bitrate)
ffprobe -v quiet -print_format json -show_streams "URL_DO_STREAM"
```

### Metodo 5: Wireshark / Charles Proxy
- Capturar trafego de rede de apps mobile ou desktop
- Filtrar por protocolos HTTP/HTTPS
- Buscar por extensoes .m3u8, .ts, .mpd

---

## Formatos de Stream Comuns

| Formato | Extensao | Descricao |
|---------|----------|-----------|
| HLS | .m3u8 | HTTP Live Streaming (mais comum em IPTV) |
| DASH | .mpd | Dynamic Adaptive Streaming |
| MP4 | .mp4 | Stream direto de arquivo |
| RTMP | rtmp:// | Real-Time Messaging Protocol |
| RTSP | rtsp:// | Real-Time Streaming Protocol |

---

## Estrutura de um arquivo M3U para IPTV

```m3u
#EXTM3U

#EXTINF:-1 tvg-id="canal1" tvg-name="Naruto" tvg-logo="https://exemplo.com/logo.png" group-title="Anime",Naruto
https://exemplo.com/stream/naruto.m3u8

#EXTINF:-1 tvg-id="canal2" tvg-name="One Piece" tvg-logo="https://exemplo.com/logo2.png" group-title="Anime",One Piece
https://exemplo.com/stream/onepiece.m3u8
```

### Campos importantes:
- **tvg-id:** Identificador unico do canal
- **tvg-name:** Nome do canal
- **tvg-logo:** URL do logo/imagem
- **group-title:** Categoria/grupo
- **URL:** Link direto do stream (proximo linha apos #EXTINF)

---

## Ferramentas Uteis

| Ferramenta | Uso |
|-----------|-----|
| **yt-dlp** | Extrair URLs de centenas de sites |
| **ffmpeg/ffprobe** | Validar e converter streams |
| **m3u4u.com** | Editor online de listas M3U |
| **xTeVe** | Proxy IPTV com suporte a EPG |
| **TiviMate** | Player IPTV para Android/TV |
| **VLC** | Player universal que suporta M3U |
| **IPTV Checker** | Verificar quais URLs estao ativas |

---

## Dicas para Manter a Lista Atualizada

1. **Verificacao periodica:** URLs de stream expiram - verificar regularmente
2. **Multiplas fontes:** Ter URLs de backup para cada canal
3. **Automacao:** Criar scripts para verificar URLs ativas automaticamente
4. **EPG (Guia de Programacao):** Adicionar fontes EPG para ter grade de programacao
5. **User-Agent:** Alguns streams exigem User-Agent especifico no header

```bash
# Script simples para verificar URLs ativas
while IFS= read -r line; do
  if [[ "$line" == http* ]]; then
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$line")
    echo "$status - $line"
  fi
done < lista.m3u
```
