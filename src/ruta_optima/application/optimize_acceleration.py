"""Caso de uso de aceleracion optima bajo presupuesto."""

import logging

from ruta_optima.domain.models import AcceleratedStage, AccelerationResult, DpTraceEntry, Stage

logger = logging.getLogger("ruta_optima.application.optimize_acceleration")


class OptimizeAcceleration:
    """Orquesta la solucion exacta de mochila 0/1 para una cadena."""

    def execute(self, stages: list[Stage], budget: int) -> AccelerationResult:
        if budget < 0:
            raise ValueError("budget must be non-negative")

        logger.info("Iniciando optimizacion DP: %d etapas, presupuesto %d", len(stages), budget)

        reductions = [0] * (budget + 1)
        choices = [[False] * (budget + 1) for _ in stages]
        trace: list[DpTraceEntry] = []

        for stage_index, stage in enumerate(stages):
            logger.debug(
                "Procesando etapa %s (%d/%d): costo=%d, reduccion=%d",
                stage.name,
                stage_index + 1,
                len(stages),
                stage.cost,
                stage.reduction,
            )
            previous = reductions[:]
            for available_budget in range(budget + 1):
                best = previous[available_budget]
                decision = "skip"
                if stage.cost <= available_budget:
                    candidate = previous[available_budget - stage.cost] + stage.reduction
                    if candidate > best:
                        best = candidate
                        decision = "take"
                        choices[stage_index][available_budget] = True
                reductions[available_budget] = best
                logger.debug(
                    "DP[%d][%d] = %d (%s)",
                    stage_index + 1,
                    available_budget,
                    best,
                    decision,
                )
                trace.append(
                    DpTraceEntry(
                        stage=stage.name,
                        stage_index=stage_index,
                        budget=available_budget,
                        reduction=best,
                        decision=decision,
                    )
                )

        selected: list[str] = []
        remaining_budget = budget
        for stage_index in range(len(stages) - 1, -1, -1):
            stage = stages[stage_index]
            if choices[stage_index][remaining_budget]:
                selected.append(stage.name)
                remaining_budget -= stage.cost
        selected.reverse()

        total_reduction = reductions[budget]
        total_cost = sum(stage.cost for stage in stages if stage.name in selected)
        base_duration = sum(stage.duration for stage in stages)
        selected_details = tuple(
            AcceleratedStage(stage.name, stage.cost, stage.reduction)
            for stage in stages
            if stage.name in selected
        )
        logger.info(
            "Optimizacion finalizada: reduccion=%d, duracion=%d, costo=%d, etapas=%s",
            total_reduction,
            base_duration - total_reduction,
            total_cost,
            ", ".join(selected),
        )
        return AccelerationResult(
            base_duration=base_duration,
            total_duration=base_duration - total_reduction,
            total_cost=total_cost,
            total_reduction=total_reduction,
            accelerated_stages=tuple(selected),
            accelerated_stage_details=selected_details,
            dp_trace=tuple(trace),
        )