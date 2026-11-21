from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import joblib
import numpy as np
from numpy.typing import NDArray


class PerturbationPredictor:
    """Artifact-backed predictor for perturbation effects."""

    def __init__(
        self,
        *,
        model: Any,
        effect_pca: Any,
        perturbations: list[str],
        context_features: NDArray[np.float64],
        genes: list[str],
        control_state: NDArray[np.float64],
        average_effect: NDArray[np.float64],
    ) -> None:
        features = np.asarray(context_features, dtype=np.float64)
        state = np.asarray(control_state, dtype=np.float64).reshape(-1)
        average = np.asarray(average_effect, dtype=np.float64).reshape(-1)

        if features.shape[0] != len(perturbations):
            raise ValueError("context feature rows must match perturbations")
        if state.size != len(genes):
            raise ValueError("control state must match genes")
        if average.size != len(genes):
            raise ValueError("average effect must match genes")
        if len(set(perturbations)) != len(perturbations):
            raise ValueError("perturbations must be unique")
        if (
            not np.isfinite(features).all()
            or not np.isfinite(state).all()
            or not np.isfinite(average).all()
        ):
            raise ValueError("artifact arrays must contain only finite values")

        self._model = model
        self._effect_pca = effect_pca
        self._features = features
        self._perturbation_indices = {
            perturbation: index for index, perturbation in enumerate(perturbations)
        }
        self.genes = tuple(genes)
        self.control_state = state
        self.average_effect = average

    @classmethod
    def load(cls, path: str | Path) -> "PerturbationPredictor":
        artifact_path = Path(path)
        if not artifact_path.is_file():
            raise FileNotFoundError(f"Predictor artifact not found: {artifact_path}")

        bundle = joblib.load(artifact_path)
        if not isinstance(bundle, Mapping):
            raise ValueError("predictor artifact must contain a mapping")

        required = {
            "model",
            "effect_pca",
            "perturbations",
            "context_features",
            "genes",
            "control_state",
            "average_effect",
        }
        missing = required.difference(bundle)
        if missing:
            raise ValueError(
                f"predictor artifact is missing fields: {', '.join(sorted(missing))}"
            )

        return cls(
            model=bundle["model"],
            effect_pca=bundle["effect_pca"],
            perturbations=list(bundle["perturbations"]),
            context_features=bundle["context_features"],
            genes=list(bundle["genes"]),
            control_state=bundle["control_state"],
            average_effect=bundle["average_effect"],
        )

    @property
    def available_perturbations(self) -> tuple[str, ...]:
        return tuple(self._perturbation_indices)

    def predict(self, perturbation: str) -> NDArray[np.float64]:
        try:
            index = self._perturbation_indices[perturbation]
        except KeyError as error:
            raise ValueError(
                f"Unsupported perturbation {perturbation!r}; "
                f"{len(self._perturbation_indices)} perturbations are available"
            ) from error

        with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
            reduced_effect = self._model.predict(self._features[[index]])
            effect = np.asarray(
                self._effect_pca.inverse_transform(reduced_effect)[0],
                dtype=np.float64,
            )
        if effect.shape != self.control_state.shape or not np.isfinite(effect).all():
            raise ValueError("predictor produced an invalid effect vector")
        return effect
