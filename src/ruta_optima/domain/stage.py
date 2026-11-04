"""Entidad de una etapa de la cadena."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Stage:
    """Etapa de la cadena que puede acelerarse una sola vez."""

    name: str
    duration: int
    cost: int
    reduction: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("stage name cannot be empty")
        if self.duration < 0 or self.cost < 0 or self.reduction < 0:
            raise ValueError("duration, cost and reduction must be non-negative")
        if self.reduction > self.duration:
            raise ValueError("reduction cannot exceed duration")