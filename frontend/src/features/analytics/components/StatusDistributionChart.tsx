import Card from "../../../shared/components/Card";
import EmptyState from "../../../shared/components/EmptyState";
import StatusBadge from "../../../shared/components/StatusBadge";

import type {
    StatusDistributionItem,
} from "../types/analytics.types";

interface StatusDistributionChartProps {
    items: StatusDistributionItem[];
}

function StatusDistributionChart({
    items,
}: StatusDistributionChartProps) {
    if (items.length === 0) {
        return (
            <EmptyState
                title="No status distribution available"
                description="No investigations were found for the selected analytics period."
            />
        );
    }

    return (
        <Card>
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Status Distribution
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Breakdown of investigation outcomes in the selected period.
                </p>
            </div>

            <div className="mt-6 space-y-5">
                {items.map((item) => (
                    <div key={item.status}>
                        <div className="flex flex-wrap items-center justify-between gap-3">
                            <StatusBadge
                                status={
                                    item.status as
                                    | "Resolved"
                                    | "Waiting"
                                    | "Technical Investigation"
                                    | "Escalated"
                                }
                            />

                            <div className="text-right">
                                <p className="text-sm font-semibold text-white">
                                    {item.count}
                                </p>

                                <p className="text-xs text-slate-500">
                                    {item.percentage}%
                                </p>
                            </div>
                        </div>

                        <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-800">
                            <div
                                className="h-full rounded-full bg-slate-300 transition-all duration-300"
                                style={{
                                    width: `${item.percentage}%`,
                                }}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </Card>
    );
}

export default StatusDistributionChart;