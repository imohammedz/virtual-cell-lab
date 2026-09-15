import unittest

import numpy as np

from src.virtual_cell import ExperimentResult, VirtualCell, VirtualExperiment


class StubPredictor:
    genes = ("A", "B", "C")
    control_state = np.array([1.0, 2.0, 3.0])

    def predict(self, perturbation: str) -> np.ndarray:
        if perturbation != "TFAM":
            raise ValueError("unsupported perturbation")
        return np.array([0.5, -1.0, 0.25])


class VirtualCellTests(unittest.TestCase):
    def test_rejects_misaligned_control_state(self) -> None:
        with self.assertRaisesRegex(ValueError, "same length"):
            VirtualCell("RPE1", [1.0], ["A", "B"])


class ExperimentResultTests(unittest.TestCase):
    def test_ranks_increased_and_decreased_genes(self) -> None:
        result = ExperimentResult.create(
            cell_type="RPE1",
            perturbation="TFAM",
            genes=["A", "B", "C"],
            predicted_state=[1.5, 1.0, 3.25],
            predicted_effect=[0.5, -1.0, 0.25],
        )

        self.assertEqual(result.top_increased_genes(2)[0].gene, "A")
        self.assertEqual(result.top_decreased_genes(2)[0].gene, "B")


class VirtualExperimentTests(unittest.TestCase):
    def test_adds_predicted_effect_to_control_state(self) -> None:
        predictor = StubPredictor()
        cell = VirtualCell("RPE1", predictor.control_state, predictor.genes)

        result = VirtualExperiment(cell, predictor).run("TFAM")

        np.testing.assert_allclose(result.predicted_effect, [0.5, -1.0, 0.25])
        np.testing.assert_allclose(result.predicted_state, [1.5, 1.0, 3.25])

    def test_rejects_mismatched_control_state(self) -> None:
        predictor = StubPredictor()
        cell = VirtualCell("RPE1", [1.0, 2.0, 4.0], predictor.genes)

        with self.assertRaisesRegex(ValueError, "control states must match"):
            VirtualExperiment(cell, predictor)


if __name__ == "__main__":
    unittest.main()
