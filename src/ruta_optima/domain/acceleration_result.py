"""Resultado de la optimización de aceleración."""

from dataclasses import dataclass

from .accelerated_stage import AcceleratedStage
from .dp_trace_entry import DpTraceEntry


@dataclass(frozen=True)
class AccelerationResult:
    base_duration: int
    total_duration: int
    total_cost: int
    total_reduction: int
    accelerated_stages: tuple[str, ...]
    accelerated_stage_details: tuple[AcceleratedStage, ...]
    dp_trace: tuple[DpTraceEntry, ...]