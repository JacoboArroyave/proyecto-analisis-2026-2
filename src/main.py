"""Punto de entrada principal de la aplicacion."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from time import perf_counter

from ruta_optima.application.optimize_acceleration import OptimizeAcceleration
from ruta_optima.constants.base import (
    DEFAULT_LOG_DIRECTORY,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SCENARIO_PATH,
)
from ruta_optima.infrastructure.json_scenario import JsonScenarioReader
from ruta_optima.infrastructure.logging_config import configure_logging


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

    logger = configure_logging(args.log_dir, DEFAULT_LOG_LEVEL)
    scenario = JsonScenarioReader().read(args.scenario)
    start_time = perf_counter()
    result = OptimizeAcceleration(logger).execute(list(scenario.stages), scenario.budget)
    elapsed_ms = (perf_counter() - start_time) * 1000

    output = asdict(result)
    if not args.full_output:
        output.pop("dp_trace")
        output["execution_time_ms"] = round(elapsed_ms, 3)
        output["trace_entries"] = len(result.dp_trace)
        output["trace_location"] = str(args.log_dir)
    else:
        output["execution_time_ms"] = round(elapsed_ms, 3)

    print(json.dumps(output, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
