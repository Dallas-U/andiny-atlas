import { useEffect, useState } from "react";

import PageHeader from "../../../shared/components/PageHeader";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";
import Card from "../../../shared/components/Card";
import BackButton from "../../../shared/components/BackButton";

import ExecutiveKpiCards from "../components/ExecutiveKpiCards";
import BranchPerformancePanel from "../components/BranchPerformancePanel";
import DepartmentPerformancePanel from "../components/DepartmentPerformancePanel";
import DepartmentCasePanel from "../components/DepartmentCasePanel";

import {
    getEnterpriseAnalytics,
    type EnterpriseAnalyticsResponse,
} from "../api/enterpriseAnalyticsApi";

const ORGANIZATION_ID =
    "8909e590-3bc6-4f7f-afc4-8c674b71a538";

function ExecutiveDashboardPage() {
    const [analytics, setAnalytics] =
        useState<EnterpriseAnalyticsResponse | null>(
            null,
        );

    const [selectedBranchId, setSelectedBranchId] =
        useState<string | null>(null);

    const [selectedDepartmentId, setSelectedDepartmentId] =
        useState<string | null>(null);

    const [selectedDepartmentName, setSelectedDepartmentName] =
        useState<string | null>(null);

    const [isLoading, setIsLoading] =
        useState(true);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    useEffect(() => {
        async function loadExecutiveAnalytics() {
            try {
                setIsLoading(true);
                setErrorMessage(null);

                const response =
                    await getEnterpriseAnalytics(
                        ORGANIZATION_ID,
                    );

                setAnalytics(response);
            } catch (error) {
                console.error(
                    "Failed to load executive analytics:",
                    error,
                );

                setErrorMessage(
                    "Unable to load executive analytics.",
                );
            } finally {
                setIsLoading(false);
            }
        }

        void loadExecutiveAnalytics();
    }, []);

    function handleSelectBranch(
        branchId: string,
    ): void {
        setSelectedBranchId(branchId);

        /*
         * A department belongs to a branch.
         * Changing branches therefore invalidates the
         * currently selected department.
         */
        setSelectedDepartmentId(null);
        setSelectedDepartmentName(null);
    }

    function handleSelectDepartment(
        departmentId: string,
        departmentName: string,
    ): void {
        setSelectedDepartmentId(departmentId);
        setSelectedDepartmentName(departmentName);
    }

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">
                <div className="mb-6">
                    <BackButton />
                </div>

                <PageHeader
                    title="Executive Dashboard"
                    description="Enterprise-level visibility into investigation performance."
                />

                {isLoading && (
                    <div className="mt-8 space-y-6">
                        <LoadingSkeleton className="h-48 w-full" />

                        <LoadingSkeleton className="h-72 w-full" />

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
                        <ExecutiveKpiCards
                            kpis={analytics.kpis}
                        />

                        <BranchPerformancePanel
                            selectedBranchId={
                                selectedBranchId
                            }
                            onSelectBranch={
                                handleSelectBranch
                            }
                        />

                        <DepartmentPerformancePanel
                            selectedBranchId={
                                selectedBranchId
                            }
                            selectedDepartmentId={
                                selectedDepartmentId
                            }
                            onSelectDepartment={
                                handleSelectDepartment
                            }
                        />

                        <DepartmentCasePanel
                            departmentId={
                                selectedDepartmentId
                            }
                            departmentName={
                                selectedDepartmentName
                            }
                        />
                    </div>
                )}
            </div>
        </main>
    );
}

export default ExecutiveDashboardPage;