"""Objeto de trazabilidad de una decisión de programación dinámica."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DpTraceEntry:
    stage: str
    stage_index: int
    budget: int
    reduction: int
    decision: str