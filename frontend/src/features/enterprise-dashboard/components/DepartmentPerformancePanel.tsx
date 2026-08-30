import { useEffect, useState } from "react";
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
    const [departments, setDepartments] = useState<DepartmentAnalytics[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!selectedBranchId) {
            setDepartments([]);
            setError(null);
            setLoading(false);
            return;
        }

        setLoading(true);
        setError(null);

        getDepartmentAnalytics(selectedBranchId)
            .then((response) => {
                setDepartments(response.departments);
            })
            .catch(() => {
                setDepartments([]);
                setError("Unable to load department analytics.");
            })
            .finally(() => {
                setLoading(false);
            });
    }, [selectedBranchId]);

    const getResolutionRate = (department: DepartmentAnalytics) => {
        if (department.total_cases === 0) {
            return 0;
        }

        return (
            (department.resolved_cases / department.total_cases) *
            100
        );
    };

    const getOperationalStatus = (department: DepartmentAnalytics) => {
        const resolutionRate = getResolutionRate(department);

        if (department.total_cases === 0) {
            return {
                label: "No activity",
                className: "text-slate-400",
            };
        }

        if (department.escalation_rate > 0) {
            return {
                label: "Requires attention",
                className: "text-amber-400",
            };
        }

        if (resolutionRate === 100) {
            return {
                label: "Fully resolved",
                className: "text-emerald-400",
            };
        }

        return {
            label: "Active investigations",
            className: "text-blue-400",
        };
    };

    return (
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">
                    Department Performance
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Investigation performance across departments within the
                    selected branch.
                </p>
            </div>

            {!selectedBranchId && (
                <p className="text-sm text-slate-400">
                    Select a branch to view department performance.
                </p>
            )}

            {selectedBranchId && loading && (
                <p className="text-sm text-slate-400">
                    Loading department analytics...
                </p>
            )}

            {selectedBranchId && !loading && error && (
                <p className="text-sm text-red-400">{error}</p>
            )}

            {selectedBranchId &&
                !loading &&
                !error &&
                departments.length === 0 && (
                    <p className="text-sm text-slate-400">
                        No department analytics available for this branch.
                    </p>
                )}

            {selectedBranchId &&
                !loading &&
                !error &&
                departments.length > 0 && (
                    <div className="space-y-4">
                        {departments.map((department) => {
                            const resolutionRate =
                                getResolutionRate(department);

                            const operationalStatus =
                                getOperationalStatus(department);

                            const unresolvedCases = Math.max(
                                department.total_cases -
                                department.resolved_cases,
                                0,
                            );

                            return (
                                <div
                                    key={department.department_id}
                                    className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                                >
                                    <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                                        <div>
                                            <h3 className="text-base font-semibold text-white">
                                                {department.department_name}
                                            </h3>

                                            <p className="mt-1 text-sm text-slate-400">
                                                {department.total_cases}{" "}
                                                {department.total_cases === 1
                                                    ? "total investigation"
                                                    : "total investigations"}
                                            </p>

                                            <p
                                                className={`mt-2 text-sm font-medium ${operationalStatus.className}`}
                                            >
                                                {operationalStatus.label}
                                            </p>
                                        </div>

                                        <div className="text-left lg:text-right">
                                            <p className="text-sm text-slate-400">
                                                Resolution
                                            </p>

                                            <p className="mt-1 text-2xl font-bold text-emerald-400">
                                                {resolutionRate.toFixed(1)}%
                                            </p>
                                        </div>
                                    </div>

                                    <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Total
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-white">
                                                {department.total_cases}
                                            </p>
                                        </div>

                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Resolved
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-emerald-400">
                                                {department.resolved_cases}
                                            </p>
                                        </div>

                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Unresolved
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-blue-400">
                                                {unresolvedCases}
                                            </p>
                                        </div>

                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Escalation
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-amber-400">
                                                {department.escalation_rate.toFixed(
                                                    1,
                                                )}
                                                %
                                            </p>
                                        </div>
                                    </div>

                                    <div className="mt-5">
                                        <div className="mb-2 flex items-center justify-between text-xs">
                                            <span className="text-slate-500">
                                                Resolution performance
                                            </span>

                                            <span className="font-medium text-slate-300">
                                                {resolutionRate.toFixed(1)}%
                                            </span>
                                        </div>

                                        <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                                            <div
                                                className="h-full rounded-full bg-emerald-500 transition-all duration-500"
                                                style={{
                                                    width: `${Math.min(
                                                        resolutionRate,
                                                        100,
                                                    )}%`,
                                                }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
        </section>
    );
}

export default DepartmentPerformancePanel;