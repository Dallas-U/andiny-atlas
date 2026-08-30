import { useEffect, useState } from "react";
import { useParams } from "@tanstack/react-router";

import BackButton from "../shared/components/BackButton";
import LoadingSkeleton from "../shared/components/LoadingSkeleton";

import EditInvestigationForm from "../features/investigation/components/EditInvestigationForm";
import InvestigationDetails from "../features/investigation/components/InvestigationDetails";
import InvestigationHistory from "../features/investigation/components/InvestigationHistory";
import { getCase } from "../features/investigation/api/investigation.api";
import type { CaseResponse } from "../features/investigation/types/investigation.types";

import Card from "../shared/components/Card";
import PageHeader from "../shared/components/PageHeader";

function InvestigationDetailsPage() {

    const { caseId } = useParams({
        from: "/dashboard/investigations/$caseId",
    });

    const [investigation, setInvestigation] =
        useState<CaseResponse | null>(null);

    const [historyRefreshKey, setHistoryRefreshKey] =
        useState(0);

    const [isLoading, setIsLoading] =
        useState(true);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    useEffect(() => {
        async function loadInvestigation(): Promise<void> {
            try {
                setIsLoading(true);
                setErrorMessage(null);

                const response = await getCase(caseId);

                setInvestigation(response);
            } catch (error) {
                console.error(
                    "Failed to load investigation:",
                    error,
                );

                setErrorMessage(
                    "Unable to load this investigation.",
                );
            } finally {
                setIsLoading(false);
            }
        }

        void loadInvestigation();
    }, [caseId]);

    function handleInvestigationUpdated(
        updatedInvestigation: CaseResponse,
    ) {
        setInvestigation(updatedInvestigation);

        setHistoryRefreshKey(
            (currentKey) => currentKey + 1,
        );
    }

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-5xl">

                <div className="mb-8">
                    <BackButton
                        to="/dashboard/investigations"
                        label="Back to investigations"
                    />
                </div>

                <PageHeader
                    title="Investigation Details"
                    description="Review the current investigation, update its outcome, and inspect its immutable audit history."
                />

                <div className="mt-8 space-y-8">

                    {isLoading && (
                        <Card>
                            <div className="space-y-6">
                                <LoadingSkeleton className="h-8 w-1/2" />

                                <LoadingSkeleton className="h-5 w-1/3" />

                                <LoadingSkeleton className="h-20 w-full" />

                                <LoadingSkeleton className="h-20 w-full" />
                            </div>
                        </Card>
                    )}

                    {!isLoading &&
                        (errorMessage || !investigation) && (
                            <Card className="border-red-900">
                                <p className="text-red-400">
                                    {errorMessage ??
                                        "Unable to load this investigation."}
                                </p>
                            </Card>
                        )}

                    {!isLoading &&
                        investigation && (
                            <>
                                <InvestigationDetails
                                    investigation={investigation}
                                />

                                <EditInvestigationForm
                                    investigation={investigation}
                                    onUpdated={
                                        handleInvestigationUpdated
                                    }
                                />

                                <InvestigationHistory
                                    key={
                                        historyRefreshKey
                                    }
                                    caseId={caseId}
                                />
                            </>
                        )}
                </div>
            </div>
        </main>
    );
}

export default InvestigationDetailsPage;