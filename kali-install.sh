#!/bin/bash

# ------------------ GLOBAL CONFIGURATION ---------------- #

readonly VERSION="1.3.0"
readonly BLUE=$'\033[38;2;39;127;255m'
readonly GREEN=$'\033[0;32m'
readonly RED=$'\033[0;31m'
readonly YELLOW=$'\033[1;33m'
readonly CYAN=$'\033[38;2;73;174;230m'
readonly BOLD=$'\033[1m'
readonly RESET=$'\033[0m'

log_info() { echo -e "${GREEN}➜${RESET} $*"; }
log_warn() { echo -e "${YELLOW}⚠${RESET} $*" >&2; }
log_error() { echo -e "${RED}✘${RESET} $*" >&2; }

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⣾⣷⣯⣟⡿⣿'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\r${GREEN}⏳${RESET} %s ${GREEN}%s${RESET} " "$2" "${spinstr:0:1}"
        spinstr=$temp${spinstr%"${temp}"}
        sleep $delay
        ((i++))
        if [[ $i -eq ${#spinstr} ]]; then i=0; fi
    done
    wait $pid
    local exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        printf "\r[${GREEN}✔${RESET}] %s\n" "$2"
    else
        printf "\r[${RED}✘${RESET}] %s\n" "$2"
        return 1
    fi
    return 0
}

separator() {
    echo -e "${BLUE}══════════════════════════════════════════════════════════════════════════${RESET}"
}

uninstall_gtfsearch() {
    log_info "Removing all GTFSearch installations..."
    rm -rf "$USER_HOME/.data" /usr/share/gtfobins /usr/local/lib/gtfsearch /usr/local/bin/gtfsearch.py /usr/bin/gtfsearch.py /usr/bin/gtfsearch &>/dev/null
    rm -f "$USER_HOME/.gtfsearch_history" &>/dev/null

    for RC in ".bashrc" ".zshrc"; do
        RC_FILE="$USER_HOME/$RC"
        if [[ -f "$RC_FILE" ]]; then
            sed -i '/# GTFSCAN alias/d' "$RC_FILE" &>/dev/null
            sed -i '/alias gtfsearch=/d' "$RC_FILE" &>/dev/null
            log_info "Alias removed from $RC if existed"
            sleep 0.5
        fi
    done
    log_info "Uninstallation completed."
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
echo -e "${GREEN}                  Author: SkyW4r33x\n"


# ------------------ ROOT VERIFICATION ---------------- #

log_info "Checking root permissions..."
[[ $EUID -ne 0 ]] && { log_error "This script must be run as root\n\nUsage: ${GREEN}sudo${RESET} ${CYAN}bash${RESET} $0"; exit 1; }
log_info "Root permissions confirmed."

# ------------------ USER DETECTION ---------------- #

REAL_USER=$(logname || echo "${SUDO_USER:-$USER}")
USER_HOME="/home/$REAL_USER"
log_info "Detected user: ${BLUE}$REAL_USER${RESET}"

# ------------------ MAIN MENU ---------------- #

separator
log_info "Available options:"
echo -e "  ${BLUE}1)${RESET} Install GTFSearch v${VERSION} (removes previous versions)"
echo -e "  ${BLUE}2)${RESET} Uninstall GTFSearch (removes everything)"
echo -e ""
read -p "[${YELLOW}*${RESET}] Choose an option (1 or 2): " choice

case "$choice" in
    1)
        separator
        read -p "$(echo -e "${YELLOW}⚠${RESET} Confirmation: Are you sure you want to install? (y/n): ")" confirm
        if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
            log_info "Installation cancelled."
            exit 0
        fi
        uninstall_gtfsearch 
        separator
        log_info "Starting GTFSearch v${VERSION} installation..."
        
        mkdir -p "$USER_HOME/.data"
        cp .data/gtfobins.json "$USER_HOME/.data/gtfobins.json"
        chmod 644 "$USER_HOME/.data/gtfobins.json"
        chown -R "$REAL_USER:$REAL_USER" "$USER_HOME/.data"
        log_info "Data files copied to ${BLUE}$USER_HOME/.data${RESET}"
        
        log_info "Creating Python virtual environment..."
        mkdir -p /usr/local/lib/gtfsearch
        apt update -qq &>/dev/null &
        spinner $! "Updating repositories..." || { log_error "Failed to update repositories"; exit 1; }
        apt install -y python3 python3-venv &>/dev/null &
        spinner $! "Installing Python dependencies..." || { log_error "Failed to install dependencies"; exit 1; }
        
        python3 -m venv /usr/local/lib/gtfsearch/venv
        source /usr/local/lib/gtfsearch/venv/bin/activate
        
        pip install --upgrade pip &>/dev/null &
        spinner $! "Upgrading pip..." || { log_error "Failed to upgrade pip"; exit 1; }
        
        pip install rich &>/dev/null &
        spinner $! "Installing rich library..." || { log_error "Failed to install rich"; exit 1; }
        
        pip install prompt-toolkit &>/dev/null &
        spinner $! "Installing prompt-toolkit library..." || { log_error "Failed to install prompt-toolkit"; exit 1; }
        
        deactivate
        
        install -m 755 -o "$REAL_USER" -g "$REAL_USER" gtfsearch.py /usr/local/bin/gtfsearch.py
        
        cat << EOF > /usr/bin/gtfsearch
#!/bin/sh
exec /usr/local/lib/gtfsearch/venv/bin/python3 /usr/local/bin/gtfsearch.py "\$@"
EOF
        chmod +x /usr/bin/gtfsearch
        log_info "Main script installed at ${BLUE}/usr/bin/gtfsearch${RESET}"
        
        separator
        echo -e "\n[${GREEN}✔${BOLD}${RESET}] Installation completed ${GREEN}successfully${RESET}"

        echo -e "[${CYAN}${BOLD}+${RESET}]${BOLD} Usage instructions:${RESET}"
        echo -e "${BLUE}────────────────────────────────────────────────${RESET}"

        echo -e "[${BLUE}*${RESET}] Interactive mode:      ${CYAN}gtfsearch${RESET}"
        echo -e "[${BLUE}*${RESET}] Non-interactive mode:  ${CYAN}gtfsearch${RESET} --help"
        echo -e "[${BLUE}*${RESET}] Search nmap:           ${CYAN}gtfsearch${RESET} nmap"
        echo -e "[${BLUE}*${RESET}] Search nmap SUID:      ${CYAN}gtfsearch${RESET} nmap ${GREEN}-t${RESET} SUID"

        echo -e "${BLUE}────────────────────────────────────────────────${RESET}"
        echo -e "[${CYAN}${BOLD}+${RESET}]${BOLD} Note:${RESET} If you used aliases, reload your shell with:"
        echo -e " ${CYAN}source${RESET} ~/.bashrc"
        echo -e " ${CYAN}source${RESET} ~/.zshrc\n"

        echo -e "[${CYAN}${BOLD}+${RESET}]${BOLD} Installation summary:${RESET}"

        echo -e "${GREEN}✔${RESET} Data files: ${BLUE}$USER_HOME/.data${RESET}"
        echo -e "${GREEN}✔${RESET} Virtual environment: ${BLUE}/usr/local/lib/gtfsearch/venv${RESET}"
        echo -e "${GREEN}✔${RESET} Executable: ${BLUE}/usr/bin/gtfsearch${RESET}"

        echo -e "[${RED}${BOLD}#${RESET}] Made with heart, in a world of shit 😎!\n"
        separator
        ;;
    2)
        separator
        read -p "$(echo -e "${YELLOW}⚠${RESET} Confirmation: Are you sure you want to uninstall? (y/n): ")" confirm
        if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
            log_info "Uninstallation cancelled."
            exit 0
        fi
        uninstall_gtfsearch
        separator
        echo -e "\n[${RED}${BOLD}#${RESET}] Complete uninstall 😎 CRACK!"
        echo -e "[${BLUE}${BOLD}+${RESET}] All GTFSearch components have been removed.\n"
        separator
    
        ;;
    *)
        log_error "Invalid option. Choose 1 or 2."
        exit 1
        ;;
esac