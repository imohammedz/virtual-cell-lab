const metrics = [
  { label: "Null MSE", value: "0.004396" },
  { label: "Average-effect MSE", value: "0.003735" },
  { label: "Ridge MSE", value: "0.003668" },
  { label: "Improvement vs. null", value: "16.6%" },
  { label: "Median Pearson", value: "0.288" },
  { label: "Individual wins", value: "59 / 132" },
];

export function EvaluationSummary() {
  return (
    <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
        Held-out evaluation
      </p>
      <div className="mt-5 grid gap-4 sm:grid-cols-3 lg:grid-cols-6">
        {metrics.map((metric) => (
          <div key={metric.label} className="rounded-xl bg-slate-50 p-4">
            <p className="text-xs leading-5 text-slate-500">{metric.label}</p>
            <p className="mt-1 font-mono text-lg font-semibold text-slate-900">
              {metric.value}
            </p>
          </div>
        ))}
      </div>
      <p className="mt-5 max-w-4xl text-sm leading-6 text-slate-600">
        Control-derived gene context contains useful aggregate signal for unseen
        perturbations, but performance is inconsistent across genes. Results are
        computational predictions of transcriptional response—not biological,
        clinical, or wet-lab validation.
      </p>
    </section>
  );
}
