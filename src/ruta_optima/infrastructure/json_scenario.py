"""Adaptador JSON para escenarios de aceleracion."""

import json
import logging
from pathlib import Path

from ruta_optima.domain.acceleration_scenario import AccelerationScenario
from ruta_optima.domain.stage import Stage


class JsonScenarioReader:
    """Adaptador que traduce JSON externo al modelo del dominio."""

    def read(self, source: Path) -> AccelerationScenario:
        logger = logging.getLogger("ruta_optima.infrastructure.json_scenario")
        logger.info("Leyendo escenario JSON: %s", source)
        with source.open(encoding="utf-8") as file:
            payload = json.load(file)

        if "stages" in payload:
            stages = tuple(Stage(**stage) for stage in payload["stages"])
            scenario = AccelerationScenario(stages, payload["budget"])
            logger.info("Escenario cargado: %d etapas, presupuesto %d", len(stages), scenario.budget)
            return scenario

        parameters = payload["parametros"]
        stages = tuple(
            Stage(
                name=stage["id"],
                duration=stage["duracion_normal"],
                cost=stage["costo_aceleracion"],
                reduction=stage["reduccion_tiempo_si_acelera"],
            )
            for stage in payload["etapas"]
        )
        scenario = AccelerationScenario(stages, parameters["presupuesto_aceleracion_B"])
        logger.info("Entrada oficial G3 cargada: %d etapas, presupuesto %d", len(stages), scenario.budget)
        return scenario