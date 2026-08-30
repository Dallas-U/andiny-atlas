import { useEffect, useState } from "react";

import {
    getBranchAnalytics,
    type BranchAnalytics,
} from "../api/enterpriseAnalyticsApi";

interface BranchPerformancePanelProps {
    organizationId: string;
    selectedBranchId: string | null;
    onSelectBranch: (branchId: string) => void;
}

function BranchPerformancePanel({
    organizationId,
    selectedBranchId,
    onSelectBranch,
}: BranchPerformancePanelProps) {
    const [branches, setBranches] = useState<BranchAnalytics[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;

        setLoading(true);
        setError(null);

        getBranchAnalytics(organizationId)
            .then((response) => {
                if (!isMounted) {
                    return;
                }

                setBranches(response.branches);

                if (
                    response.branches.length > 0 &&
                    !selectedBranchId
                ) {
                    onSelectBranch(response.branches[0].branch_id);
                }
            })
            .catch(() => {
                if (!isMounted) {
                    return;
                }

                setBranches([]);
                setError("Unable to load branch analytics.");
            })
            .finally(() => {
                if (isMounted) {
                    setLoading(false);
                }
            });

        return () => {
            isMounted = false;
        };
    }, [organizationId, onSelectBranch, selectedBranchId]);

    const getResolutionRate = (
        branch: BranchAnalytics,
    ): number => {
        if (branch.total_cases === 0) {
            return 0;
        }

        return (
            (branch.resolved_cases / branch.total_cases) *
            100
        );
    };

    const getOperationalStatus = (
        branch: BranchAnalytics,
    ) => {
        const resolutionRate =
            getResolutionRate(branch);

        if (branch.total_cases === 0) {
            return {
                label: "No activity",
                className: "text-slate-400",
            };
        }

        if (branch.escalation_rate > 0) {
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
                    Branch Performance
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Comparative investigation performance across
                    enterprise branches.
                </p>
            </div>

            {loading && (
                <p className="text-sm text-slate-400">
                    Loading branch analytics...
                </p>
            )}

            {!loading && error && (
                <p className="text-sm text-red-400">
                    {error}
                </p>
            )}

            {!loading &&
                !error &&
                branches.length === 0 && (
                    <p className="text-sm text-slate-400">
                        No branch analytics available.
                    </p>
                )}

            {!loading &&
                !error &&
                branches.length > 0 && (
                    <div className="space-y-4">
                        {branches.map((branch) => {
                            const resolutionRate =
                                getResolutionRate(branch);

                            const operationalStatus =
                                getOperationalStatus(branch);

                            const isSelected =
                                selectedBranchId ===
                                branch.branch_id;

                            const unresolvedCases =
                                Math.max(
                                    branch.total_cases -
                                    branch.resolved_cases,
                                    0,
                                );

                            return (
                                <button
                                    key={branch.branch_id}
                                    type="button"
                                    onClick={() =>
                                        onSelectBranch(
                                            branch.branch_id,
                                        )
                                    }
                                    className={`block w-full rounded-xl border p-5 text-left transition ${isSelected
                                            ? "border-blue-500 bg-slate-950 ring-1 ring-blue-500/30"
                                            : "border-slate-800 bg-slate-950 hover:border-slate-700"
                                        }`}
                                >
                                    <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                                        <div>
                                            <h3 className="text-base font-semibold text-white">
                                                {
                                                    branch.branch_name
                                                }
                                            </h3>

                                            <p className="mt-1 text-sm text-slate-400">
                                                {
                                                    branch.total_cases
                                                }{" "}
                                                {branch.total_cases ===
                                                    1
                                                    ? "total investigation"
                                                    : "total investigations"}
                                            </p>

                                            <p
                                                className={`mt-2 text-sm font-medium ${operationalStatus.className}`}
                                            >
                                                {
                                                    operationalStatus.label
                                                }
                                            </p>

                                            {isSelected && (
                                                <p className="mt-2 text-xs font-medium text-blue-400">
                                                    Selected branch
                                                </p>
                                            )}
                                        </div>

                                        <div className="text-left lg:text-right">
                                            <p className="text-sm text-slate-400">
                                                Resolution
                                            </p>

                                            <p className="mt-1 text-2xl font-bold text-emerald-400">
                                                {resolutionRate.toFixed(
                                                    1,
                                                )}
                                                %
                                            </p>
                                        </div>
                                    </div>

                                    <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Total
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-white">
                                                {
                                                    branch.total_cases
                                                }
                                            </p>
                                        </div>

                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Resolved
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-emerald-400">
                                                {
                                                    branch.resolved_cases
                                                }
                                            </p>
                                        </div>

                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Unresolved
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-blue-400">
                                                {
                                                    unresolvedCases
                                                }
                                            </p>
                                        </div>

                                        <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                            <p className="text-xs text-slate-500">
                                                Escalation
                                            </p>

                                            <p className="mt-1 text-lg font-semibold text-amber-400">
                                                {branch.escalation_rate.toFixed(
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
                                                        resolutionRate,
                                                        100,
                                                    )}%`,
                                                }}
                                            />
                                        </div>
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                )}
        </section>
    );
}

export default BranchPerformancePanel;