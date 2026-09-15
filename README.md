# virtual-cell-lab
AI-Based Virtual Cell Lab for predicting cellular state changes under biological perturbations.

## Virtual Cell engine

Train the local model artifact from the downloaded RPE1 dataset:

```bash
source .venv/bin/activate
python -m src.models.train_unseen_predictor
```

Run an artifact-backed virtual experiment:

```bash
python -m src.virtual_cell.demo --perturbation TFAM
```

Generated model artifacts are stored under `artifacts/` and are not committed.
