"""Interfaz de linea de comandos para ejecutar un escenario."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from ruta_optima.application.optimize_acceleration import OptimizeAcceleration
from ruta_optima.infrastructure.logging_config import configure_logging
from ruta_optima.infrastructure.json_scenario import JsonScenarioReader

DEFAULT_SCENARIO = Path("data/entrada_G3_mochila_20_nodos.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Optimiza la aceleracion de una cadena")
    parser.add_argument(
        "scenario",
        type=Path,
        nargs="?",
        default=DEFAULT_SCENARIO,
        help="Ruta al escenario JSON (por defecto: entrada oficial G3)",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=Path("logs"),
        help="Directorio de logs (por defecto: logs)",
    )
    args = parser.parse_args()
    configure_logging(args.log_dir)
    scenario = JsonScenarioReader().read(args.scenario)
    result = OptimizeAcceleration().execute(list(scenario.stages), scenario.budget)
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()