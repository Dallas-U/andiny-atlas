import { useEffect, useState } from "react";

import BackButton from "../../../shared/components/BackButton";
import PageHeader from "../../../shared/components/PageHeader";

import ExportOptions from "../components/ExportOptions";
import ExportPreview from "../components/ExportPreview";
import ExportHistory from "../components/ExportHistory";

import {
    getInvestigationSummaryReport,
} from "../../reports/api/reports.api";

import {
    getInvestigationAnalytics,
} from "../../analytics/api/analytics.api";

import {
    exportReportViaBackend,
} from "../api/backendExport.api";

import {
    exportAnalyticsToCsv,
} from "../utils/analyticsCsvExport";

import {
    exportAnalyticsToExcel,
} from "../utils/analyticsExcelExport";

import {
    exportAnalyticsToPdf,
} from "../utils/analyticsPdfExport";

import {
    getExportHistory,
} from "../api/exportAudit.api";

import type {
    InvestigationReportResponse,
} from "../../reports/types/report.types";

import type {
    InvestigationAnalyticsResponse,
} from "../../analytics/types/analytics.types";

import type {
    InvestigationStatus,
} from "../../investigation/types/investigation.types";

import type {
    ExportFormat,
    ExportHistoryItem,
    ExportSource,
} from "../types/export.types";

type AnalyticsInterval =
    | "day"
    | "week"
    | "month";

function today(): string {
    return new Date()
        .toISOString()
        .slice(0, 10);
}

function thirtyDaysAgo(): string {
    const date = new Date();

    date.setDate(
        date.getDate() - 30,
    );

    return date
        .toISOString()
        .slice(0, 10);
}

function ExportCenterPage() {
    const [source, setSource] =
        useState<ExportSource>("reports");

    const [format, setFormat] =
        useState<ExportFormat>("csv");

    const [startDate, setStartDate] =
        useState(thirtyDaysAgo());

    const [endDate, setEndDate] =
        useState(today());

    const [status, setStatus] =
        useState<InvestigationStatus | "">("");

    const [interval, setInterval] =
        useState<AnalyticsInterval>("day");

    const [report, setReport] =
        useState<InvestigationReportResponse | null>(
            null,
        );

    const [analytics, setAnalytics] =
        useState<InvestigationAnalyticsResponse | null>(
            null,
        );

    const [history, setHistory] =
        useState<ExportHistoryItem[]>([]);

    const [isLoading, setIsLoading] =
        useState(false);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    async function loadHistory(): Promise<void> {
        try {
            const records =
                await getExportHistory();

            setHistory(records);
        } catch (error) {
            console.error(
                "Failed to load Trust Ledger history:",
                error,
            );
        }
    }

    useEffect(() => {
        loadHistory();
    }, []);

    function handleSourceChange(
        nextSource: ExportSource,
    ): void {
        setSource(nextSource);

        setReport(null);
        setAnalytics(null);
        setErrorMessage(null);
    }

    async function handleGeneratePreview(): Promise<void> {
        try {
            setIsLoading(true);
            setErrorMessage(null);

            if (source === "reports") {
                const response =
                    await getInvestigationSummaryReport({
                        start_date: startDate,
                        end_date: endDate,
                        ...(status
                            ? {
                                status,
                            }
                            : {}),
                    });

                setReport(response);
                setAnalytics(null);

                return;
            }

            const response =
                await getInvestigationAnalytics({
                    start_date: startDate,
                    end_date: endDate,
                    interval,
                });

            setAnalytics(response);
            setReport(null);
        } catch (error) {
            console.error(
                "Failed to generate export preview:",
                error,
            );

            setReport(null);
            setAnalytics(null);

            setErrorMessage(
                "Unable to generate the export preview.",
            );
        } finally {
            setIsLoading(false);
        }
    }

    async function handleReportExport(): Promise<boolean> {
        if (!report) {
            return false;
        }

        await exportReportViaBackend(
            report,
            format,
        );

        return true;
    }

    async function handleAnalyticsExport(): Promise<boolean> {
        if (!analytics) {
            return false;
        }

        if (format === "csv") {
            await exportAnalyticsToCsv(
                analytics,
            );

            return true;
        }

        if (format === "excel") {
            await exportAnalyticsToExcel(
                analytics,
            );

            return true;
        }

        await exportAnalyticsToPdf(
            analytics,
        );

        return true;
    }

    async function handleExport(): Promise<void> {
        const exported =
            source === "reports"
                ? await handleReportExport()
                : await handleAnalyticsExport();

        if (exported) {
            await loadHistory();
        }
    }

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">

                <div className="mb-6">
                    <BackButton />
                </div>

                <PageHeader
                    title="Export Centre"
                    description="Generate and manage investigation and analytics exports."
                />

                <div className="mt-8 space-y-8">
                    <ExportOptions
                        source={source}
                        format={format}
                        startDate={startDate}
                        endDate={endDate}
                        status={status}
                        interval={interval}
                        isLoading={isLoading}
                        onSourceChange={
                            handleSourceChange
                        }
                        onFormatChange={
                            setFormat
                        }
                        onStartDateChange={
                            setStartDate
                        }
                        onEndDateChange={
                            setEndDate
                        }
                        onStatusChange={
                            setStatus
                        }
                        onIntervalChange={
                            setInterval
                        }
                        onGeneratePreview={
                            handleGeneratePreview
                        }
                    />

                    <ExportPreview
                        source={source}
                        format={format}
                        report={report}
                        analytics={analytics}
                        errorMessage={
                            errorMessage
                        }
                        onExport={
                            handleExport
                        }
                    />

                    <ExportHistory
                        history={history}
                    />
                </div>

            </div>
        </main>
    );
}

export default ExportCenterPage;