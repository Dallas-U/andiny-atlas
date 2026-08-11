import * as XLSX from "xlsx";

import type {
    InvestigationAnalyticsResponse,
} from "../../analytics/types/analytics.types";

export function exportAnalyticsToExcel(
    analytics: InvestigationAnalyticsResponse,
): void {
    const workbook =
        XLSX.utils.book_new();

    const overviewRows = [
        {
            Metric: "Start Date",
            Value: analytics.start_date,
        },
        {
            Metric: "End Date",
            Value: analytics.end_date,
        },
        {
            Metric: "Interval",
            Value: analytics.interval,
        },
        {
            Metric: "Total Cases",
            Value: analytics.kpis.total_cases,
        },
        {
            Metric: "Resolved Cases",
            Value: analytics.kpis.resolved_cases,
        },
        {
            Metric: "Waiting Cases",
            Value: analytics.kpis.waiting_cases,
        },
        {
            Metric:
                "Technical Investigation Cases",
            Value:
                analytics.kpis
                    .technical_investigation_cases,
        },
        {
            Metric: "Escalated Cases",
            Value: analytics.kpis.escalated_cases,
        },
        {
            Metric: "Resolution Rate",
            Value:
                `${analytics.kpis.resolution_rate}%`,
        },
        {
            Metric: "Escalation Rate",
            Value:
                `${analytics.kpis.escalation_rate}%`,
        },
    ];

    const overviewSheet =
        XLSX.utils.json_to_sheet(
            overviewRows,
        );

    XLSX.utils.book_append_sheet(
        workbook,
        overviewSheet,
        "Overview",
    );

    const trendSheet =
        XLSX.utils.json_to_sheet(
            analytics.trend.map(
                (item) => ({
                    Period: item.period,
                    Count: item.count,
                }),
            ),
        );

    XLSX.utils.book_append_sheet(
        workbook,
        trendSheet,
        "Trend",
    );

    const statusSheet =
        XLSX.utils.json_to_sheet(
            analytics.status_distribution.map(
                (item) => ({
                    Status: item.status,
                    Count: item.count,
                    Percentage:
                        `${item.percentage}%`,
                }),
            ),
        );

    XLSX.utils.book_append_sheet(
        workbook,
        statusSheet,
        "Status Distribution",
    );

    const workloadSheet =
        XLSX.utils.json_to_sheet(
            analytics.investigator_workload.map(
                (item) => ({
                    Investigator:
                        item.investigator_name,
                    "Investigator ID":
                        item.investigator_id,
                    Investigations:
                        item.count,
                }),
            ),
        );

    XLSX.utils.book_append_sheet(
        workbook,
        workloadSheet,
        "Investigator Workload",
    );

    const filename =
        `investigation-analytics-${analytics.start_date}-to-${analytics.end_date}.xlsx`;

    XLSX.writeFile(
        workbook,
        filename,
    );
}