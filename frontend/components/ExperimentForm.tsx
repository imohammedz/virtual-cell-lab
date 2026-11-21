"use client";

import { FormEvent, useState } from "react";
import type { ModelId } from "@/types/experiment";

interface ExperimentFormProps {
  perturbations: string[];
  disabled: boolean;
  running: boolean;
  onRun: (perturbation: string, model: ModelId) => Promise<void>;
}

export function ExperimentForm({
  perturbations,
  disabled,
  running,
  onRun,
}: ExperimentFormProps) {
  const [selected, setSelected] = useState("TFAM");
  const [model, setModel] = useState<ModelId>("gene_context_ridge");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (selected) {
      void onRun(selected, model);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-slate-200 bg-slate-950 p-6 text-white shadow-lg shadow-slate-300/40"
    >
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-teal-300">
        Experiment setup
      </p>
      <label
        htmlFor="perturbation"
        className="mt-5 block text-sm font-medium text-slate-200"
      >
        Perturbation
      </label>
      <select
        id="perturbation"
        value={selected}
        onChange={(event) => setSelected(event.target.value)}
        disabled={disabled || running}
        className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none transition focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {perturbations.length === 0 && <option>Loading perturbations...</option>}
        {perturbations.map((perturbation) => (
          <option key={perturbation} value={perturbation}>
            {perturbation}
          </option>
        ))}
      </select>
      <label
        htmlFor="model"
        className="mt-5 block text-sm font-medium text-slate-200"
      >
        Highlighted model
      </label>
      <select
        id="model"
        value={model}
        onChange={(event) => setModel(event.target.value as ModelId)}
        disabled={disabled || running}
        className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none transition focus:border-teal-400 focus:ring-2 focus:ring-teal-400/20 disabled:cursor-not-allowed disabled:opacity-60"
      >
        <option value="gene_context_ridge">Gene-context Ridge</option>
        <option value="average_effect">Average training effect</option>
        <option value="no_change">No change</option>
      </select>
      <button
        type="submit"
        disabled={disabled || running || !selected}
        className="mt-5 w-full rounded-xl bg-teal-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-teal-300 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
      >
        {running ? "Running experiment..." : "Run Virtual Experiment"}
      </button>
      <p className="mt-4 text-xs leading-5 text-slate-400">
        All three predictions are generated from saved artifacts and validated
        baselines. No training occurs when an experiment is run.
      </p>
    </form>
  );
}
