from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    CellResponse,
    ExperimentRequest,
    ExperimentResponse,
    GeneChangeResponse,
    HealthResponse,
    ModelMetadataResponse,
    ModelPredictionResponse,
    PerturbationsResponse,
)
from .services import VirtualCellService, get_virtual_cell_service
from .services import MODEL_METRICS, MODEL_NAMES
from src.virtual_cell.result import GeneChange


app = FastAPI(
    title="Virtual Cell Lab API",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/cell", response_model=CellResponse)
def get_cell(
    service: VirtualCellService = Depends(get_virtual_cell_service),
) -> CellResponse:
    return CellResponse(
        cell_type=service.cell.cell_type,
        gene_count=len(service.cell.genes),
        data_type="scRNA-seq",
    )


@app.get("/perturbations", response_model=PerturbationsResponse)
def get_perturbations(
    service: VirtualCellService = Depends(get_virtual_cell_service),
) -> PerturbationsResponse:
    perturbations = sorted(service.perturbations)
    return PerturbationsResponse(
        count=len(perturbations),
        perturbations=perturbations,
    )


@app.post("/experiments", response_model=ExperimentResponse)
def create_experiment(
    request: ExperimentRequest,
    service: VirtualCellService = Depends(get_virtual_cell_service),
) -> ExperimentResponse:
    try:
        results = {
            model: service.run_model(request.perturbation, model)
            for model in MODEL_NAMES
        }
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    def serialize_prediction(model: str) -> ModelPredictionResponse:
        result = results[model]
        gene_indices = {gene: index for index, gene in enumerate(result.genes)}

        def serialize_change(change: GeneChange) -> GeneChangeResponse:
            gene = change.gene
            index = gene_indices[gene]
            return GeneChangeResponse(
                gene=gene,
                change=change.change,
                control_expression=float(service.cell.control_state[index]),
                predicted_expression=float(result.predicted_state[index]),
            )

        mse, pearson = MODEL_METRICS[model]
        return ModelPredictionResponse(
            model=model,
            top_increased_genes=[
                serialize_change(change) for change in result.top_increased_genes()
            ],
            top_decreased_genes=[
                serialize_change(change) for change in result.top_decreased_genes()
            ],
            metadata=ModelMetadataResponse(
                model=MODEL_NAMES[model],
                data_type="scRNA-seq",
                prediction_mode="unseen-perturbation",
                training_perturbations=len(service.perturbations),
                validation_mse=mse,
                validation_pearson=pearson,
                improvement_vs_null_percent=(MODEL_METRICS["no_change"][0] - mse)
                / MODEL_METRICS["no_change"][0]
                * 100,
            ),
        )

    closest_model = min(MODEL_METRICS, key=lambda model: MODEL_METRICS[model][0])
    return ExperimentResponse(
        cell_type=service.cell.cell_type,
        perturbation=request.perturbation,
        selected_model=request.model,
        closest_model=closest_model,
        predictions=[serialize_prediction(model) for model in MODEL_NAMES],
    )
