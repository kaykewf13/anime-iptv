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

## Captura de URLs no iOS (iPhone/iPad)

### Metodo 1: App Stream Detector (Recomendado)
1. Baixar **Web Inspector** ou **Achilles** na App Store
2. Ativar o proxy local do app
3. Ir em **Ajustes > Wi-Fi > (sua rede) > Configurar Proxy > Manual**
4. Colocar IP `127.0.0.1` e a porta do app (ex: `8888`)
5. Abrir o site de streaming no Safari
6. Reproduzir o video
7. Voltar ao app e filtrar por `.m3u8` ou `.mpd`
8. Copiar a URL capturada

### Metodo 2: Safari Web Inspector (com Mac)
1. No iPhone: **Ajustes > Safari > Avancado > Web Inspector** (ativar)
2. Conectar o iPhone ao Mac via cabo USB
3. No Mac: abrir **Safari > Desenvolvedor > (nome do iPhone)**
4. Selecionar a aba do site com o video
5. Ir na aba **Rede (Network)**
6. Filtrar por `.m3u8` / `.mpd` / `video`
7. Reproduzir o video no iPhone
8. As URLs aparecerao no Safari do Mac

### Metodo 3: Apps de Proxy/Sniffer para iOS
| App | Descricao | Preco |
|-----|-----------|-------|
| **Stream Detector** | Detecta streams HLS automaticamente | Gratis |
| **Achilles** | Proxy HTTP/HTTPS com inspector | Gratis |
| **Thor HTTP Sniffer** | Sniffer completo de rede | Pago |
| **Proxyman** | Proxy com interface moderna | Freemium |
| **Charles Proxy** (iOS) | Versao mobile do Charles | Pago |
| **HTTP Catcher** | Captura requisicoes HTTP/HTTPS | Pago |

### Metodo 4: Atalhos do iOS (Shortcuts)
1. Criar um **Atalho** que use a acao "Obter conteudo da URL"
2. Combinar com "Obter URLs do Texto" para extrair links de stream
3. Exemplo de fluxo:
   - Entrada: URL da pagina
   - Acao: Obter conteudo da pagina
   - Acao: Corresponder texto (regex: `https?://[^\s"']+\.m3u8[^\s"']*`)
   - Acao: Copiar para area de transferencia

### Metodo 5: a]Shortcut (app Atalhos) + yt-dlp via iSH/a-Shell
1. Instalar **iSH** (emulador Linux) ou **a-Shell** na App Store
2. No terminal do iSH:
   ```bash
   apk add python3 py3-pip
   pip install yt-dlp
   yt-dlp -g "URL_DO_VIDEO"
   ```
3. No a-Shell:
   ```bash
   pip install yt-dlp
   yt-dlp -g "URL_DO_VIDEO"
   ```
4. A URL direta do stream sera exibida no terminal

### Metodo 6: VLC para iOS
1. Baixar **VLC** na App Store
2. Abrir VLC > **Fluxo de Rede**
3. Colar a URL da pagina do video
4. Se o VLC reproduzir, o stream e compativel com IPTV
5. Para capturar a URL real: usar o metodo do Safari Web Inspector enquanto o VLC reproduz

### Dicas especificas para iOS:
- **Certificado SSL:** Apps de proxy precisam instalar um certificado em Ajustes > Geral > Perfis para interceptar HTTPS
- **VPN conflito:** Desativar VPN ao usar apps de proxy (usam a mesma funcionalidade)
- **Rede local:** Funciona melhor em Wi-Fi (nao em dados moveis)
- **Apps de streaming:** Muitos apps usam DRM (Widevine/FairPlay) - essas URLs nao funcionarao em players IPTV

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
