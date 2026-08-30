import { useState } from "react";

import PageHeader from "../../../shared/components/PageHeader";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";
import Card from "../../../shared/components/Card";

import AnalyticsFilters from "../components/AnalyticsFilters";
import BackButton from "../../../shared/components/BackButton";
import AnalyticsOverviewCards from "../components/AnalyticsOverviewCards";
import InvestigationTrendChart from "../components/InvestigationTrendChart";
import StatusDistributionChart from "../components/StatusDistributionChart";
import InvestigatorWorkloadTable from "../components/InvestigatorWorkloadTable";

import {
    getInvestigationAnalytics,
    type InvestigationAnalyticsQuery,
} from "../api/analytics.api";

import type {
    InvestigationAnalyticsResponse,
} from "../types/analytics.types";

function AnalyticsPage() {
    const [analytics, setAnalytics] =
        useState<InvestigationAnalyticsResponse | null>(
            null,
        );

    const [isLoading, setIsLoading] =
        useState(false);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    async function handleApply(
        filters: InvestigationAnalyticsQuery,
    ) {
        try {
            setIsLoading(true);
            setErrorMessage(null);

            const response =
                await getInvestigationAnalytics(
                    filters,
                );

            setAnalytics(response);
        } catch (error) {
            console.error(
                "Failed to load analytics:",
                error,
            );

            setErrorMessage(
                "Unable to load analytics.",
            );
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">
                <div className="mb-6">
                    <BackButton />
                </div>
                <PageHeader
                    title="Investigation Analytics"
                    description="Operational insights into investigation performance."
                />

                <div className="mt-8">
                    <AnalyticsFilters
                        onApply={handleApply}
                        isLoading={isLoading}
                    />
                </div>

                {isLoading && (
                    <div className="mt-8">
                        <LoadingSkeleton className="h-72 w-full" />
                    </div>
                )}

                {errorMessage && (
                    <Card className="mt-8 border-red-900">
                        <p className="text-red-400">
                            {errorMessage}
                        </p>
                    </Card>
                )}

                {analytics && !isLoading && (
                    <div className="mt-8 space-y-8">
                        <AnalyticsOverviewCards
                            kpis={analytics.kpis}
                        />

                        <InvestigationTrendChart
                            items={analytics.trend}
                        />

                        <StatusDistributionChart
                            items={
                                analytics.status_distribution
                            }
                        />

                        <InvestigatorWorkloadTable
                            investigators={
                                analytics.investigator_workload
                            }
                        />
                    </div>
                )}
            </div>
        </main>
    );
}

export default AnalyticsPage;