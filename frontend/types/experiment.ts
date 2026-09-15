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
}

export interface ModelMetadata {
  model: string;
  data_type: string;
  prediction_mode: string;
  training_perturbations: number;
}

export interface ExperimentResult {
  cell_type: string;
  perturbation: string;
  top_increased_genes: GeneChange[];
  top_decreased_genes: GeneChange[];
  metadata: ModelMetadata;
}
