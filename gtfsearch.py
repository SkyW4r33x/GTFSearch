#!/usr/bin/env python3
#
# Author: SkyW4r33x
# Github: https://github.com/SkyW4r33x/gtfobins
#

from dataclasses import dataclass
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from typing import Dict, List, Optional
import argparse
import json
import os
import sys

console = Console()

class Config:
    @staticmethod
    def get_real_user():
        return os.getenv("SUDO_USER") or os.getenv("USER")
    
    real_user = get_real_user()
    data_file: Path = Path(f"/home/{real_user}/.data/gtfobins.json")

    @classmethod
    def create_default(cls) -> 'Config':
        if not cls.data_file.exists():
            raise FileNotFoundError(f"No se pudo encontrar el archivo de datos en {cls.data_file}")
        return cls()
    
class GTFOBinsManager:
    def __init__(self, config: Config, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self.data = self._load_data()
        self.function_filters = []

    def _load_data(self) -> List[Dict]:
        try:
            with open(self.config.data_file) as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Invalid JSON format: Expected a list.")
                return data
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    def find_command(self, path: str) -> Optional[Dict]:
        command = Path(path).name
        result = next((tool for tool in self.data if tool['name'] == command), None)
        
        if result and self.function_filters:
            # Filtrar funciones si hay filtros activos
            filtered_functions = [
                f for f in result['functions']
                if f['function'] in self.function_filters
            ]
            if filtered_functions:
                result = result.copy()
                result['functions'] = filtered_functions
            else:
                return None
        
        return result

    def scan_directory(self, directory: str) -> List[str]:
        """Escanea un directorio en busca de archivos ejecutables."""
        paths = []
        try:
            if os.path.isfile(directory):
                paths.append(directory)
            else:
                for root, _, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.access(file_path, os.X_OK):  
                            paths.append(file_path)
        except Exception as e:
            if self.verbose:
                console.print(f"[bold red]Error al escanear {directory}:[/bold red] {e}")
        return paths

    def export_results(self, results: Dict, format: str, output_file: str):
        """Exporta los resultados en el formato especificado."""
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
        elif format == 'csv':
            with open(output_file, 'w') as f:
                f.write("Command,Function,Description\n")
                for path, cmd_info in results.items():
                    for func in cmd_info['functions']:
                        f.write(f"{cmd_info['name']},{func['function']},{func.get('description', '')}\n")
        elif format == 'txt':
            with open(output_file, 'w') as f:
                for path, cmd_info in results.items():
                    f.write(f"Command: {cmd_info['name']}\n")
                    for func in cmd_info['functions']:
                        f.write(f"  Function: {func['function']}\n")
                        if 'description' in func:
                            f.write(f"  Description: {func['description']}\n")
                    f.write("\n")

class GTFOBinsDisplay:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_command_header(command: str) -> None:
        width = console.width
        separator = "═" * ((width - len(command) - 4) // 2)
        console.print(f"\n[bold #ca3636]{separator}[ {command} ]{separator}[/bold #ca3636]")

    @staticmethod
    def display_results(command: str, results: Optional[Dict]) -> None:
        GTFOBinsDisplay.clear_screen()
        if not results:
            console.print(f"\n[bold red]✗[/bold red] No se encontraron resultados para [cyan]{command}[/cyan].")
            return

        for function in results['functions']:
            console.print(f"\n[bold cyan][*] {function['function']}:[/bold cyan]")
            
            if description := function.get('description'):
                console.print(f"\n{description}")

            for example in function.get('examples', []):
                if description := example.get('description'):
                    console.print(f"\n[italic yellow]{description}[/italic yellow]")
                if code := example.get('code'):
                    console.print(Syntax(
                        code,
                        "bash",
                        line_numbers=True,
                        theme="one-dark",
                        padding=(1, 1, 1, 0),
                        word_wrap=True
                    ))

    @staticmethod
    def list_commands(data: List[Dict]) -> None:
        GTFOBinsDisplay.clear_screen()
        table = Table(title="\nComandos disponibles en GTFOBins")
        table.add_column("Comando", style="cyan")
        table.add_column("Funciones", style="green")

        for tool in sorted(data, key=lambda x: x['name']):
            functions_str = ", ".join(f['function'] for f in tool['functions'])
            table.add_row(tool['name'], functions_str)

        console.print(table)

    @staticmethod
    def analyze_file(manager: GTFOBinsManager, file_path: str) -> None:
        GTFOBinsDisplay.clear_screen()
        console.print(f"\n[bold yellow]+ [/bold yellow]Analizando ruta desde el archivo: [cyan]{file_path}[/cyan]\n")
        
        try:
            with open(file_path) as f:
                paths = [line.strip() for line in f if line.strip()]
        except (FileNotFoundError, IOError) as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            return

        # Analizar cada ruta encontrada
        results = {}
        not_found = []
        
        for path in paths:
            command = manager.find_command(path)
            if command:
                bin_name = Path(path).name
                if bin_name not in results:
                    results[bin_name] = command
            else:
                bin_name = Path(path).name
                if bin_name not in not_found:
                    not_found.append(bin_name)

        # Mostrar primero los detalles de cada binario encontrado
        if results:
            for bin_name, command_info in results.items():
                GTFOBinsDisplay.print_command_header(bin_name)
                for function in command_info['functions']:
                    console.print(f"\n[bold cyan][*] {function['function']}:[/bold cyan]")
                    
                    if description := function.get('description'):
                        console.print(f"\n{description}")

                    for example in function.get('examples', []):
                        if description := example.get('description'):
                            console.print(f"\n[italic yellow]{description}[/italic yellow]")
                        if code := example.get('code'):
                            console.print(Syntax(
                                code,
                                "bash",
                                line_numbers=True,
                                theme="one-dark",
                                padding=(1, 1, 1, 0),
                                word_wrap=True
                            ))

        # Al final, mostrar el resumen del análisis
        console.print("\n[bold green]+[/bold green] Binarios encontrados:")
        if results:
            found_bins = sorted(results.keys())
            console.print("   [green]" + ", ".join(found_bins))
        else:
            console.print("   [yellow]No se encontraron binarios GTFOBins[/yellow]")

        if not_found:
            console.print("\n[bold red]![/bold red] No encontrados:")
            console.print("   [red]" + ", ".join(sorted(not_found)))

        console.print(f"\n[bold green]» Análisis completado:[/bold green]\n"
                     f"  [bold green]✓[/bold green] Encontrados: {len(results)}\n"
                     f"  [bold red]✗[/bold red] No encontrados: {len(not_found)}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="""Herramienta para buscar y explorar GTFOBins localmente

Author      : SkyW4r33x
Repository  : https://github.com/SkyW4r33x

example of use:
  gtfscan vim                    # Buscar un comando específico
  gtfscan -l                     # Listar todos los comandos
  gtfscan /ruta/archivo.txt      # Analizar rutas desde archivo
""",
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s [-h] [-l] [-v] [comando|archivo]"
    )
    parser.add_argument("-h", "--help", action="help", help="Muestra este mensaje de ayuda")
    parser.add_argument("-l", "--list", action="store_true", help="Listar todos los comandos disponibles")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar información detallada de depuración")
    parser.add_argument("comando", nargs="?", metavar="", help=argparse.SUPPRESS)
    
    args = parser.parse_args()
    manager = GTFOBinsManager(Config(), args.verbose)
    
    if args.list:
        GTFOBinsDisplay.list_commands(manager.data)
    elif args.comando:
        if os.path.isfile(args.comando):
            GTFOBinsDisplay.analyze_file(manager, args.comando)
        else:
            results = manager.find_command(args.comando)
            GTFOBinsDisplay.display_results(args.comando, results)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()