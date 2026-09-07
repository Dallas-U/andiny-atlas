import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import {
    getEnterpriseAnalytics,
    type EnterpriseAnalyticsResponse,
} from "../api/enterpriseAnalyticsApi";

const ORGANIZATION_ID =
    "8909e590-3bc6-4f7f-afc4-8c674b71a538";

function EnterpriseKpiCards() {
    const { t } = useTranslation();

    const [data, setData] =
        useState<EnterpriseAnalyticsResponse | null>(
            null,
        );

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<string | null>(null);

    useEffect(() => {
        getEnterpriseAnalytics(ORGANIZATION_ID)
            .then(setData)
            .catch(() => {
                setError(
                    "dashboard.executiveKpi.loadError",
                );
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <h2 className="text-lg font-semibold text-white">
                    {t(
                        "dashboard.executiveKpi.title",
                    )}
                </h2>

                <p className="mt-2 text-sm text-slate-400">
                    {t(
                        "dashboard.executiveKpi.loading",
                    )}
                </p>
            </section>
        );
    }

    if (error || !data) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <h2 className="text-lg font-semibold text-white">
                    {t(
                        "dashboard.executiveKpi.title",
                    )}
                </h2>

                <p className="mt-2 text-sm text-red-400">
                    {t(
                        error ??
                        "dashboard.executiveKpi.noData",
                    )}
                </p>
            </section>
        );
    }

    const { kpis } = data;

    const cards = [
        {
            label: t("dashboard.kpi.totalCases"),
            value: kpis.total_cases.toString(),
            valueClass: "text-white",
        },
        {
            label: t("dashboard.kpi.resolvedCases"),
            value: kpis.resolved_cases.toString(),
            valueClass: "text-emerald-400",
        },
        {
            label: t("dashboard.kpi.waitingCases"),
            value: kpis.waiting_cases.toString(),
            valueClass: "text-yellow-400",
        },
        {
            label: t(
                "dashboard.kpi.technicalInvestigation",
            ),
            value:
                kpis.technical_investigation_cases.toString(),
            valueClass: "text-blue-400",
        },
        {
            label: t("dashboard.kpi.escalatedCases"),
            value: kpis.escalated_cases.toString(),
            valueClass: "text-amber-400",
        },
        {
            label: t("dashboard.kpi.resolutionRate"),
            value: `${kpis.resolution_rate.toFixed(1)}%`,
            valueClass: "text-emerald-400",
        },
        {
            label: t("dashboard.kpi.escalationRate"),
            value: `${kpis.escalation_rate.toFixed(1)}%`,
            valueClass: "text-amber-400",
        },
    ];

    return (
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">
                    {t(
                        "dashboard.executiveKpi.title",
                    )}
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    {t(
                        "dashboard.executiveKpi.subtitle",
                    )}
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