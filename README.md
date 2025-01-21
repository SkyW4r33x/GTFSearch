# GTFScan

GTFScan es un escáner local de GTFOBins. Esta herramienta de línea de comandos está diseñada para identificar y analizar binarios potencialmente vulnerables en sistemas Unix/Linux de manera rápida y eficiente.

## Requisitos

- Python 3.13.1    [![Python](https://img.shields.io/badge/Python-3.13.1+-blue.svg)](https://www.python.org/downloads/)

- Solo sistema operativo Linux

## Instalación

### Kali Linux
```bash
git clone https://github.com/SkyW4r33x/GTFSearch.git
cd gtfobins
chmod +x kali-install.sh
./kali-install.sh
```

### Otras distribuciones
```bash
git clone https://github.com/SkyW4r33x/GTFSearch.git
cd gtfobins
pip install -r requirements.txt
chmod +x install.sh
./install.sh
```

## Uso
```bash
gtfscan vim                 # Buscar un binario específico
gtfscan -l                  # Listar todos los binarios
gtfscan /ruta/archivo.txt   # Analizar desde archivo
gtfscan -h                  # Mostrar ayuda
```

## Opciones
| Opción | Descripción |
|--------|-------------|
| `-l, --list` | Lista todos los binarios disponibles |
| `-v, --verbose` | Modo verboso con información detallada |
| `-h, --help` | Muestra el mensaje de ayuda |


## Créditos
- 🔧 Desarrollado por [SkyW4r33x](https://github.com/SkyW4r33x)
- 💡 Basado en el proyecto [GTFOBins](https://github.com/GTFOBins/GTFOBins.github.io)
