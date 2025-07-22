#!/bin/bash

# ------------------ GLOBAL CONFIGURATION ---------------- #

readonly VERSION="1.3.0"
readonly BLUE=$'\033[38;2;39;127;255m'
readonly GREEN=$'\033[0;32m'
readonly RED=$'\033[0;31m'
readonly YELLOW=$'\033[1;33m'
readonly CYAN=$'\033[38;2;73;174;230m'
readonly PINK=$'\033[38;2;254;1;58m'
readonly BOLD=$'\033[1m'
readonly RESET=$'\033[0m'

log_info() { echo -e "[${GREEN}${BOLD}➜${RESET}] $*"; }
log_warn() { echo -e "[${YELLOW}${BOLD}!${RESET}] $*" >&2; }
log_error() { echo -e "[${RED}${BOLD}✘${RESET}] $*" >&2; }
gtfsearch() { echo -n  "${BLUE}${BOLD}GTFSearch${RESET}"; }

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⣾⣷⣯⣟⡿⣿'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\r[${GREEN}⏳${RESET}] %s ${GREEN}%s${RESET} " "$2" "${spinstr:0:1}"
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
    echo -e "${BLUE}\n══════════════════════════════════════════════════════════════════════════\n${RESET}"
}

uninstall_gtfsearch() {
  log_info "Removing all $(gtfsearch) installations..."
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

show_banner() {
    clear
    echo -e "${BLUE}"
    echo -e " ██████╗████████╗███████╗███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗ "
    echo -e "██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║ "
    echo -e "██║  ███╗  ██║   █████╗  ███████╗█████╗  ███████║██████╔╝██║     ███████║ "
    echo -e "██║   ██║  ██║   ██╔══╝  ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║ "
    echo -e "╚██████╔╝  ██║   ██║     ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║ "
    echo -e " ╚═════╝   ╚═╝   ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ${RESET}\n"
    echo -e "        ${BLUE}+ -- --=[${RESET} ${YELLOW}${bold}+${RESET} Created by ${BLUE}${BOLD}:${RESET} Jordan (SkyW4r33x) 🐉 ${BLUE}${BOLD}       ]${RESET}"
    echo -e "        ${BLUE}+ -- --=[${RESET} ${YELLOW}${bold}+${RESET} Repository ${BLUE}${BOLD}:${RESET} https://github.com/SkyW4r33x ${BLUE}${BOLD}]${RESET}\n\n"
}

show_menu() {
    separator
    log_info "Available options:"
    echo -e "  ${BOLD}1)${RESET} Install $(gtfsearch) ${BOLD}v${VERSION}${RESET} (removes previous versions)"
    echo -e "  ${BOLD}2)${RESET} Uninstall $(gtfsearch) (removes everything)"
    echo -e ""
}

show_usage_instructions() {
    clear
    echo -e "\n[${CYAN}${BOLD}+${RESET}]${BOLD} Usage instructions:${RESET}"
    echo -e "${BLUE}────────────────────────────────────────────────${RESET}"
    sleep 0.5
    echo -e "[${BLUE}*${RESET}] Interactive mode:      ${CYAN}gtfsearch${RESET}"
    sleep 0.5
    echo -e "[${BLUE}*${RESET}] Non-interactive mode:  ${CYAN}gtfsearch${RESET} ${GREEN}--help${RESET}"
    sleep 0.5
    echo -e "[${BLUE}*${RESET}] Search nmap:           ${CYAN}gtfsearch${RESET} nmap"
    sleep 0.5
    echo -e "[${BLUE}*${RESET}] Search nmap SUID:      ${CYAN}gtfsearch${RESET} nmap ${GREEN}-t${RESET} SUID\n"
}

show_installation_summary() {
    sleep 0.5
    echo -e "[${CYAN}${BOLD}+${RESET}]${BOLD} Installation summary:${RESET}"
    echo -e "${BLUE}────────────────────────────────────────────────${RESET}"
    sleep 0.5
    echo -e "[${GREEN}✔${RESET}] Data files: ${BLUE}${BOLD}$USER_HOME/.data${RESET}"
    sleep 0.5
    echo -e "[${GREEN}✔${RESET}] Virtual environment: ${BLUE}${BOLD}/usr/local/lib/gtfsearch/venv${RESET}"
    sleep 0.5
    echo -e "[${GREEN}✔${RESET}] Executable: ${BLUE}${BOLD}/usr/bin/gtfsearch${RESET}\n"
}

# ------------------ CORE FUNCTIONS ---------------- #
check_root() {
    log_info "Checking root permissions..."
    [[ $EUID -ne 0 ]] && { 
        log_error "This script must be run as root\n\nUsage: ${GREEN}sudo${RESET} ${CYAN}bash${RESET} $0"
        exit 1
    }
    log_info "Root permissions confirmed."
}

detect_user() {
    REAL_USER=$(logname || echo "${SUDO_USER:-$USER}")
    USER_HOME="/home/$REAL_USER"
    log_info "Detected user: ${BLUE}${BOLD}$REAL_USER${RESET}"
}

install_dependencies() {
    log_info "Creating Python virtual environment..."
    mkdir -p /usr/local/lib/gtfsearch
    apt update -qq &>/dev/null &
    spinner $! "Updating repositories..." || { log_error "Failed to update repositories"; return 1; }
    apt install -y python3 python3-venv &>/dev/null &
    spinner $! "Installing Python dependencies..." || { log_error "Failed to install dependencies"; return 1; }
}

setup_python_environment() {
    python3 -m venv /usr/local/lib/gtfsearch/venv
    source /usr/local/lib/gtfsearch/venv/bin/activate
    
    pip install --upgrade pip &>/dev/null &
    spinner $! "Upgrading pip..." || { log_error "Failed to upgrade pip"; return 1; }
    
    pip install rich prompt-toolkit &>/dev/null &
    spinner $! "Installing required libraries..." || { log_error "Failed to install libraries"; return 1; }
    
    deactivate
}

install_gtfsearch() {
    separator
    log_info "Starting $(gtfsearch) v${VERSION} installation..."
    
    mkdir -p "$USER_HOME/.data"
    cp .data/gtfobins.json "$USER_HOME/.data/gtfobins.json"
    chmod 644 "$USER_HOME/.data/gtfobins.json"
    chown -R "$REAL_USER:$REAL_USER" "$USER_HOME/.data"
    log_info "Data files copied to ${BLUE}${BOLD}$USER_HOME/.data${RESET}"
    
    install_dependencies || return 1
    setup_python_environment || return 1
    
    install -m 755 -o "$REAL_USER" -g "$REAL_USER" gtfsearch.py /usr/local/bin/gtfsearch.py
    
    cat << EOF > /usr/bin/gtfsearch
#!/bin/sh
exec /usr/local/lib/gtfsearch/venv/bin/python3 /usr/local/bin/gtfsearch.py "\$@"
EOF
    chmod +x /usr/bin/gtfsearch
    log_info "Main script installed at ${BLUE}${BOLD}/usr/bin/gtfsearch${RESET}"
    return 0
}

# ------------------ MAIN EXECUTION ---------------- #
main() {
    show_banner
    check_root
    detect_user

    prompt_status="${GREEN}✔${RESET}"

    while true; do
        show_banner
        check_root
        detect_user
        show_menu
        read -p "$(echo -e "${GREEN}┌──(${RESET}${BLUE}${BOLD}$REAL_USER${RESET}${GREEN})-[${RESET}${BOLD}GTFSearch${RESET}${GREEN}]-[${prompt_status}${GREEN}]${RESET}\n${GREEN}└──╼${RESET}${BLUE}$ ${RESET}")" choice
        case "$choice" in
            1|2) break ;;
            *)  echo -e ""
                log_error "Invalid option. Please choose 1 or 2."
                prompt_status="${RED}✘ ERROR${RESET}"
                sleep 1
                clear
                ;;
        esac
    done

    case "$choice" in
        1)
            clear
            echo ""
            read -p "$(echo -e "[${YELLOW}${BOLD}!${RESET}] ${BOLD}Confirmation:${RESET} Are you sure you want to install? (y/n): ")" confirm
            [[ "$confirm" != [yY] ]] && { log_info "Installation ${GREEN}cancelled${RESET}."; exit 0; }
            
            uninstall_gtfsearch
            if install_gtfsearch; then
                separator
                sleep 3
                show_usage_instructions
                show_installation_summary
                echo -e "[${RED}${BOLD}#${RESET}] Made with heart${RED}${BOLD}❣${RESET}, in a world of shit 😎!\n"
                echo -e "\t\t${RED}${BOLD}H4PPY H4CK1NG${RESET}"
            fi
            ;;
        2)
            clear
            read -p "$(echo -e "\n[${BOLD}${YELLOW}!${RESET}] ${BOLD}Confirmation:${RESET} Are you sure you want to uninstall? (y/n): ")" confirm
            [[ "$confirm" != [yY] ]] && { log_info "Uninstallation cancelled."; exit 0; }
            
            uninstall_gtfsearch
            echo -e "\n\t[${RED}${BOLD}#${RESET}] ${RED}${BOLD}GTFSearch${RESET} complete uninstallation 😎 CRACK!\n"
            ;;
    esac
}

main