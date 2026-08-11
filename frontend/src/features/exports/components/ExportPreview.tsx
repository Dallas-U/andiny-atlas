import type {
    ReactNode,
} from "react";

import Card from "../../../shared/components/Card";
import EmptyState from "../../../shared/components/EmptyState";

import type {
    InvestigationReportResponse,
} from "../../reports/types/report.types";

import type {
    InvestigationAnalyticsResponse,
} from "../../analytics/types/analytics.types";

import type {
    ExportFormat,
    ExportSource,
} from "../types/export.types";

interface ExportPreviewProps {
    source: ExportSource;
    format: ExportFormat;

    report:
    InvestigationReportResponse | null;

    analytics:
    InvestigationAnalyticsResponse | null;

    errorMessage: string | null;

    onExport: () => void;
}

function ExportPreview({
    source,
    format,
    report,
    analytics,
    errorMessage,
    onExport,
}: ExportPreviewProps) {
    if (errorMessage) {
        return (
            <Card className="border-red-900">
                <p className="text-red-400">
                    {errorMessage}
                </p>
            </Card>
        );
    }

    const formatLabel =
        format === "excel"
            ? "Excel (.xlsx)"
            : format.toUpperCase();

    if (source === "reports") {
        if (!report) {
            return (
                <EmptyState
                    title="No export preview yet"
                    description="Configure the report options above and generate a preview."
                />
            );
        }

        return (
            <Card>
                <div className="flex flex-wrap items-start justify-between gap-4">
                    <div>
                        <h2 className="text-xl font-semibold text-white">
                            Report Export Preview
                        </h2>

                        <p className="mt-1 text-sm text-slate-400">
                            Review the report before downloading.
                        </p>
                    </div>

                    <button
                        type="button"
                        onClick={onExport}
                        disabled={
                            report.items.length === 0
                        }
                        className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        Export {formatLabel}
                    </button>
                </div>

                <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                    <PreviewMetric
                        label="Reporting Period"
                        value={`${report.start_date} → ${report.end_date}`}
                    />

                    <PreviewMetric
                        label="Status"
                        value={
                            report.applied_status ??
                            "All statuses"
                        }
                    />

                    <PreviewMetric
                        label="Records"
                        value={report.items.length}
                    />

                    <PreviewMetric
                        label="Format"
                        value={formatLabel}
                    />
                </div>

                <div className="mt-6 overflow-x-auto">
                    <table className="min-w-full divide-y divide-slate-800">
                        <thead className="bg-slate-950/60">
                            <tr>
                                <TableHeading>
                                    Customer
                                </TableHeading>

                                <TableHeading>
                                    Phone
                                </TableHeading>

                                <TableHeading>
                                    Status
                                </TableHeading>

                                <TableHeading>
                                    Created
                                </TableHeading>
                            </tr>
                        </thead>

                        <tbody className="divide-y divide-slate-800">
                            {report.items
                                .slice(0, 5)
                                .map((item) => (
                                    <tr
                                        key={
                                            item.case_id
                                        }
                                    >
                                        <TableCell>
                                            {
                                                item.customer_name
                                            }
                                        </TableCell>

                                        <TableCell>
                                            {
                                                item.phone_number
                                            }
                                        </TableCell>

                                        <TableCell>
                                            {
                                                item.result
                                                    .status
                                            }
                                        </TableCell>

                                        <TableCell>
                                            {
                                                item.timestamp
                                            }
                                        </TableCell>
                                    </tr>
                                ))}
                        </tbody>
                    </table>

                    {report.items.length > 5 && (
                        <p className="mt-3 text-sm text-slate-500">
                            Showing the first 5 of{" "}
                            {report.items.length} records.
                        </p>
                    )}
                </div>
            </Card>
        );
    }

    if (!analytics) {
        return (
            <EmptyState
                title="No analytics preview yet"
                description="Configure the analytics options above and generate a preview."
            />
        );
    }

    return (
        <Card>
            <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                    <h2 className="text-xl font-semibold text-white">
                        Analytics Export Preview
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        Review the analytics data before generating
                        the export.
                    </p>
                </div>

                <button
                    type="button"
                    onClick={onExport}
                    disabled={
                        analytics.kpis.total_cases === 0
                    }
                    className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    Export {formatLabel}
                </button>
            </div>

            <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <PreviewMetric
                    label="Reporting Period"
                    value={`${analytics.start_date} → ${analytics.end_date}`}
                />

                <PreviewMetric
                    label="Interval"
                    value={analytics.interval}
                />

                <PreviewMetric
                    label="Total Cases"
                    value={
                        analytics.kpis.total_cases
                    }
                />

                <PreviewMetric
                    label="Format"
                    value={formatLabel}
                />

                <PreviewMetric
                    label="Resolved"
                    value={
                        analytics.kpis.resolved_cases
                    }
                />

                <PreviewMetric
                    label="Escalated"
                    value={
                        analytics.kpis.escalated_cases
                    }
                />

                <PreviewMetric
                    label="Resolution Rate"
                    value={`${analytics.kpis.resolution_rate}%`}
                />

                <PreviewMetric
                    label="Escalation Rate"
                    value={`${analytics.kpis.escalation_rate}%`}
                />
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-2">
                <div className="rounded-lg border border-slate-800 bg-slate-950 p-5">
                    <h3 className="font-semibold text-white">
                        Trend
                    </h3>

                    {analytics.trend.length === 0 ? (
                        <p className="mt-4 text-sm text-slate-500">
                            No trend data available.
                        </p>
                    ) : (
                        <div className="mt-4 space-y-3">
                            {analytics.trend.map(
                                (item) => (
                                    <div
                                        key={item.period}
                                        className="flex items-center justify-between gap-4"
                                    >
                                        <span className="text-sm text-slate-400">
                                            {
                                                item.period
                                            }
                                        </span>

                                        <span className="font-medium text-white">
                                            {
                                                item.count
                                            }
                                        </span>
                                    </div>
                                ),
                            )}
                        </div>
                    )}
                </div>

                <div className="rounded-lg border border-slate-800 bg-slate-950 p-5">
                    <h3 className="font-semibold text-white">
                        Status Distribution
                    </h3>

                    {analytics.status_distribution.length ===
                        0 ? (
                        <p className="mt-4 text-sm text-slate-500">
                            No status distribution available.
                        </p>
                    ) : (
                        <div className="mt-4 space-y-3">
                            {analytics.status_distribution.map(
                                (item) => (
                                    <div
                                        key={
                                            item.status
                                        }
                                        className="flex items-center justify-between gap-4"
                                    >
                                        <span className="text-sm text-slate-400">
                                            {
                                                item.status
                                            }
                                        </span>

                                        <span className="font-medium text-white">
                                            {
                                                item.count
                                            }
                                            {" · "}
                                            {
                                                item.percentage
                                            }
                                            %
                                        </span>
                                    </div>
                                ),
                            )}
                        </div>
                    )}
                </div>
            </div>

            <div className="mt-6 rounded-lg border border-slate-800 bg-slate-950 p-5">
                <h3 className="font-semibold text-white">
                    Investigator Workload
                </h3>

                {analytics.investigator_workload.length ===
                    0 ? (
                    <p className="mt-4 text-sm text-slate-500">
                        No investigator workload data available.
                    </p>
                ) : (
                    <div className="mt-4 space-y-3">
                        {analytics.investigator_workload.map(
                            (investigator) => (
                                <div
                                    key={
                                        investigator.investigator_id
                                    }
                                    className="flex flex-wrap items-center justify-between gap-4"
                                >
                                    <div>
                                        <p className="text-sm font-medium text-slate-300">
                                            {
                                                investigator.investigator_name
                                            }
                                        </p>

                                        <p className="mt-1 text-xs text-slate-600">
                                            {
                                                investigator.investigator_id
                                            }
                                        </p>
                                    </div>

                                    <span className="font-medium text-white">
                                        {
                                            investigator.count
                                        }{" "}
                                        investigations
                                    </span>
                                </div>
                            ),
                        )}
                    </div>
                )}
            </div>
        </Card>
    );
}

interface PreviewMetricProps {
    label: string;
    value: string | number;
}

function PreviewMetric({
    label,
    value,
}: PreviewMetricProps) {
    return (
        <div className="rounded-lg border border-slate-800 bg-slate-950 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-500">
                {label}
            </p>

            <p className="mt-2 font-medium capitalize text-white">
                {value}
            </p>
        </div>
    );
}

interface TableCellProps {
    children: ReactNode;
}

function TableCell({
    children,
}: TableCellProps) {
    return (
        <td className="px-5 py-4 text-sm text-slate-300">
            {children}
        </td>
    );
}

interface TableHeadingProps {
    children: ReactNode;
}

function TableHeading({
    children,
}: TableHeadingProps) {
    return (
        <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
            {children}
        </th>
    );
}

export default ExportPreview;