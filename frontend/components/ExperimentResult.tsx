import { ExpressionComparison } from "@/components/ExpressionComparison";
import { GeneChangeChart } from "@/components/GeneChangeChart";
import { GeneChangeList } from "@/components/GeneChangeList";
import type { ExperimentResult as ExperimentResultData } from "@/types/experiment";

interface ExperimentResultProps {
  result: ExperimentResultData | null;
  running: boolean;
}

export function ExperimentResult({ result, running }: ExperimentResultProps) {
  const selectedPrediction = result?.predictions.find(
    (prediction) => prediction.model === result.selected_model,
  );
  const displayedPrediction = selectedPrediction ?? result?.predictions[0];
  const closestPrediction = result?.predictions.find(
    (prediction) => prediction.model === result.closest_model,
  );

  return (
    <section
      className="min-h-[34rem] rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8"
      aria-live="polite"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
            Model comparison
          </p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-950">
            {result ? `${result.perturbation} predictions` : "Awaiting experiment"}
          </h2>
        </div>
        {result && (
          <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-800">
            Complete
          </span>
        )}
      </div>

      {running ? (
        <div className="flex min-h-[25rem] items-center justify-center">
          <div className="text-center">
            <div className="mx-auto size-9 animate-spin rounded-full border-4 border-slate-200 border-t-teal-600" />
            <p className="mt-4 text-sm text-slate-500">Comparing predictions...</p>
          </div>
        </div>
      ) : result && displayedPrediction ? (
        <>
          <div className="mt-6 rounded-xl border border-teal-100 bg-teal-50 p-4 text-sm text-teal-950">
            <strong>Best validated model:</strong>{" "}
            {closestPrediction?.metadata.model}
            <span className="ml-2 text-teal-800">
              Based on held-out validation MSE; this live experiment has no ground
              truth.
            </span>
          </div>
          <div className="mt-6 grid gap-3 md:grid-cols-3">
            {result.predictions.map((prediction) => (
              <div
                key={prediction.model}
                className={`rounded-xl border p-4 ${
                  prediction.model === result.closest_model
                    ? "border-emerald-300 bg-emerald-50"
                    : "border-slate-200 bg-slate-50"
                }`}
              >
                <p className="text-sm font-semibold text-slate-900">
                  {prediction.metadata.model}
                </p>
                <p className="mt-2 font-mono text-lg text-slate-900">
                  MSE {prediction.metadata.validation_mse.toFixed(6)}
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  {prediction.metadata.improvement_vs_null_percent.toFixed(1)}% vs.
                  null
                </p>
              </div>
            ))}
          </div>
          <p className="mt-6 text-sm text-slate-500">
            Highlighting:{" "}
            <strong className="text-slate-800">
              {displayedPrediction.metadata.model}
            </strong>
          </p>
          <div className="mt-3 grid gap-8 border-y border-slate-100 py-7 xl:grid-cols-2">
            <GeneChangeList
              title="Increased genes"
              direction="increase"
              changes={displayedPrediction.top_increased_genes}
            />
            <GeneChangeList
              title="Decreased genes"
              direction="decrease"
              changes={displayedPrediction.top_decreased_genes}
            />
          </div>
          <div className="mt-8 grid gap-8 border-b border-slate-100 pb-8 xl:grid-cols-2">
            <GeneChangeChart
              increased={displayedPrediction.top_increased_genes}
              decreased={displayedPrediction.top_decreased_genes}
            />
            <ExpressionComparison
              changes={[
                ...displayedPrediction.top_increased_genes.slice(0, 3),
                ...displayedPrediction.top_decreased_genes.slice(0, 3),
              ]}
            />
          </div>
          <dl className="mt-7 grid gap-5 text-sm sm:grid-cols-3">
            <Metadata
              label="Highlighted model"
              value={displayedPrediction.metadata.model}
            />
            <Metadata
              label="Prediction mode"
              value={displayedPrediction.metadata.prediction_mode.replace("-", " ")}
            />
            <Metadata
              label="Validation MSE"
              value={displayedPrediction.metadata.validation_mse.toFixed(6)}
            />
          </dl>
        </>
      ) : (
        <div className="flex min-h-[25rem] items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50/70">
          <div className="max-w-xs px-5 text-center">
            <div className="mx-auto flex size-12 items-center justify-center rounded-full bg-teal-100 text-xl text-teal-700">
              ◇
            </div>
            <p className="mt-4 font-medium text-slate-800">
              Select a perturbation to begin
            </p>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              All three model predictions will appear here for comparison.
            </p>
          </div>
        </div>
      )}
    </section>
  );
}

function Metadata({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-slate-500">{label}</dt>
      <dd className="mt-1 font-semibold capitalize text-slate-900">{value}</dd>
    </div>
  );
}
