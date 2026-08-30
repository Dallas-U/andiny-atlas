import Card from "../../../shared/components/Card";
import EmptyState from "../../../shared/components/EmptyState";

import type {
    InvestigationTrendItem,
} from "../types/analytics.types";

interface InvestigationTrendChartProps {
    items: InvestigationTrendItem[];
}

function InvestigationTrendChart({
    items,
}: InvestigationTrendChartProps) {
    if (items.length === 0) {
        return (
            <EmptyState
                title="No trend data available"
                description="No investigations were found for the selected analytics period."
            />
        );
    }

    const maximumCount = Math.max(
        ...items.map((item) => item.count),
        1,
    );

    return (
        <Card>
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Investigation Trend
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Investigation volume grouped by the selected interval.
                </p>
            </div>

            <div className="mt-6 space-y-5">
                {items.map((item) => {
                    const widthPercentage =
                        (item.count / maximumCount) * 100;

                    return (
                        <div key={item.period}>
                            <div className="flex items-center justify-between gap-4">
                                <p className="text-sm font-medium text-slate-300">
                                    {item.period}
                                </p>

                                <p className="text-sm font-semibold text-white">
                                    {item.count}
                                </p>
                            </div>

                            <div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-800">
                                <div
                                    className="h-full rounded-full bg-indigo-500 transition-all duration-300"
                                    style={{
                                        width: `${widthPercentage}%`,
                                    }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>
        </Card>
    );
}

export default InvestigationTrendChart;