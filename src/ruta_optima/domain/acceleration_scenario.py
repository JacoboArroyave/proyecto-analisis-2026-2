"""Objeto de dominio que representa una instancia de aceleración."""

from dataclasses import dataclass

from .stage import Stage


@dataclass(frozen=True)
class AccelerationScenario:
    stages: tuple[Stage, ...]
    budget: int

    def __post_init__(self) -> None:
        if self.budget < 0:
            raise ValueError("budget must be non-negative")