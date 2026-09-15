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

## API

Start the FastAPI server after training the model artifact:

```bash
uvicorn backend.app.main:app --reload
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Frontend

With the API running on port 8000, start the web application:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` to select a perturbation and run an experiment.
