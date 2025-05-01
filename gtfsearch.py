#!/usr/bin/env python3
#
# Author: SkyW4r33x
# Github: https://github.com/SkyW4r33x/gtfobins
#

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
    def get_real_user() -> str:
        return os.getenv("SUDO_USER") or os.getenv("USER") or "unknown"
    
    real_user = get_real_user()
    data_file: Path = Path(f"/home/{real_user}/.data/gtfobins.json")

    @classmethod
    def create_default(cls) -> 'Config':
        if not cls.data_file.exists():
            raise FileNotFoundError(f"No se encontró el archivo de datos en {cls.data_file}")
        return cls()

class GTFOBinsManager:
    def __init__(self, config: Config, verbose: bool = False, function_type: Optional[str] = None):
        self.config = config
        self.verbose = verbose
        self.function_filter = function_type.lower() if function_type else None
        self.data = self._load_data()

    def _load_data(self) -> List[Dict]:
        try:
            with open(self.config.data_file, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Formato JSON inválido: se esperaba una lista")
                return data
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            if self.verbose:
                console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    def find_command(self, command: str) -> Optional[Dict]:
        command_name = Path(command).name
        result = next((tool for tool in self.data if tool['name'] == command_name), None)
        
        if result and self.function_filter:
            filtered_functions = [
                f for f in result['functions']
                if f['function'].lower() == self.function_filter
            ]
            if filtered_functions:
                result = result.copy()
                result['functions'] = filtered_functions
            else:
                return None
        
        return result

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

        GTFOBinsDisplay.print_command_header(command)
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
        table = Table(title="\nComandos disponibles en GTFOBins", title_style="bold #ca3636")
        table.add_column("Comando", style="cyan")
        table.add_column("Funciones", style="yellow")
        for tool in sorted(data, key=lambda x: x['name']):
            functions_str = ", ".join(f['function'] for f in tool['functions'])
            table.add_row(tool['name'], functions_str)
        console.print(table)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Busca información de GTFOBins para un comando, opcionalmente filtrado por tipo (e.g., SUID), o lista todos los comandos",
        add_help=False,
        usage="gtfsearch [-h] [-v] [-l] [-t TYPE] [comando]"
    )
    parser.add_argument("-h", "--help", action="help", help="Muestra este mensaje de ayuda")
    parser.add_argument("-v", "--verbose", action="store_true", help="Muestra detalles de depuración")
    parser.add_argument("-l", "--list", action="store_true", help="Lista todos los comandos disponibles")
    parser.add_argument("-t", "--type", help="Filtra por tipo de función (e.g., SUID)")
    parser.add_argument("comando", nargs="?", help="Comando a buscar (e.g., nmap)")
    
    args = parser.parse_args()

    try:
        config = Config.create_default()
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    manager = GTFOBinsManager(config, args.verbose, args.type)
    
    if args.list:
        GTFOBinsDisplay.list_commands(manager.data)
    elif args.comando:
        results = manager.find_command(args.comando)
        GTFOBinsDisplay.display_results(args.comando, results)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
