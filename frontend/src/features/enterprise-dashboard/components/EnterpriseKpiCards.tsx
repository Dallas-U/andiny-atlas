import { useEffect, useState } from "react";
import {
    getEnterpriseAnalytics,
    type EnterpriseAnalyticsResponse,
} from "../api/enterpriseAnalyticsApi";

const ORGANIZATION_ID = "8909e590-3bc6-4f7f-afc4-8c674b71a538";

function EnterpriseKpiCards() {
    const [data, setData] = useState<EnterpriseAnalyticsResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        getEnterpriseAnalytics(ORGANIZATION_ID)
            .then(setData)
            .catch(() => {
                setError("Unable to load enterprise analytics.");
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <h2 className="text-lg font-semibold text-white">
                    Executive KPI Dashboard
                </h2>

                <p className="mt-2 text-sm text-slate-400">
                    Loading enterprise analytics...
                </p>
            </section>
        );
    }

    if (error || !data) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <h2 className="text-lg font-semibold text-white">
                    Executive KPI Dashboard
                </h2>

                <p className="mt-2 text-sm text-red-400">
                    {error ?? "No enterprise analytics available."}
                </p>
            </section>
        );
    }

    const { kpis } = data;

    const cards = [
        {
            label: "Total Cases",
            value: kpis.total_cases.toString(),
            valueClass: "text-white",
        },
        {
            label: "Resolved Cases",
            value: kpis.resolved_cases.toString(),
            valueClass: "text-emerald-400",
        },
        {
            label: "Waiting Cases",
            value: kpis.waiting_cases.toString(),
            valueClass: "text-yellow-400",
        },
        {
            label: "Technical Investigation",
            value: kpis.technical_investigation_cases.toString(),
            valueClass: "text-blue-400",
        },
        {
            label: "Escalated Cases",
            value: kpis.escalated_cases.toString(),
            valueClass: "text-amber-400",
        },
        {
            label: "Resolution Rate",
            value: `${kpis.resolution_rate.toFixed(1)}%`,
            valueClass: "text-emerald-400",
        },
        {
            label: "Escalation Rate",
            value: `${kpis.escalation_rate.toFixed(1)}%`,
            valueClass: "text-amber-400",
        },
    ];

    return (
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">
                    Executive KPI Dashboard
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Live enterprise metrics from the Atlas executive analytics engine.
                </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {cards.map((card) => (
                    <div
                        key={card.label}
                        className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                    >
                        <p className="text-sm text-slate-400">
                            {card.label}
                        </p>

                        <p
                            className={`mt-2 text-3xl font-bold ${card.valueClass}`}
                        >
                            {card.value}
                        </p>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default EnterpriseKpiCards;