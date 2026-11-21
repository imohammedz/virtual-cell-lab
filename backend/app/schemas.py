from typing import Literal, Optional

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
    model: Literal["no_change", "average_effect", "gene_context_ridge"] = (
        "gene_context_ridge"
    )


class GeneChangeResponse(BaseModel):
    gene: str
    change: float
    control_expression: float
    predicted_expression: float


class ModelMetadataResponse(BaseModel):
    model: str
    data_type: str
    prediction_mode: str
    training_perturbations: int
    validation_mse: float
    validation_pearson: Optional[float] = None
    improvement_vs_null_percent: float


class ModelPredictionResponse(BaseModel):
    model: str
    top_increased_genes: list[GeneChangeResponse]
    top_decreased_genes: list[GeneChangeResponse]
    metadata: ModelMetadataResponse


class ExperimentResponse(BaseModel):
    cell_type: str
    perturbation: str
    selected_model: str
    closest_model: str
    predictions: list[ModelPredictionResponse]
