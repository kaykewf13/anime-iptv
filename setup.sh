#!/bin/sh
# Script simplificado para iSH (iOS)
# Uso: sh setup.sh

echo "Baixando arquivos..."

cd /root

curl -LO "https://raw.githubusercontent.com/kaykewf13/anime-iptv/claude/video-url-iptv-capture-Kyjuu/filtro-anime-iptv.sh"

curl -LO "https://raw.githubusercontent.com/kaykewf13/anime-iptv/claude/video-url-iptv-capture-Kyjuu/exemplo-lista.m3u"

chmod +x filtro-anime-iptv.sh

echo "Executando filtro..."

bash filtro-anime-iptv.sh --no-check

echo "Pronto! Arquivo gerado: /root/anime-iptv-filtrado.m3u"
