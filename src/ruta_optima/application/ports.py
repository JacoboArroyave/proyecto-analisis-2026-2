"""Puertos que la aplicacion necesita de adaptadores externos."""

from pathlib import Path
from typing import Protocol

from ruta_optima.domain.acceleration_scenario import AccelerationScenario


class ScenarioReader(Protocol):
    """Contrato para leer un escenario sin acoplarse a su formato."""

    def read(self, source: Path) -> AccelerationScenario:
        ...


class LoggerPort(Protocol):
    """Contrato mínimo de logging requerido por los casos de uso."""

    def info(self, message: str, *args: object) -> None:
        ...

    def debug(self, message: str, *args: object) -> None:
        ...