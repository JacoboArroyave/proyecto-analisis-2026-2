import unittest
from pathlib import Path

from ruta_optima.application.optimize_acceleration import OptimizeAcceleration
from ruta_optima.domain.models import Stage
from ruta_optima.infrastructure.json_scenario import JsonScenarioReader


class AccelerationTests(unittest.TestCase):
    def test_dynamic_programming_reconstructs_optimal_stages(self) -> None:
        stages = [
            Stage("A", duration=10, cost=3, reduction=4),
            Stage("B", duration=8, cost=4, reduction=5),
            Stage("C", duration=6, cost=2, reduction=3),
        ]

        result = OptimizeAcceleration().execute(stages, budget=6)

        self.assertEqual(result.accelerated_stages, ("B", "C"))
        self.assertEqual(result.total_reduction, 8)
        self.assertEqual(result.total_cost, 6)
        self.assertEqual(result.total_duration, 16)
        self.assertEqual(
            result.accelerated_stage_details[0].name,
            "B",
        )
        self.assertEqual(result.accelerated_stage_details[0].cost, 4)
        self.assertTrue(all(entry.reduction >= 0 for entry in result.dp_trace))

    def test_official_g3_input_loads_only_acceleration_data(self) -> None:
        scenario = Path(__file__).parents[1] / "data" / "entrada_G3_mochila_20_nodos.json"

        loaded = JsonScenarioReader().read(scenario)

        self.assertEqual(len(loaded.stages), 20)
        self.assertEqual(loaded.budget, 72)
        self.assertEqual(loaded.stages[0], Stage("E01", 18, 7, 5))


if __name__ == "__main__":
    unittest.main()