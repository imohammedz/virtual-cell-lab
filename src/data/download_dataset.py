from pathlib import Path
from urllib.request import urlretrieve

URL = (
    "https://storage.googleapis.com/scperteval/processed/"
    "replogle22rpe1_processed_complete.h5ad"
)

OUTPUT = Path("data/raw/replogle22rpe1.h5ad")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

if OUTPUT.exists():
    print(f"Dataset already exists: {OUTPUT}")
else:
    print("Downloading RPE1 perturbation dataset...")
    urlretrieve(URL, OUTPUT)
    print(f"Saved to: {OUTPUT}")
