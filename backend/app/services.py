from functools import lru_cache
from pathlib import Path

from src.virtual_cell import PerturbationPredictor, VirtualCell, VirtualExperiment
from src.virtual_cell.result import ExperimentResult


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


@lru_cache(maxsize=1)
def get_virtual_cell_service() -> VirtualCellService:
    return VirtualCellService()
