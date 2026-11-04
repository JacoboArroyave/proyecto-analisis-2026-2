"""Detalle de una etapa seleccionada para aceleración."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AcceleratedStage:
    name: str
    cost: int
    reduction: int