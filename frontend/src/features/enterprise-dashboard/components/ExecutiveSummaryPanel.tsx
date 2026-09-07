import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import {
    getEnterpriseAnalytics,
    type EnterpriseAnalyticsResponse,
} from "../api/enterpriseAnalyticsApi";

const ORGANIZATION_ID =
    "8909e590-3bc6-4f7f-afc4-8c674b71a538";

function ExecutiveSummaryPanel() {
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
                    "dashboard.operationalSummary.loadError",
                );
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <div className="mb-6">
                    <h2 className="text-lg font-semibold text-white">
                        {t(
                            "dashboard.operationalSummary.title",
                        )}
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        {t(
                            "dashboard.operationalSummary.loading",
                        )}
                    </p>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
                    <div className="h-4 w-3/4 animate-pulse rounded bg-slate-800" />

                    <div className="mt-3 h-4 w-1/2 animate-pulse rounded bg-slate-800" />

                    <div className="mt-3 h-4 w-2/3 animate-pulse rounded bg-slate-800" />
                </div>
            </section>
        );
    }

    if (error || !data) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <div className="mb-6">
                    <h2 className="text-lg font-semibold text-white">
                        {t(
                            "dashboard.operationalSummary.title",
                        )}
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        {t(
                            "dashboard.operationalSummary.insight",
                        )}
                    </p>
                </div>

                <div className="rounded-xl border border-red-900/50 bg-red-950/20 p-5">
                    <p className="text-sm text-red-400">
                        {t(
                            error ??
                            "dashboard.operationalSummary.noData",
                        )}
                    </p>
                </div>
            </section>
        );
    }

    const { kpis } = data;

    const totalCases =
        kpis.total_cases;

    const resolvedCases =
        kpis.resolved_cases;

    const waitingCases =
        kpis.waiting_cases;

    const technicalCases =
        kpis.technical_investigation_cases;

    const escalatedCases =
        kpis.escalated_cases;

    const hasCases =
        totalCases > 0;

    const operationalStatus = !hasCases
        ? t(
            "dashboard.operationalSummary.noInvestigations",
        )
        : escalatedCases > 0
            ? t(
                "dashboard.operationalSummary.attentionRequired",
            )
            : technicalCases > 0
                ? t(
                    "dashboard.operationalSummary.technicalAttention",
                )
                : resolvedCases === totalCases
                    ? t(
                        "dashboard.operationalSummary.allResolved",
                    )
                    : t(
                        "dashboard.operationalSummary.inProgress",
                    );

    const workloadSummary = !hasCases
        ? t(
            "dashboard.operationalSummary.noWorkload",
        )
        : t(
            "dashboard.operationalSummary.workload",
            {
                count: totalCases,
            },
        );

    const resolutionSummary = hasCases
        ? t(
            "dashboard.operationalSummary.position",
            {
                resolved: resolvedCases,
                waiting: waitingCases,
                technical: technicalCases,
                escalated: escalatedCases,
            },
        )
        : t(
            "dashboard.operationalSummary.noResolutionActivity",
        );

    return (
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">
                    {t(
                        "dashboard.operationalSummary.title",
                    )}
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    {t(
                        "dashboard.operationalSummary.subtitle",
                    )}
                </p>
            </div>

            <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
                <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                        {t(
                            "dashboard.operationalSummary.operationalStatus",
                        )}
                    </p>

                    <p className="mt-3 text-base font-semibold text-white">
                        {operationalStatus}
                    </p>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                        {t(
                            "dashboard.operationalSummary.currentWorkload",
                        )}
                    </p>

                    <p className="mt-3 text-base font-semibold text-white">
                        {workloadSummary}
                    </p>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                        {t(
                            "dashboard.operationalSummary.investigationPosition",
                        )}
                    </p>

                    <p className="mt-3 text-base font-semibold text-white">
                        {resolutionSummary}
                    </p>
                </div>
            </div>

            <div className="mt-5 rounded-xl border border-slate-800 bg-slate-950 p-5">
                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                    <div>
                        <p className="text-sm font-medium text-white">
                            {t(
                                "dashboard.operationalSummary.resolutionPerformance",
                            )}
                        </p>

                        <p className="mt-1 text-sm text-slate-400">
                            {t(
                                "dashboard.operationalSummary.resolutionRateDescription",
                                {
                                    rate: kpis.resolution_rate.toFixed(
                                        1,
                                    ),
                                },
                            )}
                        </p>
                    </div>

                    <div className="w-full md:w-64">
                        <div className="mb-2 flex items-center justify-between text-xs">
                            <span className="text-slate-500">
                                {t(
                                    "dashboard.operationalSummary.resolution",
                                )}
                            </span>

                            <span className="font-medium text-emerald-400">
                                {kpis.resolution_rate.toFixed(
                                    1,
                                )}
                                %
                            </span>
                        </div>

                        <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                            <div
                                className="h-full rounded-full bg-emerald-500 transition-all duration-500"
                                style={{
                                    width: `${Math.min(
                                        Math.max(
                                            kpis.resolution_rate,
                                            0,
                                        ),
                                        100,
                                    )}%`,
                                }}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {escalatedCases > 0 && (
                <div className="mt-5 rounded-xl border border-amber-900/50 bg-amber-950/20 p-5">
                    <p className="text-sm font-semibold text-amber-400">
                        {t(
                            "dashboard.operationalSummary.executiveAttention",
                        )}
                    </p>

                    <p className="mt-1 text-sm text-amber-200/80">
                        {t(
                            "dashboard.operationalSummary.escalationAttention",
                            {
                                count: escalatedCases,
                            },
                        )}
                    </p>
                </div>
            )}
        </section>
    );
}

export default ExecutiveSummaryPanel;