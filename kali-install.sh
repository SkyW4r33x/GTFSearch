#!/bin/bash

# ------------------ CONFIGURACION GLOBAL ---------------- #

readonly VERSION="1.3.0"

readonly BLUE=$'\033[38;2;39;127;255m'
readonly GREEN=$'\033[0;32m'
readonly RED=$'\033[0;31m'
readonly YELLOW=$'\033[1;33m'
readonly BOLD=$'\033[1m'
readonly RESET=$'\033[0m'

log_info() { echo -e "${GREEN}[INFO]${RESET} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${RESET} $*" >&2; }
log_error() { echo -e "${RED}[ERROR]${RESET} $*" >&2; }

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\r${GREEN}[INFO]${RESET} %s %c " "$2" "${spinstr:0:1}"
        spinstr=$temp${spinstr%"${temp}"}
        sleep $delay
        ((i++))
        if [[ $i -eq ${#spinstr} ]]; then i=0; fi
    done
    wait $pid
    local exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        printf "\r${GREEN}[INFO]${RESET} %s ✓\n" "$2"
    else
        printf "\r${RED}[ERROR]${RESET} %s ✗\n" "$2"
        return 1
    fi
    return 0
}

# ------------------ BANNER ---------------- #

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

# ------------------ VERIFICACION DE ROOT ---------------- #

[[ $EUID -ne 0 ]] && { log_error "Este script debe ejecutarse como root\n\nUso: ${YELLOW}sudo $0${RESET}"; exit 1; }

# ------------------ OBTENCION DE USUARIO ---------------- #

REAL_USER=$(logname || echo "${SUDO_USER:-$USER}")
USER_HOME="/home/$REAL_USER"

# ------------------ ELIMINACION DE VERSIONES ANTERIORES ---------------- #

log_info "Eliminando todas las instalaciones anteriores de GTFSearch..."

rm -rf "$USER_HOME/.data" /usr/share/gtfobins /usr/local/lib/gtfsearch /usr/local/bin/gtfsearch.py /usr/bin/gtfsearch.py /usr/bin/gtfsearch &>/dev/null

rm -f "$USER_HOME/.gtfsearch_history" &>/dev/null

for RC in ".bashrc" ".zshrc"; do
    RC_FILE="$USER_HOME/$RC"
    if [[ -f "$RC_FILE" ]]; then
        sed -i '/# GTFSCAN alias/d' "$RC_FILE" &>/dev/null
        sed -i '/alias gtfsearch=/d' "$RC_FILE" &>/dev/null
        log_info "Alias eliminado de $RC si existía"
        sleep 0.5
    fi
done

# ------------------ INSTALACION NUEVA ---------------- #

log_info "Iniciando nueva instalación de GTFSearch..."

mkdir -p "$USER_HOME/.data"
cp .data/gtfobins.json "$USER_HOME/.data/gtfobins.json"
chmod 644 "$USER_HOME/.data/gtfobins.json"
chown -R "$REAL_USER:$REAL_USER" "$USER_HOME/.data"

log_info "Creando entorno virtual..."
mkdir -p /usr/local/lib/gtfsearch
apt update -qq &>/dev/null
apt install -y python3 python3-venv &>/dev/null
python3 -m venv /usr/local/lib/gtfsearch/venv
source /usr/local/lib/gtfsearch/venv/bin/activate

pip install --upgrade pip &>/dev/null &
spinner $! "Actualizando pip en el entorno virtual..." || { log_error "Fallo al actualizar ${RED}${BOLD}pip${RESET}"; exit 1; }

pip install rich &>/dev/null &
spinner $! "Instalando librería ${GREEN}${BOLD}rich${RESET}..." || { log_error "Fallo al instalar ${RED}${BOLD}rich${RESET}"; exit 1; }

pip install prompt-toolkit &>/dev/null &
spinner $! "Instalando librería ${GREEN}${BOLD}prompt-toolkit${RESET}..." || { log_error "Fallo al instalar ${RED}${BOLD}prompt-toolkit${RESET}"; exit 1; }

deactivate

cp gtfsearch.py /usr/local/bin/gtfsearch.py
chmod +x /usr/local/bin/gtfsearch.py

cat << EOF > /usr/bin/gtfsearch
#!/bin/sh
exec /usr/local/lib/gtfsearch/venv/bin/python3 /usr/local/bin/gtfsearch.py "\$@"
EOF
chmod +x /usr/bin/gtfsearch

# ------------------ MENSAJE FINAL ---------------- #

sleep 1.5

echo -e "\n${GREEN}${BOLD}✓${RESET} GTFSearch instalado exitosamente (todas las versiones anteriores eliminadas)"
echo -e "\n${BOLD}Uso:${RESET}"
echo -e "Modo interactivo     :  ${GREEN}gtfsearch${RESET}"
echo -e "Modo no interactivo  :  ${GREEN}gtfsearch${RESET} --help | ${GREEN}gtfsearch${RESET} nmap | ${GREEN}gtfsearch${RESET} nmap ${GREEN}-t${RESET} SUID\n"
echo -e "${BOLD}Nota:${RESET}\nSi usabas aliases, recarga tu shell con:\n${GREEN}source${RESET} ~/.bashrc\n${GREEN}source${RESET} ~/.zshrc\n"

