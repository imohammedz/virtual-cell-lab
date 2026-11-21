import numpy as np

from .cell import VirtualCell
from .predictor import PerturbationPredictor
from .result import ExperimentResult


class VirtualExperiment:
    def __init__(
        self,
        cell: VirtualCell,
        predictor: PerturbationPredictor,
    ) -> None:
        if cell.genes != predictor.genes:
            raise ValueError("cell and predictor genes must match in name and order")
        if not np.array_equal(cell.control_state, predictor.control_state):
            raise ValueError("cell and predictor control states must match")

        self.cell = cell
        self.predictor = predictor

    def run(self, perturbation: str) -> ExperimentResult:
        predicted_effect = self.predictor.predict(perturbation)
        predicted_state = self.cell.control_state + predicted_effect
        return ExperimentResult.create(
            cell_type=self.cell.cell_type,
            perturbation=perturbation,
            genes=self.cell.genes,
            predicted_state=predicted_state,
            predicted_effect=predicted_effect,
        )
