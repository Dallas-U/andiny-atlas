import { useState } from "react";

import PageHeader from "../../../shared/components/PageHeader";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";

import ReportFilters from "../components/ReportFilters";
import ReportSummaryCards from "../components/ReportSummaryCards";
import ReportResultsTable from "../components/ReportResultsTable";
import BackButton from "../../../shared/components/BackButton";
import { exportReportToCsv } from "../../exports/utils/reportCsvExport";
import { exportReportToExcel } from "../../exports/utils/reportExcelExport";
import { exportReportToPdf } from "../../exports/utils/reportPdfExport";

import { getInvestigationSummaryReport } from "../api/reports.api";

import type {
    InvestigationReportResponse,
} from "../types/report.types";

import type {
    ReportFilterFormData,
} from "../schema/report.schema";

function ReportsPage() {
    const [report, setReport] =
        useState<InvestigationReportResponse | null>(
            null,
        );

    const [isLoading, setIsLoading] =
        useState(false);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    async function handleGenerate(
        filters: ReportFilterFormData,
    ) {
        try {
            setIsLoading(true);
            setErrorMessage(null);

            const response =
                await getInvestigationSummaryReport(
                    filters,
                );

            setReport(response);
        } catch (error) {
            console.error(
                "Failed to generate report:",
                error,
            );

            setErrorMessage(
                "Unable to generate report.",
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
                    title="Investigation Reports"
                    description="Generate operational reports for investigation activities."
                />

                <div className="mt-8">
                    <ReportFilters
                        onGenerate={handleGenerate}
                        isLoading={isLoading}
                    />
                </div>

                {isLoading && (
                    <div className="mt-8">
                        <LoadingSkeleton className="h-56 w-full" />
                    </div>
                )}

                {errorMessage && (
                    <div className="mt-8 rounded-xl border border-red-900 bg-slate-900 p-5">
                        <p className="text-red-400">
                            {errorMessage}
                        </p>
                    </div>
                )}

                {report && (
                    <div className="mt-8 space-y-8">

                        <div className="flex flex-wrap justify-end gap-3">
                            <button
                                type="button"
                                onClick={() => {
                                    exportReportToCsv(report.items);
                                }}
                                disabled={report.items.length === 0}
                                className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:border-slate-600 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                Export CSV
                            </button>

                            <button
                                type="button"
                                onClick={() => {
                                    exportReportToExcel(report.items);
                                }}
                                disabled={report.items.length === 0}
                                className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:border-slate-600 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                Export Excel
                            </button>

                            <button
                                type="button"
                                onClick={() => {
                                    exportReportToPdf(report);
                                }}
                                disabled={report.items.length === 0}
                                className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                Export PDF
                            </button>
                        </div>

                        <ReportSummaryCards
                            summary={report.summary}
                        />

                        <ReportResultsTable
                            investigations={report.items}
                        />

                    </div>
                )}

            </div>
        </main>
    );
}

export default ReportsPage;