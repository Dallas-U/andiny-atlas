import { useEffect, useState } from "react";

import {
    getEnterpriseAnalytics,
    type EnterpriseKpis,
} from "../../enterprise-dashboard/api/enterpriseAnalyticsApi";

interface EnterpriseExecutiveSummaryProps {
    organizationId: string;
}

function EnterpriseExecutiveSummary({
    organizationId,
}: EnterpriseExecutiveSummaryProps) {
    const [kpis, setKpis] =
        useState<EnterpriseKpis | null>(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;

        setLoading(true);
        setError(null);

        getEnterpriseAnalytics(organizationId)
            .then((response) => {
                if (!isMounted) {
                    return;
                }

                setKpis(response.kpis);
            })
            .catch(() => {
                if (!isMounted) {
                    return;
                }

                setKpis(null);
                setError(
                    "Unable to load executive analytics.",
                );
            })
            .finally(() => {
                if (isMounted) {
                    setLoading(false);
                }
            });

        return () => {
            isMounted = false;
        };
    }, [organizationId]);

    if (loading) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-sm text-slate-400">
                    Loading executive analytics...
                </p>
            </section>
        );
    }

    if (error) {
        return (
            <section className="rounded-2xl border border-red-900 bg-slate-900 p-6">
                <p className="text-sm text-red-400">
                    {error}
                </p>
            </section>
        );
    }

    if (!kpis) {
        return null;
    }

    const cards = [
        {
            label: "Total Cases",
            value: kpis.total_cases,
            className: "text-white",
        },
        {
            label: "Resolved Cases",
            value: kpis.resolved_cases,
            className: "text-emerald-400",
        },
        {
            label: "Waiting Cases",
            value: kpis.waiting_cases,
            className: "text-amber-400",
        },
        {
            label: "Technical Investigation",
            value: kpis.technical_investigation_cases,
            className: "text-blue-400",
        },
        {
            label: "Escalated Cases",
            value: kpis.escalated_cases,
            className: "text-red-400",
        },
        {
            label: "Resolution Rate",
            value: `${kpis.resolution_rate.toFixed(1)}%`,
            className: "text-emerald-400",
        },
        {
            label: "Escalation Rate",
            value: `${kpis.escalation_rate.toFixed(1)}%`,
            className: "text-amber-400",
        },
    ];

    return (
        <section className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Executive KPI Dashboard
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Live enterprise metrics from the Atlas
                    executive analytics engine.
                </p>
            </div>

            <div className="grid grid-cols-2 gap-4 md:grid-cols-4 xl:grid-cols-7">
                {cards.map((card) => (
                    <div
                        key={card.label}
                        className="rounded-xl border border-slate-800 bg-slate-900 p-4"
                    >
                        <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                            {card.label}
                        </p>

                        <p
                            className={`mt-2 text-2xl font-bold ${card.className}`}
                        >
                            {card.value}
                        </p>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default EnterpriseExecutiveSummary;