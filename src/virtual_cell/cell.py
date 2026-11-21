from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class VirtualCell:
    """Canonical expression state for a cell type."""

    cell_type: str
    control_state: NDArray[np.float64]
    genes: tuple[str, ...]

    def __init__(
        self,
        cell_type: str,
        control_state: Sequence[float],
        genes: Sequence[str],
    ) -> None:
        state = np.asarray(control_state, dtype=np.float64).reshape(-1).copy()
        gene_names = tuple(genes)

        if not cell_type.strip():
            raise ValueError("cell_type must not be empty")
        if state.size != len(gene_names):
            raise ValueError("control_state and genes must have the same length")
        if len(set(gene_names)) != len(gene_names):
            raise ValueError("genes must be unique")
        if not np.isfinite(state).all():
            raise ValueError("control_state must contain only finite values")

        state.setflags(write=False)
        object.__setattr__(self, "cell_type", cell_type)
        object.__setattr__(self, "control_state", state)
        object.__setattr__(self, "genes", gene_names)
