"use client";

import { useEffect, useState } from "react";

import { CellSummary } from "@/components/CellSummary";
import { ExperimentForm } from "@/components/ExperimentForm";
import { ExperimentResult } from "@/components/ExperimentResult";
import { EvaluationSummary } from "@/components/EvaluationSummary";
import { getCell, getPerturbations, runExperiment } from "@/lib/api";
import type {
  Cell,
  ExperimentResult as ExperimentResultData,
  ModelId,
} from "@/types/experiment";

export default function Home() {
  const [cell, setCell] = useState<Cell | null>(null);
  const [perturbations, setPerturbations] = useState<string[]>([]);
  const [result, setResult] = useState<ExperimentResultData | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadExperimentOptions() {
      try {
        const [cellResponse, perturbationResponse] = await Promise.all([
          getCell(),
          getPerturbations(),
        ]);
        setCell(cellResponse);
        setPerturbations(perturbationResponse.perturbations);
      } catch (loadError) {
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Unable to connect to the Virtual Cell API.",
        );
      } finally {
        setLoading(false);
      }
    }

    void loadExperimentOptions();
  }, []);

  async function handleRun(perturbation: string, model: ModelId) {
    setRunning(true);
    setError(null);
    try {
      setResult(await runExperiment(perturbation, model));
    } catch (runError) {
      setError(
        runError instanceof Error
          ? runError.message
          : "The virtual experiment could not be completed.",
      );
    } finally {
      setRunning(false);
    }
  }

  return (
    <main className="min-h-screen px-5 py-8 sm:px-8 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <header className="mb-10 flex items-end justify-between gap-6 border-b border-slate-200 pb-7">
          <div>
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-teal-700">
              In silico perturbation research
            </p>
            <h1 className="text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
              Virtual Cell Lab
            </h1>
            <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">
              Explore predicted gene-expression responses in RPE1 cells using a
              model trained on real Perturb-seq measurements.
            </p>
          </div>
          <div className="hidden rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-800 sm:block">
            Model online
          </div>
        </header>

        {error && (
          <div
            className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800"
            role="alert"
          >
            {error}
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
          <section className="space-y-6">
            <CellSummary cell={cell} loading={loading} />
            <ExperimentForm
              perturbations={perturbations}
              disabled={loading || Boolean(error)}
              running={running}
              onRun={handleRun}
            />
          </section>

          <ExperimentResult result={result} running={running} />
        </div>
        <EvaluationSummary />
      </div>
    </main>
  );
}
