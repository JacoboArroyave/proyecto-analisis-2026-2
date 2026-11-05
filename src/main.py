"""Punto de entrada principal de la aplicacion."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from time import perf_counter

# Asegurar que la raíz del proyecto esté en el path para las importaciones
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from ruta_optima.application.optimize_acceleration import OptimizeAcceleration
from ruta_optima.constants.base import (
    DEFAULT_LOG_DIRECTORY,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SCENARIO_PATH,
)
from ruta_optima.infrastructure.json_scenario import JsonScenarioReader
from ruta_optima.infrastructure.logging_config import configure_logging

# Importamos las funciones de auditoría
from auditoria.brute_force import fuerza_bruta
from auditoria.greedy import greedy
from auditoria.utils import cargar_json


def mostrar_menu() -> None:
    print("\n================ ADA - MENÚ PRINCIPAL ================")
    print("1. Optimización estándar (Lógica original de la CLI)")
    print("2. Algoritmo de Fuerza Bruta (Auditoría)")
    print("3. Algoritmo Greedy / Voraz (Auditoría)")
    print("0. Salir")
    print("==================================================================")


def ejecutar_optimizacion_estandar(args) -> None:
    """Mantiene intacta la lógica original de tu CLI."""
    logger = configure_logging(args.log_dir, DEFAULT_LOG_LEVEL)
    scenario = JsonScenarioReader().read(args.scenario)
    start_time = perf_counter()
    result = OptimizeAcceleration(logger).execute(list(scenario.stages), scenario.budget)
    elapsed_ms = (perf_counter() - start_time) * 1000

    output = asdict(result)
    if not args.full_output:
        output.pop("dp_trace", None)
        output["execution_time_ms"] = round(elapsed_ms, 3)
        output["trace_entries"] = len(result.dp_trace)
        output["trace_location"] = str(args.log_dir)
    else:
        output["execution_time_ms"] = round(elapsed_ms, 3)

    print(json.dumps(output, indent=2, ensure_ascii=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="Optimiza la aceleracion de una cadena")
    parser.add_argument(
        "scenario",
        type=Path,
        nargs="?",
        default=DEFAULT_SCENARIO_PATH,
        help="Ruta al escenario JSON (por defecto: entrada oficial G3)",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=DEFAULT_LOG_DIRECTORY,
        help="Directorio de logs (por defecto: logs)",
    )
    parser.add_argument(
        "--full-output",
        action="store_true",
        help="Imprime tambien la traza completa de la programacion dinamica",
    )
    args = parser.parse_args()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            print("\n--- Ejecutando Optimización Estándar ---")
            ejecutar_optimizacion_estandar(args)

        elif opcion == "2":
            print("\n--- Ejecutando Algoritmo de Fuerza Bruta ---")
            # Usa por defecto el archivo configurado en utils apuntando a data/
            universo, interacciones = cargar_json()
            fuerza_bruta(universo, interacciones)

        elif opcion == "3":
            print("\n--- Ejecutando Algoritmo Greedy ---")
            universo, interacciones = cargar_json()
            greedy(universo, interacciones)

        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, elija un número entre 1 y 3 (o 0 para salir).")


if __name__ == "__main__":
    main()