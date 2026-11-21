from dataclasses import dataclass

import anndata as ad
import numpy as np
from numpy.typing import NDArray
from scipy import sparse


@dataclass(frozen=True)
class GeneContextFeatures:
    perturbations: list[str]
    context_genes: list[str]
    values: NDArray[np.float64]
    control_state: NDArray[np.float64]


def build_gene_context_features(
    adata: ad.AnnData,
    perturbations: list[str],
    *,
    n_context_genes: int = 500,
) -> GeneContextFeatures:
    missing = sorted(set(perturbations).difference(adata.var_names))
    if missing:
        raise ValueError(
            f"{len(missing)} perturbation targets are not measured genes"
        )

    control = adata[adata.obs["perturbation"] == "control"]
    if control.n_obs == 0:
        raise ValueError("dataset does not contain control cells")

    control_x = control.X
    control_state = np.asarray(control_x.mean(axis=0)).flatten()
    if sparse.issparse(control_x):
        squared_mean = np.asarray(control_x.power(2).mean(axis=0)).flatten()
    else:
        squared_mean = np.mean(np.square(control_x), axis=0)
    variance = np.maximum(squared_mean - np.square(control_state), 0)

    context_count = min(n_context_genes, adata.n_vars)
    context_indices = np.argsort(variance)[-context_count:][::-1]
    target_indices = adata.var_names.get_indexer(perturbations)

    context_expression = _dense(control_x[:, context_indices])
    target_expression = _dense(control_x[:, target_indices])
    context_z = _standardize_columns(context_expression)
    target_z = _standardize_columns(target_expression)

    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        values = target_z.T @ context_z / control.n_obs
    if not np.isfinite(values).all():
        raise ValueError("gene-context calculation produced non-finite values")

    return GeneContextFeatures(
        perturbations=perturbations,
        context_genes=adata.var_names[context_indices].tolist(),
        values=values,
        control_state=control_state,
    )


def _dense(matrix: object) -> NDArray[np.float64]:
    if sparse.issparse(matrix):
        matrix = matrix.toarray()
    return np.asarray(matrix, dtype=np.float64)


def _standardize_columns(values: NDArray[np.float64]) -> NDArray[np.float64]:
    standard_deviation = values.std(axis=0)
    standard_deviation[standard_deviation == 0] = 1
    standardized = (values - values.mean(axis=0)) / standard_deviation
    if not np.isfinite(standardized).all():
        raise ValueError("standardization produced non-finite values")
    return standardized
