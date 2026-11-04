"""Entidades y objetos de valor del dominio."""

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


@dataclass(frozen=True)
class DpTraceEntry:
    stage: str
    stage_index: int
    budget: int
    reduction: int
    decision: str


@dataclass(frozen=True)
class AcceleratedStage:
    name: str
    cost: int
    reduction: int


@dataclass(frozen=True)
class AccelerationScenario:
    stages: tuple[Stage, ...]
    budget: int

    def __post_init__(self) -> None:
        if self.budget < 0:
            raise ValueError("budget must be non-negative")


@dataclass(frozen=True)
class AccelerationResult:
    base_duration: int
    total_duration: int
    total_cost: int
    total_reduction: int
    accelerated_stages: tuple[str, ...]
    accelerated_stage_details: tuple[AcceleratedStage, ...]
    dp_trace: tuple[DpTraceEntry, ...]