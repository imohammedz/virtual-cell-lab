"use client";

import { useState } from "react";

import type { GeneChange } from "@/types/experiment";

interface ExpressionComparisonProps {
  changes: GeneChange[];
}

export function ExpressionComparison({ changes }: ExpressionComparisonProps) {
  const [selectedGene, setSelectedGene] = useState(changes[0].gene);
  const selected = changes.find((item) => item.gene === selectedGene) ?? changes[0];
  const maximum = Math.max(
    selected.control_expression,
    selected.predicted_expression,
    0.1,
  );

  return (
    <div>
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h3 className="font-semibold text-slate-900">Before vs. predicted after</h3>
          <p className="mt-1 text-sm text-slate-500">
            Canonical log-normalized expression
          </p>
        </div>
        <select
          aria-label="Expression comparison gene"
          value={selectedGene}
          onChange={(event) => setSelectedGene(event.target.value)}
          className="rounded-lg border border-slate-200 bg-white px-3 py-2 font-mono text-sm text-slate-800 outline-none focus:border-teal-500"
        >
          {changes.map((item) => (
            <option key={item.gene} value={item.gene}>
              {item.gene}
            </option>
          ))}
        </select>
      </div>
      <div className="mt-6 grid grid-cols-2 gap-6">
        <ExpressionBar
          label="Control"
          value={selected.control_expression}
          maximum={maximum}
          color="bg-slate-400"
        />
        <ExpressionBar
          label="Predicted"
          value={selected.predicted_expression}
          maximum={maximum}
          color={selected.change >= 0 ? "bg-emerald-500" : "bg-rose-500"}
        />
      </div>
    </div>
  );
}

function ExpressionBar({
  label,
  value,
  maximum,
  color,
}: {
  label: string;
  value: number;
  maximum: number;
  color: string;
}) {
  return (
    <div className="flex h-40 flex-col justify-end">
      <p className="mb-2 text-center font-mono text-sm font-semibold text-slate-700">
        {value.toFixed(3)}
      </p>
      <div className="flex h-28 items-end rounded-lg bg-slate-50 px-5 pt-4">
        <div
          className={`w-full rounded-t-md ${color}`}
          style={{ height: `${Math.max((value / maximum) * 100, 2)}%` }}
        />
      </div>
      <p className="mt-2 text-center text-sm text-slate-500">{label}</p>
    </div>
  );
}
