import { ExpressionComparison } from "@/components/ExpressionComparison";
import { GeneChangeChart } from "@/components/GeneChangeChart";
import { GeneChangeList } from "@/components/GeneChangeList";
import type { ExperimentResult as ExperimentResultData } from "@/types/experiment";

interface ExperimentResultProps {
  result: ExperimentResultData | null;
  running: boolean;
}

export function ExperimentResult({ result, running }: ExperimentResultProps) {
  return (
    <section
      className="min-h-[34rem] rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8"
      aria-live="polite"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
            Predicted cellular response
          </p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-950">
            {result ? `${result.perturbation} perturbation` : "Awaiting experiment"}
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
            <p className="mt-4 text-sm text-slate-500">Predicting cell state...</p>
          </div>
        </div>
      ) : result ? (
        <>
          <div className="mt-8 grid gap-8 border-y border-slate-100 py-7 xl:grid-cols-2">
            <GeneChangeList
              title="Increased genes"
              direction="increase"
              changes={result.top_increased_genes}
            />
            <GeneChangeList
              title="Decreased genes"
              direction="decrease"
              changes={result.top_decreased_genes}
            />
          </div>
          <div className="mt-8 grid gap-8 border-b border-slate-100 pb-8 xl:grid-cols-2">
            <GeneChangeChart
              increased={result.top_increased_genes}
              decreased={result.top_decreased_genes}
            />
            <ExpressionComparison
              changes={[
                ...result.top_increased_genes.slice(0, 3),
                ...result.top_decreased_genes.slice(0, 3),
              ]}
            />
          </div>
          <dl className="mt-7 grid gap-5 text-sm sm:grid-cols-3">
            <Metadata label="Model" value={result.metadata.model} />
            <Metadata
              label="Prediction mode"
              value={result.metadata.prediction_mode.replace("-", " ")}
            />
            <Metadata
              label="Training perturbations"
              value={result.metadata.training_perturbations.toLocaleString()}
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
              The predicted expression response and strongest gene changes will
              appear here.
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
