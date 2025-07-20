
# GTFSearch

![GTFSearch Banner](https://i.imgur.com/eKrVtqQ.png)

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)
![GitHub Stars](https://img.shields.io/github/stars/SkyW4r33x/GTFSearch?style=flat-square&color=brightgreen)
![GitHub Issues](https://img.shields.io/github/issues/SkyW4r33x/GTFSearch?style=flat-square&color=yellow)
![GitHub Forks](https://img.shields.io/github/forks/SkyW4r33x/GTFSearch?style=flat-square)

GTFSearch es una herramienta avanzada de línea de comandos diseñada para buscar y analizar binarios potencialmente explotables basados en el repositorio [GTFOBins](https://gtfobins.github.io/). Facilita la identificación de vulnerabilidades en sistemas Unix/Linux de manera local, eficiente y segura, con soporte para modo interactivo, filtrado por funciones (como SUID o shell) y visualización enriquecida.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Opciones](#opciones)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Créditos](#créditos)
## Características

- **Modo Interactivo**: Explora binarios en un prompt personalizado con autocompletado inteligente, highlighting de sintaxis y navegación intuitiva.
- **Filtrado Avanzado**: Busca por tipos de funciones específicas (ej. `-t suid`) para enfocarte en exploits relevantes.
- **Listado Completo**: Muestra todos los binarios disponibles con detalles de funciones asociadas.
- **Interfaz Enriquecida**: Utiliza [Rich](https://rich.readthedocs.io/en/stable/) para tablas, paneles y código coloreado, mejorando la legibilidad.
- **Seguridad Integrada**: Incluye validación de inputs, sanitización de consultas y manejo seguro de archivos para prevenir riesgos.
- **Modo CLI Flexible**: Ejecuta búsquedas directas o ingresa al modo interactivo sin argumentos adicionales.
- **Portabilidad**: Funciona en entornos virtuales Python para evitar conflictos con el sistema.

## Requisitos

- [Python 3.8 o superior](https://www.python.org/downloads/)
- Sistema operativo Linux (optimizado para [Kali Linux](https://www.kali.org/) y distribuciones basadas en Debian/Ubuntu)
- Dependencias automáticas: `rich` y `prompt-toolkit` (instaladas en un entorno virtual durante la setup)

## Instalación

Clona el repositorio y utiliza el instalador proporcionado. Este crea un entorno virtual Python aislado, elimina versiones previas y configura el ejecutable en `/usr/bin/gtfsearch` para acceso global.

### Para Kali Linux (Recomendado)

```bash
git clone https://github.com/SkyW4r33x/GTFSearch.git
cd GTFSearch
chmod +x kali-install.sh
sudo ./kali-install.sh
```

**Notas de Instalación**:
- El proceso es automatizado y toma menos de un minuto.
- Si encuentras problemas, verifica permisos de root y conexión para actualizaciones de paquetes.
- Para desinstalación, ejecuta el instalador nuevamente (elimina automáticamente versiones previas).

## Uso

Inicia `gtfsearch` sin argumentos para el modo interactivo, ideal para exploración detallada. Para consultas rápidas, proporciona un binario directamente.

### Ejemplos

- **Modo Interactivo** (prompt personalizado para búsquedas y comandos):
  ```bash
  gtfsearch
  ```

- **Búsqueda de un Binario Específico**:
  ```bash
  gtfsearch vim
  ```

- **Listado de Todos los Binarios**:
  ```bash
  gtfsearch -l
  ```

- **Filtrado por Tipo de Función** (ej. SUID):
  ```bash
  gtfsearch vim -t suid
  ```

- **Mostrar Ayuda**:
  ```bash
  gtfsearch -h
  ```

En el modo interactivo, comandos útiles incluyen `help` (o `h`) para el menú de ayuda, `list binaries` (o `lb`) para listar, o ingresa un binario directamente para detalles.

## Opciones

| Opción            | Alias | Descripción                                      |
|-------------------|-------|--------------------------------------------------|
| `-h, --help`      |       | Muestra el mensaje de ayuda completo             |
| `-l, --list`      |       | Lista todos los binarios disponibles             |
| `-t, --type`      |       | Filtra por tipo de función (ej. suid, shell)     |

## Capturas de Pantalla

![Modo Interactivo](https://i.imgur.com/B89HAGr.png)  
*Ejemplo de modo interactivo con autocompletado y highlighting.*

![Búsqueda de Binario](https://i.imgur.com/mAz4CUF.png)  
*Resultado de búsqueda para un binario específico, con paneles y código coloreado.*

![enter image description here](https://imgur.com/uJ7l0e2.png)
*Comparativa GTFSearch y GTFObins*

## Créditos

- **Desarrollador Principal**: [SkyW4r33x](https://github.com/SkyW4r33x)
- **Inspiración y Datos**: Basado en el proyecto [GTFOBins](https://gtfobins.github.io/)
