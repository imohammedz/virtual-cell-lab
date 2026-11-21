from functools import lru_cache
from pathlib import Path

from src.virtual_cell import PerturbationPredictor, VirtualCell, VirtualExperiment
from src.virtual_cell.result import ExperimentResult

MODEL_NAMES = {
    "no_change": "No change",
    "average_effect": "Average training effect",
    "gene_context_ridge": "Gene-context Ridge",
}
MODEL_METRICS = {
    "no_change": (0.004396, None),
    "average_effect": (0.003735, 0.292948),
    "gene_context_ridge": (0.003668, 0.288035),
}


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARTIFACT = PROJECT_ROOT / "artifacts" / "unseen_predictor.joblib"


class VirtualCellService:
    def __init__(self, artifact_path: Path = DEFAULT_ARTIFACT) -> None:
        self.predictor = PerturbationPredictor.load(artifact_path)
        self.cell = VirtualCell(
            "RPE1",
            self.predictor.control_state,
            self.predictor.genes,
        )
        self.experiment = VirtualExperiment(self.cell, self.predictor)

    @property
    def perturbations(self) -> tuple[str, ...]:
        return self.predictor.available_perturbations

    def run_experiment(self, perturbation: str) -> ExperimentResult:
        return self.experiment.run(perturbation)

    def run_model(self, perturbation: str, model: str) -> ExperimentResult:
        if model == "gene_context_ridge":
            return self.experiment.run(perturbation)
        if model == "no_change":
            effect = self.predictor.control_state * 0
        elif model == "average_effect":
            effect = self.predictor.average_effect
        else:
            raise ValueError(f"Unsupported model {model!r}")

        return ExperimentResult.create(
            cell_type=self.cell.cell_type,
            perturbation=perturbation,
            genes=self.cell.genes,
            predicted_effect=effect,
            predicted_state=self.cell.control_state + effect,
        )


@lru_cache(maxsize=1)
def get_virtual_cell_service() -> VirtualCellService:
    return VirtualCellService()
