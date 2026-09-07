import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import {
    getDepartmentAnalytics,
    type DepartmentAnalytics,
} from "../api/enterpriseAnalyticsApi";

interface DepartmentPerformancePanelProps {
    selectedBranchId: string | null;
}

function DepartmentPerformancePanel({
    selectedBranchId,
}: DepartmentPerformancePanelProps) {
    const { t } = useTranslation();

    const [departments, setDepartments] =
        useState<DepartmentAnalytics[]>([]);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;

        if (!selectedBranchId) {
            setDepartments([]);
            setError(null);
            setLoading(false);

            return () => {
                isMounted = false;
            };
        }

        setLoading(true);
        setError(null);

        getDepartmentAnalytics(selectedBranchId)
            .then((response) => {
                if (!isMounted) {
                    return;
                }

                setDepartments(
                    response.departments,
                );
            })
            .catch(() => {
                if (!isMounted) {
                    return;
                }

                setDepartments([]);

                setError(
                    "dashboard.departmentPerformance.loadError",
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
    }, [selectedBranchId]);

    function getResolutionRate(
        department: DepartmentAnalytics,
    ): number {
        if (department.total_cases === 0) {
            return 0;
        }

        return (
            (department.resolved_cases /
                department.total_cases) *
            100
        );
    }

    function getOperationalStatus(
        department: DepartmentAnalytics,
    ): {
        label: string;
        className: string;
    } {
        const resolutionRate =
            getResolutionRate(department);

        if (department.total_cases === 0) {
            return {
                label: t(
                    "dashboard.operationalStatus.noActivity",
                ),
                className: "text-slate-400",
            };
        }

        if (department.escalation_rate > 0) {
            return {
                label: t(
                    "dashboard.operationalStatus.requiresAttention",
                ),
                className: "text-amber-400",
            };
        }

        if (resolutionRate === 100) {
            return {
                label: t(
                    "dashboard.operationalStatus.fullyResolved",
                ),
                className: "text-emerald-400",
            };
        }

        return {
            label: t(
                "dashboard.operationalStatus.activeInvestigations",
            ),
            className: "text-blue-400",
        };
    }

    return (
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">
                    {t(
                        "dashboard.departmentPerformance.title",
                    )}
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    {t(
                        "dashboard.departmentPerformance.subtitle",
                    )}
                </p>
            </div>

            {!selectedBranchId && (
                <p className="text-sm text-slate-400">
                    {t(
                        "dashboard.departmentPerformance.selectBranch",
                    )}
                </p>
            )}

            {selectedBranchId && loading && (
                <p className="text-sm text-slate-400">
                    {t(
                        "dashboard.departmentPerformance.loading",
                    )}
                </p>
            )}

            {selectedBranchId &&
                !loading &&
                error && (
                    <p className="text-sm text-red-400">
                        {t(error)}
                    </p>
                )}

            {selectedBranchId &&
                !loading &&
                !error &&
                departments.length === 0 && (
                    <p className="text-sm text-slate-400">
                        {t(
                            "dashboard.departmentPerformance.empty",
                        )}
                    </p>
                )}

            {selectedBranchId &&
                !loading &&
                !error &&
                departments.length > 0 && (
                    <div className="space-y-4">
                        {departments.map(
                            (department) => {
                                const resolutionRate =
                                    getResolutionRate(
                                        department,
                                    );

                                const operationalStatus =
                                    getOperationalStatus(
                                        department,
                                    );

                                const unresolvedCases =
                                    Math.max(
                                        department.total_cases -
                                        department.resolved_cases,
                                        0,
                                    );

                                return (
                                    <div
                                        key={
                                            department.department_id
                                        }
                                        className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                                    >
                                        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                                            <div>
                                                <h3 className="font-semibold text-white">
                                                    {
                                                        department.department_name
                                                    }
                                                </h3>

                                                <p
                                                    className={`mt-2 text-sm font-medium ${operationalStatus.className}`}
                                                >
                                                    {
                                                        operationalStatus.label
                                                    }
                                                </p>
                                            </div>

                                            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                                                <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                                    <p className="text-xs text-slate-500">
                                                        {t(
                                                            "dashboard.departmentPerformance.totalCases",
                                                        )}
                                                    </p>

                                                    <p className="mt-1 text-lg font-semibold text-white">
                                                        {
                                                            department.total_cases
                                                        }
                                                    </p>
                                                </div>

                                                <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                                    <p className="text-xs text-slate-500">
                                                        {t(
                                                            "dashboard.departmentPerformance.resolved",
                                                        )}
                                                    </p>

                                                    <p className="mt-1 text-lg font-semibold text-emerald-400">
                                                        {
                                                            department.resolved_cases
                                                        }
                                                    </p>
                                                </div>

                                                <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                                    <p className="text-xs text-slate-500">
                                                        {t(
                                                            "dashboard.departmentPerformance.unresolved",
                                                        )}
                                                    </p>

                                                    <p className="mt-1 text-lg font-semibold text-slate-200">
                                                        {
                                                            unresolvedCases
                                                        }
                                                    </p>
                                                </div>

                                                <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                                    <p className="text-xs text-slate-500">
                                                        {t(
                                                            "dashboard.departmentPerformance.escalation",
                                                        )}
                                                    </p>

                                                    <p className="mt-1 text-lg font-semibold text-amber-400">
                                                        {department.escalation_rate.toFixed(
                                                            1,
                                                        )}
                                                        %
                                                    </p>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="mt-5">
                                            <div className="mb-2 flex items-center justify-between text-xs">
                                                <span className="text-slate-500">
                                                    {t(
                                                        "dashboard.departmentPerformance.resolutionPerformance",
                                                    )}
                                                </span>

                                                <span className="font-medium text-slate-300">
                                                    {resolutionRate.toFixed(
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
                                                                resolutionRate,
                                                                0,
                                                            ),
                                                            100,
                                                        )}%`,
                                                    }}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                );
                            },
                        )}
                    </div>
                )}
        </section>
    );
}

export default DepartmentPerformancePanel;