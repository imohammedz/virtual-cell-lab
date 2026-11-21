from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class GeneChange:
    gene: str
    change: float


@dataclass(frozen=True)
class ExperimentResult:
    cell_type: str
    perturbation: str
    genes: tuple[str, ...]
    predicted_state: NDArray[np.float64]
    predicted_effect: NDArray[np.float64]

    @classmethod
    def create(
        cls,
        *,
        cell_type: str,
        perturbation: str,
        genes: Sequence[str],
        predicted_state: Sequence[float],
        predicted_effect: Sequence[float],
    ) -> "ExperimentResult":
        gene_names = tuple(genes)
        state = np.asarray(predicted_state, dtype=np.float64).reshape(-1).copy()
        effect = np.asarray(predicted_effect, dtype=np.float64).reshape(-1).copy()

        if state.size != len(gene_names) or effect.size != len(gene_names):
            raise ValueError("genes, predicted_state, and predicted_effect must align")
        if not np.isfinite(state).all() or not np.isfinite(effect).all():
            raise ValueError("predictions must contain only finite values")

        state.setflags(write=False)
        effect.setflags(write=False)
        return cls(
            cell_type=cell_type,
            perturbation=perturbation,
            genes=gene_names,
            predicted_state=state,
            predicted_effect=effect,
        )

    def top_increased_genes(self, limit: int = 10) -> list[GeneChange]:
        self._validate_limit(limit)
        indices = np.argsort(self.predicted_effect)[-limit:][::-1]
        return [
            GeneChange(self.genes[index], float(self.predicted_effect[index]))
            for index in indices
        ]

    def top_decreased_genes(self, limit: int = 10) -> list[GeneChange]:
        self._validate_limit(limit)
        indices = np.argsort(self.predicted_effect)[:limit]
        return [
            GeneChange(self.genes[index], float(self.predicted_effect[index]))
            for index in indices
        ]

    def _validate_limit(self, limit: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        if limit > len(self.genes):
            raise ValueError("limit cannot exceed the number of genes")
