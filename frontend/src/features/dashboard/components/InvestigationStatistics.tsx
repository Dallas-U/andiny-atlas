import {
    AlertTriangle,
    CheckCircle2,
    Clock3,
    Files,
} from "lucide-react";
import { useEffect, useState } from "react";

import Card from "../../../shared/components/Card";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";
import StatCard from "../../../shared/components/StatCard";
import { getStatistics } from "../../investigation/api/investigation.api";
import type { Statistics } from "../../investigation/types/investigation.types";

function InvestigationStatistics() {
    const [statistics, setStatistics] =
        useState<Statistics | null>(null);

    const [isLoading, setIsLoading] =
        useState(true);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    useEffect(() => {
        async function loadStatistics(): Promise<void> {
            try {
                setIsLoading(true);
                setErrorMessage(null);

                const response = await getStatistics();

                setStatistics(response);
            } catch (error) {
                console.error(
                    "Failed to load investigation statistics:",
                    error,
                );

                setErrorMessage(
                    "Unable to load investigation statistics.",
                );
            } finally {
                setIsLoading(false);
            }
        }

        void loadStatistics();
    }, []);

    return (
        <section className="mt-10">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Investigation Statistics
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Live operational metrics from the investigation platform.
                </p>
            </div>

            {isLoading && (
                <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                    {Array.from({ length: 4 }).map((_, index) => (
                        <Card key={index}>
                            <div className="space-y-5">
                                <LoadingSkeleton className="h-4 w-1/2" />
                                <LoadingSkeleton className="h-10 w-1/3" />
                                <LoadingSkeleton className="h-12 w-12" />
                            </div>
                        </Card>
                    ))}
                </div>
            )}

            {!isLoading && errorMessage && (
                <Card className="mt-4 border-red-900">
                    <p className="text-red-400">
                        {errorMessage}
                    </p>
                </Card>
            )}

            {!isLoading && statistics && (
                <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                    <StatCard
                        title="Total investigations"
                        value={statistics.total_cases}
                        description="All investigation cases currently recorded."
                        icon={
                            <Files className="h-6 w-6 text-slate-300" />
                        }
                    />

                    <StatCard
                        title="Resolved"
                        value={statistics.resolved_cases}
                        description="Cases completed with a resolved outcome."
                        icon={
                            <CheckCircle2 className="h-6 w-6 text-green-300" />
                        }
                    />

                    <StatCard
                        title="Waiting"
                        value={statistics.pending_cases}
                        description="Cases awaiting further investigation or action."
                        icon={
                            <Clock3 className="h-6 w-6 text-amber-300" />
                        }
                    />

                    <StatCard
                        title="Escalated"
                        value={statistics.escalated_cases}
                        description="Cases transferred for higher-level attention."
                        icon={
                            <AlertTriangle className="h-6 w-6 text-red-300" />
                        }
                    />
                </div>
            )}
        </section>
    );
}

export default InvestigationStatistics;