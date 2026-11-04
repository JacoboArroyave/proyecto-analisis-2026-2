"""Puertos que la aplicacion necesita de adaptadores externos."""

from pathlib import Path
from typing import Protocol

from ruta_optima.domain.models import AccelerationScenario


class ScenarioReader(Protocol):
    """Contrato para leer un escenario sin acoplarse a su formato."""

    def read(self, source: Path) -> AccelerationScenario:
        ...