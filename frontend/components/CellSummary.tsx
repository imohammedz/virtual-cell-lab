import type { Cell } from "@/types/experiment";

interface CellSummaryProps {
  cell: Cell | null;
  loading: boolean;
}

export function CellSummary({ cell, loading }: CellSummaryProps) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
        Cell model
      </p>
      <div className="mt-5 grid grid-cols-2 gap-4">
        <SummaryValue label="Cell type" value={loading ? "Loading..." : cell?.cell_type} />
        <SummaryValue
          label="Data modality"
          value={loading ? "Loading..." : cell?.data_type}
        />
        <SummaryValue
          label="Measured genes"
          value={loading ? "—" : cell?.gene_count.toLocaleString()}
        />
        <SummaryValue label="Organism" value="Human" />
      </div>
    </div>
  );
}

function SummaryValue({
  label,
  value,
}: {
  label: string;
  value: string | undefined;
}) {
  return (
    <div>
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-1 text-lg font-semibold text-slate-900">{value ?? "—"}</p>
    </div>
  );
}
