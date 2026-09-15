import type { GeneChange } from "@/types/experiment";

interface GeneChangeListProps {
  title: string;
  direction: "increase" | "decrease";
  changes: GeneChange[];
}

export function GeneChangeList({
  title,
  direction,
  changes,
}: GeneChangeListProps) {
  const positive = direction === "increase";
  const maxChange = Math.max(...changes.map((item) => Math.abs(item.change)), 1);

  return (
    <div>
      <div className="mb-4 flex items-center gap-2">
        <span
          className={`flex size-7 items-center justify-center rounded-full text-sm font-bold ${
            positive
              ? "bg-emerald-100 text-emerald-700"
              : "bg-rose-100 text-rose-700"
          }`}
          aria-hidden="true"
        >
          {positive ? "↑" : "↓"}
        </span>
        <h3 className="font-semibold text-slate-900">{title}</h3>
      </div>
      <ol className="space-y-3">
        {changes.slice(0, 5).map((item) => (
          <li key={item.gene} className="grid grid-cols-[5rem_1fr_auto] items-center gap-3">
            <span className="font-mono text-sm font-semibold text-slate-800">
              {item.gene}
            </span>
            <span className="h-2 overflow-hidden rounded-full bg-slate-100">
              <span
                className={`block h-full rounded-full ${
                  positive ? "bg-emerald-500" : "bg-rose-500"
                }`}
                style={{ width: `${(Math.abs(item.change) / maxChange) * 100}%` }}
              />
            </span>
            <span
              className={`font-mono text-sm font-semibold ${
                positive ? "text-emerald-700" : "text-rose-700"
              }`}
            >
              {item.change > 0 ? "+" : ""}
              {item.change.toFixed(4)}
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}
