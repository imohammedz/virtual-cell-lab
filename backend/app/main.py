from fastapi import Depends, FastAPI, HTTPException, status

from .schemas import (
    CellResponse,
    ExperimentRequest,
    ExperimentResponse,
    GeneChangeResponse,
    HealthResponse,
    ModelMetadataResponse,
    PerturbationsResponse,
)
from .services import VirtualCellService, get_virtual_cell_service


app = FastAPI(
    title="Virtual Cell Lab API",
    version="0.1.0",
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
        result = service.run_experiment(request.perturbation)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return ExperimentResponse(
        cell_type=result.cell_type,
        perturbation=result.perturbation,
        top_increased_genes=[
            GeneChangeResponse(gene=change.gene, change=change.change)
            for change in result.top_increased_genes()
        ],
        top_decreased_genes=[
            GeneChangeResponse(gene=change.gene, change=change.change)
            for change in result.top_decreased_genes()
        ],
        metadata=ModelMetadataResponse(
            model="Ridge",
            data_type="scRNA-seq",
            prediction_mode="unseen-perturbation",
            training_perturbations=len(service.perturbations),
        ),
    )
