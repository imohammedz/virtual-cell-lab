from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class CellResponse(BaseModel):
    cell_type: str
    gene_count: int
    data_type: str


class PerturbationsResponse(BaseModel):
    count: int
    perturbations: list[str]


class ExperimentRequest(BaseModel):
    perturbation: str = Field(min_length=1)


class GeneChangeResponse(BaseModel):
    gene: str
    change: float


class ModelMetadataResponse(BaseModel):
    model: str
    data_type: str
    prediction_mode: str
    training_perturbations: int


class ExperimentResponse(BaseModel):
    cell_type: str
    perturbation: str
    top_increased_genes: list[GeneChangeResponse]
    top_decreased_genes: list[GeneChangeResponse]
    metadata: ModelMetadataResponse
