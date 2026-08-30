import type {
    EnterpriseKpis,
} from "../../organization-analytics/api/organizationAnalytics.api";

interface ExecutiveKpiCardsProps {
    kpis: EnterpriseKpis;
}

interface KpiCardProps {
    label: string;
    value: string | number;
    description: string;
    valueClassName?: string;
}

function KpiCard({
    label,
    value,
    description,
    valueClassName = "text-white",
}: KpiCardProps) {
    return (
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm font-medium text-slate-400">
                {label}
            </p>

            <p
                className={`mt-3 text-3xl font-bold ${valueClassName}`}
            >
                {value}
            </p>

            <p className="mt-2 text-xs text-slate-500">
                {description}
            </p>
        </div>
    );
}

function ExecutiveKpiCards({
    kpis,
}: ExecutiveKpiCardsProps) {
    return (
        <section>
            <div className="mb-5">
                <h2 className="text-lg font-semibold text-white">
                    Executive Performance
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Organization-level investigation performance
                    and resolution indicators.
                </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <KpiCard
                    label="Total Cases"
                    value={kpis.total_cases}
                    description="Total investigations recorded"
                />

                <KpiCard
                    label="Resolved"
                    value={kpis.resolved_cases}
                    description="Successfully resolved investigations"
                    valueClassName="text-emerald-400"
                />

                <KpiCard
                    label="Waiting"
                    value={kpis.waiting_cases}
                    description="Cases awaiting further action"
                    valueClassName="text-blue-400"
                />

                <KpiCard
                    label="Technical Investigation"
                    value={kpis.technical_investigation_cases}
                    description="Cases requiring technical investigation"
                    valueClassName="text-amber-400"
                />

                <KpiCard
                    label="Escalated"
                    value={kpis.escalated_cases}
                    description="Cases escalated for additional attention"
                    valueClassName="text-red-400"
                />

                <KpiCard
                    label="Resolution Rate"
                    value={`${kpis.resolution_rate.toFixed(1)}%`}
                    description="Percentage of cases resolved"
                    valueClassName="text-emerald-400"
                />

                <KpiCard
                    label="Escalation Rate"
                    value={`${kpis.escalation_rate.toFixed(1)}%`}
                    description="Percentage of cases escalated"
                    valueClassName="text-red-400"
                />
            </div>
        </section>
    );
}

export default ExecutiveKpiCards;