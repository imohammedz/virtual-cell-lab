export interface Cell {
  cell_type: string;
  gene_count: number;
  data_type: string;
}

export interface PerturbationsResponse {
  count: number;
  perturbations: string[];
}

export interface GeneChange {
  gene: string;
  change: number;
  control_expression: number;
  predicted_expression: number;
}

export interface ModelMetadata {
  model: string;
  data_type: string;
  prediction_mode: string;
  training_perturbations: number;
  validation_mse: number;
  validation_pearson: number | null;
  improvement_vs_null_percent: number;
}

export type ModelId = "no_change" | "average_effect" | "gene_context_ridge";

export interface ModelPrediction {
  model: ModelId;
  top_increased_genes: GeneChange[];
  top_decreased_genes: GeneChange[];
  metadata: ModelMetadata;
}

export interface ExperimentResult {
  cell_type: string;
  perturbation: string;
  selected_model: ModelId;
  closest_model: ModelId;
  predictions: ModelPrediction[];
}
