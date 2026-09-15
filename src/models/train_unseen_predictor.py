import argparse
from pathlib import Path

import joblib
import numpy as np
import scanpy as sc
from sklearn.decomposition import PCA
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .features import build_gene_context_features


DEFAULT_DATASET = Path("data/raw/replogle22rpe1.h5ad")
DEFAULT_OUTPUT = Path("artifacts/unseen_predictor.joblib")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train and save the unseen-perturbation predictor"
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--min-cells", type=int, default=100)
    parser.add_argument("--context-genes", type=int, default=500)
    parser.add_argument("--effect-components", type=int, default=50)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    adata = sc.read_h5ad(args.dataset)
    counts = adata.obs["perturbation"].value_counts().drop("control")
    quality_controlled = counts[counts >= args.min_cells].index
    measured_genes = set(adata.var_names)
    perturbations = [
        perturbation
        for perturbation in quality_controlled
        if perturbation in measured_genes
    ]

    features = build_gene_context_features(
        adata,
        perturbations,
        n_context_genes=args.context_genes,
    )

    labels = adata.obs["perturbation"].to_numpy()
    effects = []
    for perturbation in perturbations:
        positions = np.flatnonzero(labels == perturbation)
        state = np.asarray(adata[positions].X.mean(axis=0)).flatten()
        effects.append(state - features.control_state)
    effect_matrix = np.asarray(effects, dtype=np.float64)

    component_count = min(
        args.effect_components,
        len(perturbations) - 1,
        adata.n_vars,
    )
    effect_pca = PCA(n_components=component_count, random_state=42)
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        reduced_effects = effect_pca.fit_transform(effect_matrix)
    if not np.isfinite(reduced_effects).all():
        raise ValueError("effect PCA produced non-finite values")

    model = make_pipeline(
        StandardScaler(),
        RidgeCV(
            alphas=np.logspace(-2, 4, 13),
            cv=5,
            scoring="neg_mean_squared_error",
        ),
    )
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        model.fit(features.values, reduced_effects)

    bundle = {
        "artifact_version": 1,
        "cell_type": "RPE1",
        "model": model,
        "effect_pca": effect_pca,
        "perturbations": perturbations,
        "context_genes": features.context_genes,
        "context_features": features.values,
        "genes": adata.var_names.tolist(),
        "control_state": features.control_state,
        "training_config": {
            "minimum_cells": args.min_cells,
            "context_genes": args.context_genes,
            "effect_components": component_count,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, args.output, compress=3)

    print(f"Saved predictor artifact: {args.output}")
    print(f"Perturbations: {len(perturbations)}")
    print(f"Genes: {adata.n_vars}")
    print(f"Selected Ridge alpha: {model.named_steps['ridgecv'].alpha_}")


if __name__ == "__main__":
    main()
