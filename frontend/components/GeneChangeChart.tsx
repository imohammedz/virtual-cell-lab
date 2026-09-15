import type { GeneChange } from "@/types/experiment";

interface GeneChangeChartProps {
  increased: GeneChange[];
  decreased: GeneChange[];
}

export function GeneChangeChart({
  increased,
  decreased,
}: GeneChangeChartProps) {
  const changes = [...increased.slice(0, 5), ...decreased.slice(0, 5)].sort(
    (left, right) => right.change - left.change,
  );
  const maximum = Math.max(...changes.map((item) => Math.abs(item.change)), 1);

  return (
    <div>
      <h3 className="font-semibold text-slate-900">Top predicted changes</h3>
      <p className="mt-1 text-sm text-slate-500">
        Signed change from the canonical control state
      </p>
      <div className="mt-5 space-y-2.5">
        {changes.map((item) => {
          const width = (Math.abs(item.change) / maximum) * 50;
          const increasedExpression = item.change >= 0;

          return (
            <div
              key={item.gene}
              className="grid grid-cols-[4.5rem_1fr_4.5rem] items-center gap-3"
            >
              <span className="truncate font-mono text-xs font-semibold text-slate-700">
                {item.gene}
              </span>
              <div className="relative h-5">
                <div className="absolute inset-y-0 left-1/2 w-px bg-slate-300" />
                <div
                  className={`absolute top-1/2 h-2.5 -translate-y-1/2 rounded-full ${
                    increasedExpression ? "bg-emerald-500" : "bg-rose-500"
                  }`}
                  style={
                    increasedExpression
                      ? { left: "50%", width: `${width}%` }
                      : { right: "50%", width: `${width}%` }
                  }
                />
              </div>
              <span
                className={`text-right font-mono text-xs font-semibold ${
                  increasedExpression ? "text-emerald-700" : "text-rose-700"
                }`}
              >
                {item.change > 0 ? "+" : ""}
                {item.change.toFixed(4)}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
