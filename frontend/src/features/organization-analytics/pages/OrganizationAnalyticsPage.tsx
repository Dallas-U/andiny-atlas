import { useEffect, useState } from "react";

import BackButton from "../../../shared/components/BackButton";
import PageHeader from "../../../shared/components/PageHeader";
import Card from "../../../shared/components/Card";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";

import {
    getOrganizationAnalytics,
} from "../api/organizationAnalytics.api";

import type {
    OrganizationAnalytics,
} from "../types/organizationAnalytics.types";

function OrganizationAnalyticsPage() {
    const [data, setData] = useState<OrganizationAnalytics[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function load() {
            try {
                const response = await getOrganizationAnalytics();
                setData(response);
            } finally {
                setIsLoading(false);
            }
        }

        load();
    }, []);

    const totalCases = data.reduce(
        (sum, item) =>
            sum + item.total_cases,
        0,
    );

    const totalResolved = data.reduce(
        (sum, item) =>
            sum + item.resolved_cases,
        0,
    );

    const overallResolution =
        totalCases === 0
            ? 0
            : Math.round(
                (totalResolved / totalCases) * 100,
            );

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">
                <div className="mb-6">
                    <BackButton />
                </div>

                <PageHeader
                    title="Organization Analytics"
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
                                    {data.length}
                                </div>
                            </Card>

                            <Card>
                                <div className="text-sm text-slate-400">
                                    Total Cases
                                </div>
                                <div className="mt-2 text-3xl font-semibold text-white">
                                    {totalCases}
                                </div>
                            </Card>

                            <Card>
                                <div className="text-sm text-slate-400">
                                    Resolved Cases
                                </div>
                                <div className="mt-2 text-3xl font-semibold text-white">
                                    {totalResolved}
                                </div>
                            </Card>

                            <Card>
                                <div className="text-sm text-slate-400">
                                    Overall Resolution
                                </div>
                                <div className="mt-2 text-3xl font-semibold text-white">
                                    {overallResolution}%
                                </div>
                            </Card>
                        </div>

                        <Card className="mt-8 overflow-hidden">
                            <div className="border-b border-slate-800 px-6 py-4">
                                <h2 className="text-lg font-semibold text-white">
                                    Organization performance
                                </h2>
                            </div>

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
                                        {data.map((item) => (
                                            <tr key={item.organization}>
                                                <td className="px-6 py-4 text-sm font-medium text-white">
                                                    {item.organization}
                                                </td>
                                                <td className="px-6 py-4 text-sm text-slate-300">
                                                    {item.total_cases}
                                                </td>
                                                <td className="px-6 py-4 text-sm text-emerald-400">
                                                    {item.resolved_cases}
                                                </td>
                                                <td className="px-6 py-4 text-sm text-amber-400">
                                                    {item.escalated_cases}
                                                </td>
                                                <td className="px-6 py-4 text-sm text-white">
                                                    {item.resolution_rate}%
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </Card>
                    </>
                )}
            </div>
        </main>
    );
}

export default OrganizationAnalyticsPage;