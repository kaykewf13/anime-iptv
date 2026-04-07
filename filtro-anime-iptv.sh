#!/bin/bash
# =============================================================
# Script: Filtro Automatico de Canais de Anime para IPTV
# Descricao: Baixa listas do IPTV-Org e filtra canais de anime
# Uso: ./filtro-anime-iptv.sh
# =============================================================

set -euo pipefail

# ---- Configuracoes ----
OUTPUT_FILE="anime-iptv-filtrado.m3u"
TEMP_DIR="/tmp/iptv-anime-filter"
LOG_FILE="$TEMP_DIR/filter.log"

# Fontes do IPTV-Org (listas publicas)
SOURCES=(
    "https://iptv-org.github.io/iptv/index.m3u"
    "https://iptv-org.github.io/iptv/categories/animation.m3u"
    "https://iptv-org.github.io/iptv/languages/por.m3u"
    "https://iptv-org.github.io/iptv/languages/jpn.m3u"
)

# Palavras-chave para filtrar anime (case-insensitive)
KEYWORDS=(
    "anime" "animax" "funimation" "crunchyroll"
    "naruto" "dragon ball" "one piece" "bleach"
    "demon slayer" "jujutsu" "attack on titan"
    "my hero" "boku no hero" "shingeki"
    "pokemon" "digimon" "sailor moon"
    "toonami" "tokusatsu" "cartoon"
    "animacao" "animation" "manga"
    "otaku" "pluto tv anime"
    "ghibli" "toei" "aniplex" "mappa"
)

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ---- Funcoes ----

log() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

setup() {
    mkdir -p "$TEMP_DIR"
    : > "$LOG_FILE"

    # Verificar dependencias
    for cmd in curl grep sed awk; do
        if ! command -v "$cmd" &>/dev/null; then
            error "Comando '$cmd' nao encontrado. Instale e tente novamente."
            exit 1
        fi
    done
}

download_sources() {
    log "Baixando listas de IPTV..."
    local count=0

    for url in "${SOURCES[@]}"; do
        local filename
        filename="$TEMP_DIR/source_${count}.m3u"
        log "  Baixando: $url"

        if curl -sL --max-time 30 --retry 3 -o "$filename" "$url" 2>>"$LOG_FILE"; then
            local lines
            lines=$(wc -l < "$filename")
            success "  -> $lines linhas baixadas"
        else
            warn "  -> Falha ao baixar: $url"
        fi

        count=$((count + 1))
    done
}

build_keyword_pattern() {
    local pattern=""
    for kw in "${KEYWORDS[@]}"; do
        if [ -n "$pattern" ]; then
            pattern="${pattern}|${kw}"
        else
            pattern="${kw}"
        fi
    done
    echo "$pattern"
}

filter_anime_channels() {
    log "Filtrando canais de anime..."

    local pattern
    pattern=$(build_keyword_pattern)
    local merged="$TEMP_DIR/merged.m3u"
    local filtered="$TEMP_DIR/filtered_entries.txt"

    # Juntar todas as fontes em um arquivo
    cat "$TEMP_DIR"/source_*.m3u 2>/dev/null > "$merged" || true

    # Extrair pares EXTINF + URL que correspondem aos keywords
    : > "$filtered"

    local prev_line=""
    local match=false
    local total=0
    local matched=0

    while IFS= read -r line; do
        if [[ "$line" == \#EXTINF* ]]; then
            prev_line="$line"
            total=$((total + 1))
            # Verificar se a linha EXTINF contem algum keyword
            if echo "$line" | grep -iEq "$pattern"; then
                match=true
            else
                match=false
            fi
        elif [[ "$line" == http* || "$line" == rtmp* || "$line" == rtsp* ]]; then
            if $match && [ -n "$prev_line" ]; then
                echo "$prev_line" >> "$filtered"
                echo "$line" >> "$filtered"
                matched=$((matched + 1))
            fi
            prev_line=""
            match=false
        fi
    done < "$merged"

    success "Encontrados $matched canais de anime de $total canais totais"
}

remove_duplicates() {
    log "Removendo canais duplicados..."

    local filtered="$TEMP_DIR/filtered_entries.txt"
    local unique="$TEMP_DIR/unique_entries.txt"
    : > "$unique"

    declare -A seen_urls
    local prev_line=""
    local before=0
    local after=0

    while IFS= read -r line; do
        if [[ "$line" == \#EXTINF* ]]; then
            prev_line="$line"
            before=$((before + 1))
        elif [[ "$line" == http* || "$line" == rtmp* || "$line" == rtsp* ]]; then
            if [ -z "${seen_urls[$line]+_}" ]; then
                seen_urls[$line]=1
                echo "$prev_line" >> "$unique"
                echo "$line" >> "$unique"
                after=$((after + 1))
            fi
            prev_line=""
        fi
    done < "$filtered"

    success "De $before canais -> $after unicos (removidos $((before - after)) duplicados)"
}

check_streams() {
    log "Verificando streams ativos (isso pode demorar)..."

    local unique="$TEMP_DIR/unique_entries.txt"
    local active="$TEMP_DIR/active_entries.txt"
    : > "$active"

    local prev_line=""
    local total=0
    local alive=0
    local dead=0

    while IFS= read -r line; do
        if [[ "$line" == \#EXTINF* ]]; then
            prev_line="$line"
        elif [[ "$line" == http* || "$line" == rtmp* || "$line" == rtsp* ]]; then
            total=$((total + 1))
            printf "\r  Verificando %d..." "$total"

            local status
            status=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 8 "$line" 2>/dev/null || echo "000")

            if [[ "$status" == "200" || "$status" == "302" || "$status" == "301" ]]; then
                echo "$prev_line" >> "$active"
                echo "$line" >> "$active"
                alive=$((alive + 1))
            else
                dead=$((dead + 1))
                echo "[OFFLINE] $status - $line" >> "$LOG_FILE"
            fi

            prev_line=""
        fi
    done < "$unique"

    echo ""
    success "$alive canais ativos / $dead offline de $total verificados"
}

generate_m3u() {
    local source_file="$1"
    local output="$2"

    log "Gerando lista M3U final..."

    {
        echo "#EXTM3U"
        echo "# =================================================="
        echo "# Lista IPTV de Anime - Gerada automaticamente"
        echo "# Data: $(date '+%Y-%m-%d %H:%M:%S %Z')"
        echo "# Fonte: IPTV-Org (github.com/iptv-org/iptv)"
        echo "# =================================================="
        echo ""

        if [ -f "$source_file" ]; then
            cat "$source_file"
        fi
    } > "$output"

    local channel_count
    channel_count=$(grep -c "^#EXTINF" "$output" 2>/dev/null || echo "0")
    success "Lista gerada: $output ($channel_count canais)"
}

cleanup() {
    log "Limpando arquivos temporarios..."
    rm -rf "$TEMP_DIR"
}

show_summary() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}         RESUMO DA EXECUCAO${NC}"
    echo -e "${CYAN}========================================${NC}"

    if [ -f "$OUTPUT_FILE" ]; then
        local channels
        channels=$(grep -c "^#EXTINF" "$OUTPUT_FILE" 2>/dev/null || echo "0")
        local urls
        urls=$(grep -c "^http" "$OUTPUT_FILE" 2>/dev/null || echo "0")
        local size
        size=$(du -h "$OUTPUT_FILE" | cut -f1)

        echo -e "  Arquivo:  ${GREEN}$OUTPUT_FILE${NC}"
        echo -e "  Canais:   ${GREEN}$channels${NC}"
        echo -e "  URLs:     ${GREEN}$urls${NC}"
        echo -e "  Tamanho:  ${GREEN}$size${NC}"
        echo ""
        echo -e "  ${YELLOW}Como usar:${NC}"
        echo -e "  - VLC: Arquivo > Abrir > $OUTPUT_FILE"
        echo -e "  - IPTV Player: Importar lista local"
        echo -e "  - TiviMate: Adicionar playlist > Arquivo"
    else
        error "Nenhum arquivo gerado."
    fi

    echo -e "${CYAN}========================================${NC}"
}

# ---- Menu de opcoes ----

show_help() {
    echo "Uso: $0 [opcoes]"
    echo ""
    echo "Opcoes:"
    echo "  --no-check    Pular verificacao de streams (mais rapido)"
    echo "  --sources     Mostrar fontes de download"
    echo "  --keywords    Mostrar palavras-chave do filtro"
    echo "  --add-kw KW   Adicionar palavra-chave extra ao filtro"
    echo "  --output FILE Definir arquivo de saida (padrao: $OUTPUT_FILE)"
    echo "  --help        Mostrar esta ajuda"
}

# ---- Main ----

main() {
    local skip_check=false
    local extra_keywords=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --no-check)
                skip_check=true
                shift
                ;;
            --sources)
                echo "Fontes configuradas:"
                for src in "${SOURCES[@]}"; do
                    echo "  - $src"
                done
                exit 0
                ;;
            --keywords)
                echo "Palavras-chave do filtro:"
                for kw in "${KEYWORDS[@]}"; do
                    echo "  - $kw"
                done
                exit 0
                ;;
            --add-kw)
                shift
                if [[ $# -gt 0 ]]; then
                    extra_keywords+=("$1")
                    shift
                fi
                ;;
            --output)
                shift
                if [[ $# -gt 0 ]]; then
                    OUTPUT_FILE="$1"
                    shift
                fi
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                error "Opcao desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Adicionar keywords extras
    for kw in "${extra_keywords[@]+"${extra_keywords[@]}"}"; do
        KEYWORDS+=("$kw")
    done

    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  Filtro Automatico de Anime IPTV${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""

    setup
    download_sources
    filter_anime_channels
    remove_duplicates

    if $skip_check; then
        warn "Verificacao de streams pulada (--no-check)"
        generate_m3u "$TEMP_DIR/unique_entries.txt" "$OUTPUT_FILE"
    else
        check_streams
        generate_m3u "$TEMP_DIR/active_entries.txt" "$OUTPUT_FILE"
    fi

    show_summary
    cleanup
}

main "$@"
