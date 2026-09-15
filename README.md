# Virtual Cell Lab

Virtual Cell Lab predicts transcriptional responses to genetic perturbations in
RPE1 cells. The project connects a leakage-safe research workflow to a reusable
Python engine, FastAPI service, and Next.js interface.

## Architecture

```text
Replogle 2022 RPE1 Perturb-seq data
                  |
        model artifact training
                  |
    VirtualCell + VirtualExperiment
                  |
              FastAPI
                  |
          Next.js web interface
```

The application loads a saved model artifact at runtime. Running an experiment
does not retrain the model.

## Setup

Python 3.9 or newer and Node.js are required.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd frontend
npm install
cd ..
```

## Dataset

The project uses the processed Replogle 2022 RPE1 Perturb-seq dataset published
by scPertEval. Download it into the gitignored `data/raw/` directory:

```bash
source .venv/bin/activate
python src/data/download_dataset.py
```

The dataset contains 240,774 cells, 8,749 measured genes, 11,485 control cells,
and 2,016 single-gene perturbations.

## Research workflow

The notebooks document the progression from data inspection to held-out
perturbation evaluation:

1. `01_dataset_exploration.ipynb`
2. `02_control_vs_perturbation.ipynb`
3. `03_baseline_prediction.ipynb`
4. `04_ml_prediction.ipynb`
5. `05_unseen_perturbation_prediction.ipynb`

## Model methodology

The unseen-perturbation model:

1. Retains perturbations with at least 100 measured cells.
2. Retains targets present among the measured genes.
3. Builds 500-dimensional target-gene context vectors from correlations in
   control cells only.
4. Splits perturbations 80/20 by identity.
5. Fits a 50-component PCA using training perturbation effects only.
6. Maps gene context to reduced perturbation effects with Ridge regression.
7. Reconstructs the predicted effect and adds it to the canonical control state.

Held-out evaluation from notebook 05:

| Model | MSE |
| --- | ---: |
| No change | 0.004396 |
| Average training effect | 0.003735 |
| Gene-context Ridge | 0.003668 |

The Ridge model improves aggregate MSE by approximately 16.6% over the null
model. Its median effect-vector Pearson correlation is 0.288, and it beats the
null individually for 59 of 132 held-out perturbations.

## Train the model artifact

After downloading the dataset:

```bash
source .venv/bin/activate
python -m src.models.train_unseen_predictor
```

This creates `artifacts/unseen_predictor.joblib`. Generated artifacts are
gitignored.

## Run a command-line experiment

```bash
source .venv/bin/activate
python -m src.virtual_cell.demo --perturbation TFAM
```

## Run the API

```bash
source .venv/bin/activate
uvicorn backend.app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive documentation
at `http://127.0.0.1:8000/docs`.

Endpoints:

- `GET /health`
- `GET /cell`
- `GET /perturbations`
- `POST /experiments`

## Run the frontend

With the API running:

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000`.

To use another API URL, set `NEXT_PUBLIC_API_URL` before building or starting
the frontend.

## Tests and checks

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v

cd frontend
npm run lint
npm run build
```

## Known limitations

- Results are computational predictions of transcriptional response, not
  biological, clinical, or wet-lab validation.
- Generalization is modest and inconsistent across held-out perturbations.
- The model is limited to RPE1, scRNA-seq expression, and perturbation targets
  represented in the trained artifact.
- Control-cell correlations are a simple biological representation; pathway or
  pretrained gene embeddings may improve future models.
- The system does not model proteins, drugs, lifespan, other cell types, or
  longitudinal changes in individual cells.
