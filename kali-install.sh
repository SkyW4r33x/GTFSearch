#!/bin/bash

# variables globales
readonly VERSION="1.3.0"

# colores 
readonly BLUE=$'\033[38;2;39;127;255m'
readonly GREEN=$'\033[0;32m'
readonly RED=$'\033[0;31m'
readonly YELLOW=$'\033[1;33m'
readonly BOLD=$'\033[1m'
readonly RESET=$'\033[0m'

# estilo de mensaje con colores
log_info() { echo -e "${GREEN}[INFO]${RESET} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${RESET} $*" >&2; }
log_error() { echo -e "${RED}[ERROR]${RESET} $*" >&2; }

clear
echo -e "${BLUE}"
echo -e "══════════════════════════════════════════════════════════════════════════" 
echo -e " ██████╗████████╗███████╗███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗ "
echo -e "██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║ "
echo -e "██║  ███╗  ██║   █████╗  ███████╗█████╗  ███████║██████╔╝██║     ███████║ "
echo -e "██║   ██║  ██║   ██╔══╝  ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║ "
echo -e "╚██████╔╝  ██║   ██║     ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║ "
echo -e " ╚═════╝   ╚═╝   ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ "
echo -e "══════════════════════════════════════════════════════════════════════════"                                                              
echo -e "${GREEN}                ╚ Author: SkyW4r33x | v${VERSION} ╝${RESET}\n"
echo -e "${BOLD}         [ GTFSEARCH - GTFOBins Scanner & Exploitation ]${RESET}\n"

# revision si es root o no
[[ $EUID -ne 0 ]] && { log_error "Este script debe ejecutarse como root\n\nUso: ${YELLOW}sudo $0${RESET}"; exit 1; }

# obtencion del ususario normal
REAL_USER=$(logname || echo "${SUDO_USER:-$USER}")
USER_HOME="/home/$REAL_USER"

log_info "Iniciando instalación de GTFSearch..."
# elimina versiones anteriores
rm -rf "$USER_HOME/.data" /usr/local/bin/gtfsearch.py &>/dev/null
# copiando data de GTFObins
cp -r .data $USER_HOME &>/dev/null
# copiando utilidad a /usr/bin
cp gtfsearch.py /usr/bin/ &>/dev/null
# dando permisos de ejecucion
chmod +x /usr/bin/gtfsearch.py
# haciendo que la carpeta y la utilidad sea del ususairo normal
chown "$REAL_USER":"$REAL_USER" /usr/bin/gtfsearch.py 
chown -R "$REAL_USER:$REAL_USER" "$USER_HOME/.data"
sleep 1.5

log_info "Instalando dependencias..."
apt update -qq &>/dev/null
apt install -y python3 &>/dev/null
apt install -y python3-rich &>/dev/null
apt install -y python3-typing-extensions &>/dev/null
sleep 0.5

ALIAS_LINE="alias gtfsearch='/usr/bin/gtfsearch.py'"

for RC in ".bashrc" ".zshrc"; do
    RC_FILE="$USER_HOME/$RC"
    if [[ -f "$RC_FILE" ]]; then
        if ! grep -q "^alias gtfsearch=" "$RC_FILE" 2>/dev/null; then
            echo -e "\n# GTFSCAN alias\n$ALIAS_LINE" >> "$RC_FILE"
            log_info "Alias agregado a $RC"
            sleep 0.5
        else
            log_warn "El alias ya existe en $RC"
            sleep 0.5
        fi
    fi
done


echo -e "\n${GREEN}${BOLD}✓${RESET} GTFSCAN instalado exitosamente"
echo -e "\n${BOLD}Uso:${RESET}"
echo -e "1. Recarga tu shell:  ${YELLOW}source ~/.bashrc ${GREEN}(o ~/.zshrc)${RESET}"
echo -e "2. Ejecuta:           ${YELLOW}gtfsearch --help${RESET}\n"
