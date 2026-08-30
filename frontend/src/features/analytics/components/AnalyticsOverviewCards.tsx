import {
    AlertTriangle,
    CheckCircle2,
    Gauge,
    ListChecks,
    Percent,
} from "lucide-react";

import StatCard from "../../../shared/components/StatCard";

import type {
    AnalyticsKpis,
} from "../types/analytics.types";

interface AnalyticsOverviewCardsProps {
    kpis: AnalyticsKpis;
}

function AnalyticsOverviewCards({
    kpis,
}: AnalyticsOverviewCardsProps) {
    return (
        <section className="grid gap-5 sm:grid-cols-2 xl:grid-cols-5">
            <StatCard
                title="Total investigations"
                value={kpis.total_cases}
                description="Investigations created in the selected period."
                icon={
                    <ListChecks className="h-6 w-6 text-slate-300" />
                }
            />

            <StatCard
                title="Resolved"
                value={kpis.resolved_cases}
                description="Cases currently marked as resolved."
                icon={
                    <CheckCircle2 className="h-6 w-6 text-green-300" />
                }
            />

            <StatCard
                title="Escalated"
                value={kpis.escalated_cases}
                description="Cases requiring higher-level attention."
                icon={
                    <AlertTriangle className="h-6 w-6 text-red-300" />
                }
            />

            <StatCard
                title="Resolution rate"
                value={kpis.resolution_rate}
                description="Resolved investigations as a percentage of total cases."
                icon={
                    <Percent className="h-6 w-6 text-blue-300" />
                }
            />

            <StatCard
                title="Escalation rate"
                value={kpis.escalation_rate}
                description="Escalated investigations as a percentage of total cases."
                icon={
                    <Gauge className="h-6 w-6 text-amber-300" />
                }
            />
        </section>
    );
}

export default AnalyticsOverviewCards;