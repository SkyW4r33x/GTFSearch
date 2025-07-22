![GTFSearch Banner](https://i.imgur.com/eKrVtqQ.png)

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)
![GitHub Stars](https://img.shields.io/github/stars/SkyW4r33x/GTFSearch?style=flat-square&color=brightgreen)
![GitHub Issues](https://img.shields.io/github/issues/SkyW4r33x/GTFSearch?style=flat-square&color=yellow)
![GitHub Forks](https://img.shields.io/github/forks/SkyW4r33x/GTFSearch?style=flat-square)

GTFSearch is an advanced command-line tool designed to search and analyze potentially exploitable binaries based on the [GTFOBins](https://gtfobins.github.io/) repository. It facilitates the identification of vulnerabilities in Unix/Linux systems locally, efficiently, and securely, with support for interactive mode, filtering by functions (such as SUID or shell), and enriched visualization.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Screenshots](#screenshots)
- [Credits](#credits)

## Features

- **Interactive Mode**: Explore binaries in a customized prompt with intelligent autocompletion, syntax highlighting, and intuitive navigation.
- **Advanced Filtering**: Search by specific function types (e.g., `-t suid`) to focus on relevant exploits.
- **Comprehensive Listing**: Displays all available binaries with details of associated functions.
- **Enriched Interface**: Uses [Rich](https://rich.readthedocs.io/en/stable/) for tables, panels, and colored code, improving readability.
- **Built-in Security**: Includes input validation, query sanitization, and secure file handling to prevent risks.
- **Flexible CLI Mode**: Run direct searches or enter interactive mode without additional arguments.
- **Portability**: Works in Python virtual environments to avoid conflicts with the system.

## Requirements

- [Python 3.8 or higher](https://www.python.org/downloads/)
- Linux operating system (optimized for [Kali Linux](https://www.kali.org/) and Debian/Ubuntu-based distributions)
- Automatic dependencies: `rich` and `prompt-toolkit` (installed in a virtual environment during setup)

## Installation

Clone the repository and use the provided installer. It creates an isolated Python virtual environment, removes previous versions, and sets up the executable in `/usr/bin/gtfsearch` for global access.

### For Kali Linux (Recommended)

```bash
git clone https://github.com/SkyW4r33x/GTFSearch.git
cd GTFSearch
chmod +x kali-install.sh
sudo ./kali-install.sh
```

**Installation Notes**:
- The process is automated and takes less than a minute.
- If you encounter issues, verify root permissions and internet connection for package updates.
- For uninstallation, run the installer again (it automatically removes previous versions).

## Usage

Launch `gtfsearch` without arguments for interactive mode, ideal for detailed exploration. For quick queries, provide a binary directly.

### Examples

- **Interactive Mode** (customized prompt for searches and commands):
  ```bash
  gtfsearch
  ```

- **Search for a Specific Binary**:
  ```bash
  gtfsearch vim
  ```

- **List All Binaries**:
  ```bash
  gtfsearch -l
  ```

- **Filter by Function Type** (e.g., SUID):
  ```bash
  gtfsearch vim -t suid
  ```

- **Show Help**:
  ```bash
  gtfsearch -h
  ```

In interactive mode, useful commands include `help` (or `h`) for the help menu, `list binaries` (or `lb`) for listing, or enter a binary directly for details.

## Options

| Option             | Description                                      |
|--------------------|--------------------------------------------------|
| `-h, --help`       | Displays the full help message                  |
| `-l, --list`       | Lists all available binaries                    |
| `-t, --type`       | Filters by function type (e.g., suid, shell)    |

## Screenshots

![Interactive Mode](https://i.imgur.com/B89HAGr.png)  
*Example of interactive mode with autocompletion and highlighting.*

![Binary Search](https://i.imgur.com/mAz4CUF.png)  
*Search result for a specific binary, with panels and colored code.*

![Comparison](https://imgur.com/uJ7l0e2.png)  
*Comparison of GTFSearch and GTFOBins*

## Credits

- **Main Developer**: [SkyW4r33x](https://github.com/SkyW4r33x)
- **Inspiration and Data**: Based on the [GTFOBins](https://gtfobins.github.io/) project
