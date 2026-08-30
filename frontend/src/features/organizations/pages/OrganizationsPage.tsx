import { useEffect, useMemo, useState } from "react";

import BackButton from "../../../shared/components/BackButton";
import Card from "../../../shared/components/Card";
import EmptyState from "../../../shared/components/EmptyState";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";
import PageHeader from "../../../shared/components/PageHeader";

import { getOrganizationOverview } from "../api/organization.api";

import type { OrganizationOverview } from "../types/organization.types";

function OrganizationsPage() {
    const [organizations, setOrganizations] = useState<
        OrganizationOverview[]
    >([]);

    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadOrganizations() {
            try {
                const response =
                    await getOrganizationOverview();

                setOrganizations(response);
            } catch (error) {
                console.error(
                    "Failed to load organizations:",
                    error,
                );
            } finally {
                setIsLoading(false);
            }
        }

        loadOrganizations();
    }, []);

    const summary = useMemo(() => {
        const totalOrganizations =
            organizations.length;

        const totalCases = organizations.reduce(
            (sum, organization) =>
                sum + organization.total_cases,
            0,
        );

        const totalResolved = organizations.reduce(
            (sum, organization) =>
                sum + organization.resolved_cases,
            0,
        );

        const totalEscalated = organizations.reduce(
            (sum, organization) =>
                sum + organization.escalated_cases,
            0,
        );

        const averageResolutionRate =
            totalOrganizations === 0
                ? 0
                : Math.round(
                    organizations.reduce(
                        (sum, organization) =>
                            sum +
                            organization.resolution_rate,
                        0,
                    ) / totalOrganizations,
                );

        return {
            totalOrganizations,
            totalCases,
            totalResolved,
            totalEscalated,
            averageResolutionRate,
        };
    }, [organizations]);

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">
                <div className="mb-6">
                    <BackButton />
                </div>

                <PageHeader
                    title="Organizations"
                    description="Executive visibility across every connected organization."
                />

                {isLoading ? (
                    <LoadingSkeleton />
                ) : (
                    <>
                        <div className="mt-8 grid gap-6 md:grid-cols-4">
                            <Card>
                                <div className="text-sm text-slate-400">
                                    Organizations
                                </div>
                                <div className="mt-2 text-3xl font-semibold text-white">
                                    {
                                        summary.totalOrganizations
                                    }
                                </div>
                            </Card>

                            <Card>
                                <div className="text-sm text-slate-400">
                                    Total Cases
                                </div>
                                <div className="mt-2 text-3xl font-semibold text-white">
                                    {summary.totalCases}
                                </div>
                            </Card>

                            <Card>
                                <div className="text-sm text-slate-400">
                                    Resolved
                                </div>
                                <div className="mt-2 text-3xl font-semibold text-emerald-400">
                                    {
                                        summary.totalResolved
                                    }
                                </div>
                            </Card>

                            <Card>
                                <div className="text-sm text-slate-400">
                                    Avg. Resolution
                                </div>
                                <div className="mt-2 text-3xl font-semibold text-white">
                                    {
                                        summary.averageResolutionRate
                                    }
                                    %
                                </div>
                            </Card>
                        </div>

                        <Card className="mt-8">
                            <div className="border-b border-slate-800 px-6 py-4">
                                <h2 className="text-lg font-semibold text-white">
                                    Organization performance
                                </h2>
                            </div>

                            {organizations.length === 0 ? (
                                <div className="p-6">
                                    <EmptyState
                                        title="No organizations available"
                                        description="Organization analytics will appear here once investigation activity is available."
                                    />
                                </div>
                            ) : (
                                <div className="overflow-x-auto">
                                    <table className="min-w-full divide-y divide-slate-800">
                                        <thead className="bg-slate-900">
                                            <tr>
                                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                    Organization
                                                </th>
                                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                    Cases
                                                </th>
                                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                    Resolved
                                                </th>
                                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                    Escalated
                                                </th>
                                                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                    Resolution
                                                </th>
                                            </tr>
                                        </thead>

                                        <tbody className="divide-y divide-slate-800 bg-slate-950">
                                            {organizations.map(
                                                (organization) => (
                                                    <tr
                                                        key={
                                                            organization.organization
                                                        }
                                                    >
                                                        <td className="px-6 py-4 text-sm font-medium text-white">
                                                            {
                                                                organization.organization
                                                            }
                                                        </td>

                                                        <td className="px-6 py-4 text-sm text-slate-300">
                                                            {
                                                                organization.total_cases
                                                            }
                                                        </td>

                                                        <td className="px-6 py-4 text-sm text-emerald-400">
                                                            {
                                                                organization.resolved_cases
                                                            }
                                                        </td>

                                                        <td className="px-6 py-4 text-sm text-amber-400">
                                                            {
                                                                organization.escalated_cases
                                                            }
                                                        </td>

                                                        <td className="px-6 py-4">
                                                            <div className="flex items-center gap-3">
                                                                <div className="h-2 w-32 rounded-full bg-slate-800">
                                                                    <div
                                                                        className="h-2 rounded-full bg-emerald-500"
                                                                        style={{
                                                                            width: `${organization.resolution_rate}%`,
                                                                        }}
                                                                    />
                                                                </div>

                                                                <span className="text-sm text-white">
                                                                    {
                                                                        organization.resolution_rate
                                                                    }
                                                                    %
                                                                </span>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                ),
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </Card>
                    </>
                )}
            </div>
        </main>
    );
}

export default OrganizationsPage;