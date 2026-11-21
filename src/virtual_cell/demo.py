import argparse
from pathlib import Path

from .cell import VirtualCell
from .experiment import VirtualExperiment
from .predictor import PerturbationPredictor


DEFAULT_ARTIFACT = Path("artifacts/unseen_predictor.joblib")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a virtual RPE1 experiment")
    parser.add_argument("--perturbation", required=True)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--top", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predictor = PerturbationPredictor.load(args.artifact)
    cell = VirtualCell("RPE1", predictor.control_state, predictor.genes)
    result = VirtualExperiment(cell, predictor).run(args.perturbation)

    print("Virtual Cell Lab")
    print(f"\nCell Type:\n{result.cell_type}")
    print(f"\nPerturbation:\n{result.perturbation}")
    print("\nPredicted strongest increases:")
    for change in result.top_increased_genes(args.top):
        print(f"{change.gene:<16} {change.change:+.4f}")
    print("\nPredicted strongest decreases:")
    for change in result.top_decreased_genes(args.top):
        print(f"{change.gene:<16} {change.change:+.4f}")
    print("\nExperiment completed.")


if __name__ == "__main__":
    main()
